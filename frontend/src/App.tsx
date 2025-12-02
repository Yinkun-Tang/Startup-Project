import React, { useState, useEffect } from "react";
import { fetchRecommendations } from "./api/fetchRecommendations";
import type { RecommendationResponse } from "./api/fetchRecommendations";
import { UserPanel } from "./components/UserPanel";
import RecommendationList from "./components/RecommendationList";

export const App: React.FC = () => {
  const [data, setData] = useState<RecommendationResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [fade, setFade] = useState(true);

  const recommenderKeys = ["UserBasedCF", "ItemBasedCF", "ContentBased", "Hybrid"] as const;

  useEffect(() => {
    const loadRecommendations = async () => {
      setLoading(true);
      try {
        const res = await fetchRecommendations();
        setData(res);
      } catch (err) {
        console.error(err);
        alert("Failed to fetch recommendations");
      }
      setLoading(false);
    };
    loadRecommendations();
  }, []);

  if (loading || !data) return <div className="p-4 text-white">Loading...</div>;

  const nextRecommender = () => {
    setFade(false);
    setTimeout(() => {
      setCurrentIndex((prev) => (prev + 1) % recommenderKeys.length);
      setFade(true);
    }, 300);
  };

  const currentKey = recommenderKeys[currentIndex];

  const currentTitleMap = {
    UserBasedCF: "User-Based CF",
    ItemBasedCF: "Item-Based CF",
    ContentBased: "Content-Based",
    Hybrid: "Hybridization",
  } as const;

  const currentColorMap = {
    UserBasedCF: "text-blue-400",
    ItemBasedCF: "text-green-400",
    ContentBased: "text-purple-400",
    Hybrid: "text-yellow-400",
  } as const;

  return (
    <div className="page">
      <div className="flex bg-gray-900 w-[1000px] max-w-full h-[90vh]">
        <div className="w-[250px] bg-gray-800 border-r border-gray-700 flex flex-col items-center justify-center p-6">
          <UserPanel userID={data.UserID} />
        </div>

        <div className="flex-1 p-6 overflow-y-auto">
          <RecommendationList
            title={currentTitleMap[currentKey]}
            movies={data.Recommendations[currentKey]}
            onNext={nextRecommender}
            fading={fade}
            titleColor={currentColorMap[currentKey]}
          />
        </div>
      </div>
    </div>
  );
};

export default App;