import React, { useState } from "react";
import FilterForm from "./component/FilterForm";

const App = () => {
  const [images, setImages] = useState({});
  const [error, setError] = useState(""); // 用于存储错误消息

  const handleSearch = async (filters) => {
    try {
      setError(""); // 在每次搜索前清空错误消息
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(filters),
      });
      if (!response.ok) {
        throw new Error("無效輸入/連線失敗");
      }

      const data = await response.json();
      if (data["success"]) {
        setImages(data["images"]); // 只设置 images 字段
      } else {
        setImages({}); // 清空 images
        setError(data["message"] || "An error occurred.123"); // 设置错误消息
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setImages({}); // 清空 images
      setError(error["message"] || "An error occurred.");
    }
  };

  return (
    <div>
      <FilterForm onSearch={handleSearch} />
      {error && <div className="error-message">{error}</div>}{" "}
      {/* 显示错误消息 */}
      <div>
        {Object.entries(images).map(([key, img]) => (
          <div key={key}>
            <h3>{key}</h3>
            <img
              src={`data:image/png;base64,${img}`}
              alt={key}
              className="outputImg"
            />
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
