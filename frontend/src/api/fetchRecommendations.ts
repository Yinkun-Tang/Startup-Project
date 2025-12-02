export interface MovieItem {
  MovieID: number;
  Title: string;
  Genres: string;
}

export interface RecommendationResponse {
  UserID: number;
  Recommendations: {
    UserBasedCF: MovieItem[];
    ItemBasedCF: MovieItem[];
    ContentBased: MovieItem[];
    Hybrid: MovieItem[];
  };
}

export async function fetchRecommendations(): Promise<RecommendationResponse> {
  const response = await fetch(`http://127.0.0.1:8000/recommend?random_user=true`);
  if (!response.ok) {
    throw new Error("Failed to fetch recommendations");
  }
  return response.json();
}

