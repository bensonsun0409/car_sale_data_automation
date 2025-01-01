import React, { useState } from 'react';
import { Tabs, Tab, Box, Button } from '@mui/material';
import Allcardetail from './Allcardetail';

const TabPanel = (props) => {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
};

const Tabtable = ({ tableData }) => {
  const [value, setValue] = useState(0);

  const price_all = tableData.price_all || [];
  const car_detail = tableData.car_detail || [];
  const avg_ask_price = tableData.avg_ask_price || [];
  const avg_day_on_market = tableData.avg_day_on_market || [];
  const seller_info = tableData.seller_info || [];

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  // CSV 导出功能
  const exportToCSV = (data, filename) => {
    let csvContent = "\uFEFF"; // 添加BOM头来解决Excel乱码问题

    if (data.length > 0) {
      // 添加列标题
      csvContent += Object.keys(data[0]).join(",") + "\n";

      // 添加每行数据
      data.forEach(row => {
        csvContent += Object.values(row).join(",") + "\n";
      });
    } else {
      csvContent += "No data available\n";
    }

    // 创建下载链接并自动点击下载
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `${filename}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={value} onChange={handleChange} aria-label="table tabs">
          <Tab label="平均上架天數報表" />
          <Tab label="平均報價報表" />
          <Tab label="報價報表" />
          <Tab label="車況總表報表" />
          <Tab label="中古車商" />
        </Tabs>
      </Box>
      <TabPanel value={value} index={0}>
        <Allcardetail tableData={avg_day_on_market} />
        <Button variant="contained" color="primary" onClick={() => exportToCSV(avg_day_on_market, "平均上架天數報表")}>
          下載 CSV
        </Button>
      </TabPanel>
      <TabPanel value={value} index={1}>
        <Allcardetail tableData={price_all} />
        <Button variant="contained" color="primary" onClick={() => exportToCSV(price_all, "平均報價報表")}>
          下載 CSV
        </Button>
      </TabPanel>
      <TabPanel value={value} index={2}>
        <Allcardetail tableData={avg_ask_price} />
        <Button variant="contained" color="primary" onClick={() => exportToCSV(avg_ask_price, "報價報表")}>
          下載 CSV
        </Button>
      </TabPanel>
      <TabPanel value={value} index={3}>
        <Allcardetail tableData={car_detail} />
        <Button variant="contained" color="primary" onClick={() => exportToCSV(car_detail, "車況總表報表")}>
          下載 CSV
        </Button>
      </TabPanel>
      <TabPanel value={value} index={4}>
        <Allcardetail tableData={seller_info} />
        <Button variant="contained" color="primary" onClick={() => exportToCSV(seller_info, "中古車商")}>
          下載 CSV
        </Button>
      </TabPanel>
    </Box>
  );
};

export default Tabtable;
