import React, { useCallback, useEffect, useState } from 'react';
import { catalogueClient } from '../api/catalogueClient';
import type { Category, Product } from '../types/catalogue';

import { CategoryNav } from '../components/CategoryNav';
import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { FilterBar } from '../components/FilterBar';
import { Footer } from '../components/Footer';
import { HeroBanner } from '../components/HeroBanner';
import { LoadingState } from '../components/LoadingState';
import { Navbar } from '../components/Navbar';
import { PaginationControls } from '../components/PaginationControls';
import { ProductGrid } from '../components/ProductGrid';

export const CataloguePage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Filter & Pagination States
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [search, setSearch] = useState<string>('');
  const [minPrice, setMinPrice] = useState<string>('');
  const [maxPrice, setMaxPrice] = useState<string>('');
  const [ordering, setOrdering] = useState<string>('-created_at');
  const [currentPage, setCurrentPage] = useState<number>(1);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [cartItems, setCartItems] = useState<Product[]>([]);

  // Fetch Categories once on mount
  useEffect(() => {
    let isMounted = true;
    catalogueClient
      .getCategories()
      .then((data) => {
        if (isMounted) setCategories(data);
      })
      .catch((err) => {
        console.warn('Could not fetch categories:', err);
      });
    return () => {
      isMounted = false;
    };
  }, []);

  // Fetch Products whenever filters or pagination changes
  const loadProducts = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await catalogueClient.getProducts({
        category: selectedCategory,
        search,
        min_price: minPrice,
        max_price: maxPrice,
        ordering,
        page: currentPage,
        page_size: 12,
      });
      setProducts(response.results);
      setTotalPages(response.total_pages);
    } catch (err: any) {
      setError(err.message || 'An unexpected error occurred while fetching products.');
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, search, minPrice, maxPrice, ordering, currentPage]);

  useEffect(() => {
    loadProducts();
  }, [loadProducts]);

  // Handlers
  const handleCategorySelect = (slug: string) => {
    setSelectedCategory(slug);
    setCurrentPage(1);
  };

  const handleSearchChange = (val: string) => {
    setSearch(val);
    setCurrentPage(1);
  };

  const handleMinPriceChange = (val: string) => {
    setMinPrice(val);
    setCurrentPage(1);
  };

  const handleMaxPriceChange = (val: string) => {
    setMaxPrice(val);
    setCurrentPage(1);
  };

  const handleOrderingChange = (val: string) => {
    setOrdering(val);
    setCurrentPage(1);
  };

  const handleResetFilters = () => {
    setSelectedCategory('');
    setSearch('');
    setMinPrice('');
    setMaxPrice('');
    setOrdering('-created_at');
    setCurrentPage(1);
  };

  const handleAddToCart = (product: Product) => {
    setCartItems((prev) => [...prev, product]);
  };

  const hasActiveFilters =
    Boolean(selectedCategory) ||
    Boolean(search) ||
    Boolean(minPrice) ||
    Boolean(maxPrice) ||
    ordering !== '-created_at';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar cartCount={cartItems.length} />
      <HeroBanner />

      <main className="container" style={{ flexGrow: 1 }} id="main-content">
        <CategoryNav
          categories={categories}
          selectedCategory={selectedCategory}
          onSelectCategory={handleCategorySelect}
        />

        <FilterBar
          search={search}
          minPrice={minPrice}
          maxPrice={maxPrice}
          ordering={ordering}
          onSearchChange={handleSearchChange}
          onMinPriceChange={handleMinPriceChange}
          onMaxPriceChange={handleMaxPriceChange}
          onOrderingChange={handleOrderingChange}
          onResetFilters={handleResetFilters}
          hasActiveFilters={hasActiveFilters}
        />

        {loading ? (
          <LoadingState />
        ) : error ? (
          <ErrorState message={error} onRetry={loadProducts} />
        ) : products.length === 0 ? (
          <EmptyState onResetFilters={handleResetFilters} />
        ) : (
          <>
            <ProductGrid products={products} onAddToCart={handleAddToCart} />
            <PaginationControls
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </>
        )}
      </main>

      <Footer />
    </div>
  );
};
