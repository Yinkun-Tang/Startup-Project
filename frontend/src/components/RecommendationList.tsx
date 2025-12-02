import React from "react";
import type { MovieItem } from "../api/fetchRecommendations";

interface RecommendationListProps {
  title: string;
  movies: MovieItem[];
  onNext?: () => void;
  fading?: boolean;
  titleColor?: string;
}

const RecommendationList: React.FC<RecommendationListProps> = ({
  title,
  movies,
  onNext,
  fading = true,
  titleColor = "text-white",
}) => {
  return (
    <div
      className={`
        bg-gray-800 rounded-xl p-6 transition-opacity duration-300
        ${fading ? "opacity-100" : "opacity-0"}
      `}
    >
      <div className="flex justify-between items-center mb-4">
        <h2 className={`text-xl font-semibold ${titleColor}`}>
          {title}
        </h2>

        {onNext && (
          <button
            onClick={onNext}
            className="px-3 py-1 bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors text-sm"
          >
            Next Recommender
          </button>
        )}
      </div>

      <ul className="flex flex-wrap gap-4">
        {movies.map((movie) => (
          <li key={movie.MovieID} className="border p-2 rounded w-48 bg-gray-700 hover:bg-gray-600">
            <div className="font-medium">{movie.Title}</div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RecommendationList;
