import React, { useCallback, useEffect, useState } from 'react';
import { catalogueClient } from '../api/catalogueClient';
import { authClient } from '../api/authClient';
import { cartClient } from '../api/cartClient';
import type { Category, Product } from '../types/catalogue';
import type { Profile, User } from '../types/auth';
import type { Cart } from '../types/cart';

import { AuthModal } from '../components/AuthModal';
import { CartDrawer } from '../components/CartDrawer';
import { CategoryNav } from '../components/CategoryNav';
import { EmptyState } from '../components/EmptyState';
import { ErrorState } from '../components/ErrorState';
import { FilterBar } from '../components/FilterBar';
import { Footer } from '../components/Footer';
import { HeroBanner } from '../components/HeroBanner';
import { LoadingState } from '../components/LoadingState';
import { Navbar } from '../components/Navbar';
import { PaginationControls } from '../components/PaginationControls';
import { ProductDetailModal } from '../components/ProductDetailModal';
import { ProductGrid } from '../components/ProductGrid';
import { ProfileModal } from '../components/ProfileModal';

export const CataloguePage: React.FC = () => {
  const [categories, setCategories] = useState<Category[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Auth & Profile State
  const [currentUser, setCurrentUser] = useState<{ user: User; profile: Profile } | null>(null);
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isProfileModalOpen, setIsProfileModalOpen] = useState(false);

  // Cart State
  const [cart, setCart] = useState<Cart | null>(null);
  const [cartLoading, setCartLoading] = useState<boolean>(false);
  const [cartError, setCartError] = useState<string | null>(null);
  const [isCartDrawerOpen, setIsCartDrawerOpen] = useState<boolean>(false);

  // URL-Persisted Filter & Product State
  const getUrlParams = () => {
    if (typeof window === 'undefined') return new URLSearchParams();
    return new URLSearchParams(window.location.search);
  };

  const initialParams = getUrlParams();
  const [selectedCategory, setSelectedCategory] = useState<string>(initialParams.get('category') || '');
  const [search, setSearch] = useState<string>(initialParams.get('search') || '');
  const [minPrice, setMinPrice] = useState<string>(initialParams.get('min_price') || '');
  const [maxPrice, setMaxPrice] = useState<string>(initialParams.get('max_price') || '');
  const [ordering, setOrdering] = useState<string>(initialParams.get('ordering') || '-created_at');
  const [currentPage, setCurrentPage] = useState<number>(parseInt(initialParams.get('page') || '1', 10));
  const [totalPages, setTotalPages] = useState<number>(1);

  // Product Detail Selection State
  const [selectedProduct, setSelectedProduct] = useState<Product | null>(null);
  const [isDetailModalOpen, setIsDetailModalOpen] = useState<boolean>(false);

  // Synchronize state with URL Query Params
  const updateUrlParams = useCallback((newParams: Record<string, string | number | null>) => {
    if (typeof window === 'undefined') return;
    const url = new URL(window.location.href);

    Object.entries(newParams).forEach(([key, value]) => {
      if (value === null || value === '' || (key === 'page' && value === 1) || (key === 'ordering' && value === '-created_at')) {
        url.searchParams.delete(key);
      } else {
        url.searchParams.set(key, String(value));
      }
    });

    window.history.pushState({}, '', url.toString());
  }, []);

  // Sync state changes to URL
  useEffect(() => {
    updateUrlParams({
      category: selectedCategory,
      search,
      min_price: minPrice,
      max_price: maxPrice,
      ordering,
      page: currentPage,
      product: selectedProduct ? selectedProduct.slug : null,
    });
  }, [selectedCategory, search, minPrice, maxPrice, ordering, currentPage, selectedProduct, updateUrlParams]);

  // Fetch Cart from Backend
  const loadCart = useCallback(async () => {
    if (!authClient.getToken()) {
      setCart(null);
      return;
    }
    setCartLoading(true);
    setCartError(null);
    try {
      const data = await cartClient.getCart();
      setCart(data);
    } catch (err: any) {
      setCartError(err.message || 'Failed to load shopping cart.');
    } finally {
      setCartLoading(false);
    }
  }, []);

  // Check current auth user on mount
  useEffect(() => {
    let isMounted = true;
    authClient.getCurrentUser().then((userData) => {
      if (isMounted && userData) {
        setCurrentUser(userData);
        loadCart();
      }
    });
    return () => {
      isMounted = false;
    };
  }, [loadCart]);

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

  // Handle deep-linked product detail via ?product=slug
  useEffect(() => {
    const productSlug = getUrlParams().get('product');
    if (productSlug && !selectedProduct) {
      catalogueClient
        .getProductBySlug(productSlug)
        .then((prod) => {
          setSelectedProduct(prod);
          setIsDetailModalOpen(true);
        })
        .catch((err) => {
          console.warn('Could not load deep-linked product:', err);
        });
    }
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

  const handleAddToCart = async (product: Product, quantity = 1) => {
    if (!currentUser) {
      setIsAuthModalOpen(true);
      return;
    }

    try {
      const updatedCart = await cartClient.addItem(product.id, quantity);
      setCart(updatedCart);
      setIsCartDrawerOpen(true);
    } catch (err: any) {
      alert(err.message || 'Could not add item to cart.');
    }
  };

  const handleUpdateCartQuantity = async (itemId: number, newQuantity: number) => {
    try {
      const updatedCart = await cartClient.updateItemQuantity(itemId, newQuantity);
      setCart(updatedCart);
    } catch (err: any) {
      alert(err.message || 'Could not update quantity.');
    }
  };

  const handleRemoveCartItem = async (itemId: number) => {
    try {
      const updatedCart = await cartClient.removeItem(itemId);
      setCart(updatedCart);
    } catch (err: any) {
      alert(err.message || 'Could not remove item.');
    }
  };

  const handleClearCart = async () => {
    if (!confirm('Are you sure you want to clear your cart?')) return;
    try {
      const updatedCart = await cartClient.clearCart();
      setCart(updatedCart);
    } catch (err: any) {
      alert(err.message || 'Could not clear cart.');
    }
  };

  const handleSelectProduct = (product: Product) => {
    setSelectedProduct(product);
    setIsDetailModalOpen(true);
  };

  const handleCloseDetailModal = () => {
    setIsDetailModalOpen(false);
    setSelectedProduct(null);
  };

  const handleAuthSuccess = (user: User, profile: Profile) => {
    setCurrentUser({ user, profile });
    loadCart();
  };

  const handleProfileUpdated = (updatedProfile: Profile) => {
    if (currentUser) {
      setCurrentUser({ user: currentUser.user, profile: updatedProfile });
    }
  };

  const handleLogout = async () => {
    await authClient.logout();
    setCurrentUser(null);
    setCart(null);
    setIsProfileModalOpen(false);
  };

  const hasActiveFilters =
    Boolean(selectedCategory) ||
    Boolean(search) ||
    Boolean(minPrice) ||
    Boolean(maxPrice) ||
    ordering !== '-created_at';

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Navbar
        cartCount={cart?.total_items || 0}
        currentUser={currentUser}
        onOpenAuthModal={() => setIsAuthModalOpen(true)}
        onOpenProfileModal={() => setIsProfileModalOpen(true)}
        onOpenCartDrawer={() => {
          if (!currentUser) {
            setIsAuthModalOpen(true);
          } else {
            setIsCartDrawerOpen(true);
          }
        }}
        onLogout={handleLogout}
      />
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
            <ProductGrid
              products={products}
              onAddToCart={(prod) => handleAddToCart(prod, 1)}
              onSelectProduct={handleSelectProduct}
            />
            <PaginationControls
              currentPage={currentPage}
              totalPages={totalPages}
              onPageChange={setCurrentPage}
            />
          </>
        )}
      </main>

      <Footer />

      {/* Cart Drawer Slide-out */}
      <CartDrawer
        isOpen={isCartDrawerOpen}
        onClose={() => setIsCartDrawerOpen(false)}
        cart={cart}
        loading={cartLoading}
        error={cartError}
        onUpdateQuantity={handleUpdateCartQuantity}
        onRemoveItem={handleRemoveCartItem}
        onClearCart={handleClearCart}
        onProceedToCheckout={() => alert('Proceeding to Checkout... (Orders Service Task)')}
      />

      {/* Product Detail Modal */}
      <ProductDetailModal
        product={selectedProduct}
        isOpen={isDetailModalOpen}
        onClose={handleCloseDetailModal}
        onAddToCart={handleAddToCart}
      />

      {/* Auth Modal */}
      <AuthModal
        isOpen={isAuthModalOpen}
        onClose={() => setIsAuthModalOpen(false)}
        onAuthSuccess={handleAuthSuccess}
      />

      {/* Profile Modal */}
      {currentUser && (
        <ProfileModal
          isOpen={isProfileModalOpen}
          onClose={() => setIsProfileModalOpen(false)}
          user={currentUser.user}
          profile={currentUser.profile}
          onProfileUpdated={handleProfileUpdated}
        />
      )}
    </div>
  );
};
