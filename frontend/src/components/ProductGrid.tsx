import React from 'react';
import type { Product } from '../types/catalogue';
import { ProductCard } from './ProductCard';

interface ProductGridProps {
  products: Product[];
  wishlistProductIds?: Set<number>;
  onAddToCart?: (product: Product) => void;
  onToggleWishlist?: (product: Product) => void;
  onSelectProduct?: (product: Product) => void;
}

export const ProductGrid: React.FC<ProductGridProps> = ({
  products,
  wishlistProductIds,
  onAddToCart,
  onToggleWishlist,
  onSelectProduct,
}) => {
  return (
    <div className="products-grid" id="products-grid">
      {products.map((product) => (
        <ProductCard
          key={product.id}
          product={product}
          isWishlisted={wishlistProductIds ? wishlistProductIds.has(product.id) : false}
          onAddToCart={onAddToCart}
          onToggleWishlist={onToggleWishlist}
          onSelectProduct={onSelectProduct}
        />
      ))}
    </div>
  );
};

