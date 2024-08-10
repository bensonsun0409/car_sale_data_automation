import React, { useState } from "react";
import FilterForm from "./component/FilterForm";
import { Grid } from "@mui/material";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import "./App.css";
const App = () => {
  const [images, setImages] = useState({});
  const [error, setError] = useState(""); // 用于存储错误消息
  const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === "dark" ? "#1A2027" : "#fff",
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: "center",
    color: theme.palette.text.secondary,
  }));

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
  const hasImages = Object.keys(images).length > 0;
  return (
    <div>
      <header>
        <h1 className="title">8891報表</h1>
        <hr />
      </header>
      <body>
        <FilterForm onSearch={handleSearch} />
        {error && <div className="error-message">{error}</div>}{" "}
        {/* 显示错误消息 */}
        {hasImages && (
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <h3>{Object.keys(images)[0]}</h3>
              <Box sx={{ maxWidth: "30%" }}>
                <img
                  src={`data:image/png;base64,${Object.values(images)[0]}`}
                  alt={Object.keys(images)[0]}
                  className="outputImg"
                  sx={{
                    maxWidth: "80%",
                    maxHeight: "80%",
                    objectFit: "contain",
                  }}
                />
              </Box>
            </Grid>
            <Grid item xs={4}>
              <h3>{Object.keys(images)[1]}</h3>
              <Box sx={{ maxWidth: "30%" }}>
                <img
                  src={`data:image/png;base64,${Object.values(images)[1]}`}
                  alt={Object.keys(images)[1]}
                  className="outputImg"
                  sx={{
                    maxWidth: "100%",
                    maxHeight: "100%",
                    objectFit: "contain",
                  }}
                />
              </Box>
            </Grid>
            <Grid item xs={4}>
              <h3>{Object.keys(images)[2]}</h3>
              <Box sx={{ maxWidth: "30%" }}>
                <img
                  src={`data:image/png;base64,${Object.values(images)[2]}`}
                  alt={Object.keys(images)[2]}
                  className="outputImg"
                  sx={{
                    maxWidth: "100%",
                    maxHeight: "100%",
                    objectFit: "contain",
                  }}
                />
              </Box>
            </Grid>
            <Grid
              item
              xs={6}
              style={{
                textAlign: "center",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <h3>{Object.keys(images)[3]}</h3>
              <Box sx={{ maxWidth: "30%" }}>
                <img
                  src={`data:image/png;base64,${Object.values(images)[3]}`}
                  alt={Object.keys(images)[3]}
                  className="outputImg"
                  sx={{
                    maxWidth: "100%",
                    maxHeight: "100%",
                    objectFit: "contain",
                  }}
                />
              </Box>
            </Grid>
            <Grid item xs={6}>
              <h3>{Object.keys(images)[4]}</h3>
              <Box sx={{ maxWidth: "30%" }}>
                <img
                  src={`data:image/png;base64,${Object.values(images)[4]}`}
                  alt={Object.keys(images)[4]}
                  className="outputImg"
                  sx={{
                    maxWidth: "100%",
                    maxHeight: "100%",
                    objectFit: "contain",
                  }}
                />
              </Box>
            </Grid>
          </Grid>
        )}
      </body>
    </div>
  );
};

export default App;
