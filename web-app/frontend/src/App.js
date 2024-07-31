import React, { useState } from "react";
import FilterForm from "./component/FilterForm";

const App = () => {
  const [images, setImages] = useState({});
  const [results, setResults] = useState([]);
  const handleSearch = async (filters) => {
    try {
      const response = await fetch("http://localhost:5000/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(filters),
      });
      if (!response.ok) {
        throw new Error("Network response was not ok.");
      }

      const data = await response.json();
      // 现在 data 是你的 JSON 数据对象，你可以从中提取 image 属性
      setImages(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div>
      <FilterForm onSearch={handleSearch} />
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
