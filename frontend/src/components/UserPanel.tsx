import React, { useEffect, useState } from "react";

interface UserPanelProps {
  userID: number;
}

export const UserPanel: React.FC<UserPanelProps> = ({ userID }) => {
  const [avatarUrl, setAvatarUrl] = useState<string>("");

  useEffect(() => {
    const url = `https://api.dicebear.com/7.x/avataaars/svg?seed=${userID}&size=128&radius=50`;
    setAvatarUrl(url);
  }, [userID]);

  return (
    <div className="flex flex-col items-center gap-3">
      <div className="relative">
        {avatarUrl ? (
          <img
            src={avatarUrl}
            alt={`User ${userID} Avatar`}
            className="rounded-full w-28 h-28 border-3 border-gray-300 shadow-md"
            onError={(e) => {
              e.currentTarget.onerror = null;
              e.currentTarget.src = `data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128"><circle cx="64" cy="64" r="64" fill="%234f46e5"/><text x="64" y="72" font-family="Arial" font-size="48" fill="white" text-anchor="middle">U</text></svg>`;
            }}
          />
        ) : (
          <div className="w-28 h-28 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
            <span className="text-white text-3xl font-bold">U</span>
          </div>
        )}
      </div>
      <div className="text-center">
        <div className="text-xl font-bold text-white">UserID #{userID}</div>
      </div>
    </div>
  );
};