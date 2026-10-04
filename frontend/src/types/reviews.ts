export interface Review {
  id: number;
  username: string;
  product_id: number;
  rating: number;
  title: string;
  comment: string;
  is_approved: boolean;
  created_at: string;
}

export interface ReviewSummaryResponse {
  product_id: number;
  average_rating: number;
  total_reviews: number;
  rating_distribution: Record<string, number>;
  reviews: Review[];
}
