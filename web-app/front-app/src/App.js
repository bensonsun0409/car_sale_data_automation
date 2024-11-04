import React, { useState, useEffect } from "react";
import FilterForm from "./component/FilterForm";
import { Grid, Button } from "@mui/material";
import { styled } from "@mui/material/styles";
import Box from "@mui/material/Box";
import Paper from "@mui/material/Paper";
import "./App.css";
import Tabtable from "./component/Tabtable";

const App = () => {
  const [images, setImages] = useState({});
  const [error, setError] = useState(""); // 用于存储错误消息
  const [searched, setSearched] = useState(false); // 用于追踪用户是否进行了搜索
  const [loading, setLoading] = useState(false); // 用于追踪搜索请求的状态
  const [tableData, setTableData] = useState({});
  const imageTitles = {
    average_price: "平均價格",
    listing_count: "刊登數量",
    avg_views: "平均瀏覽數",
    avg_asknum: "平均諮詢數",
    avg_market_date: "平均上架天數",
  };
  
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
      setSearched(true); // 用户进行了搜索
      setLoading(true); // 搜索请求进行中
      const response = await fetch("http://localhost:3000/search", {
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
        const filteredImages = {};
        for (const [key, value] of Object.entries(data["images"])) {
          console.log(`Key: ${key}, Value: ${value}`); // 调试输出
          if (value) {
            filteredImages[key] = value;
          }
        }

        setImages(filteredImages); // 设置过滤后的 images
        console.log(data["tabledata"]["table_avg_price"])
        // 解析 tableData
        const parsedTableData = {
          price_all: data["tabledata"]["table_avg_price"] ? JSON.parse(data["tabledata"]["table_avg_price"]) : [],
          car_detail: data["tabledata"]["car_detail"] ? JSON.parse(data["tabledata"]["car_detail"]) : [],
          avg_ask_price: data["tabledata"]["avg_ask_price"] ? JSON.parse(data["tabledata"]["avg_ask_price"]) : [],
          avg_day_on_market: data["tabledata"]["avg_day_on_market"] ? JSON.parse(data["tabledata"]["avg_day_on_market"]) : [],
          seller_info: data["tabledata"]["seller_info"] ? JSON.parse(data["tabledata"]["seller_info"]) : []
        };
        // console.log(price_all)

        setTableData(parsedTableData); // 将解析后的数据存入 state
      } else {
        setImages({}); // 清空 images
        setError(data["message"] || "An error occurred."); // 设置错误消息
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setImages({}); // 清空 images
      setTableData({}); // 确保清空 tableData
      setError(error["message"] || "An error occurred.");
    } finally {
      setLoading(false); // 搜索请求结束
    }
  };

  const handleDownload = (base64Image, filename) => {
    const link = document.createElement("a");
    link.href = `data:image/png;base64,${base64Image}`;
    link.download = `${filename}.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const hasImages = Object.keys(images).length > 0;

  useEffect(() => {
    if (searched && !loading && !hasImages && !error) {
      setError("沒有資料");
    }
  }, [searched, loading, hasImages, error]);

  return (
    <div>
      <header>
        <h1 className="title">8891報表</h1>
        <hr />
      </header>
      <main>
        <FilterForm onSearch={handleSearch} />
        {error && <div className="error-message">{error}</div>} {/* 显示错误消息 */}
        {loading && <div className="loading-message">Loading...</div>} {/* 显示加载消息 */}
        {!loading && searched && !hasImages && !error && (
          <div className="no-data-message">沒有資料</div> // 显示“沒有資料”
        )}
        {hasImages && (
          <Grid container spacing={2}>
            {Object.keys(images).map((key, index) => (
              
              <Grid item xs={12} sm={6} md={4} key={index}>
               <h3>{imageTitles[key] || key}</h3>
                <Box sx={{ maxWidth: "100%" }}>
                  <img
                    src={`data:image/png;base64,${images[key]}`}
                    alt={key}
                    className="outputImg"
                    style={{ maxWidth: "100%", height: "auto" }}
                  />
                </Box>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={() => handleDownload(images[key], key)}
                  style={{ marginTop: "10px" }}
                >
                  下載圖片
                </Button>
              </Grid>
            ))}
          </Grid>
        )}
      </main>
      <div>
        <Tabtable tableData={tableData} /> {/* 将整个 tableData 传递 */}
      </div>
    </div>
  );
};

export default App;
