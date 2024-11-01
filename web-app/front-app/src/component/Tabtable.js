import React, { useState } from 'react';
import { Tabs, Tab, Box, Typography } from '@mui/material';
import Allcardetail from './Allcardetail';
// 假設的表格組件，您需要根據實際需求實現這些組件
const AverageDaysListedTable = () => <Typography>平均上架天數報表內容</Typography>;
const AveragePriceTable = () => <Typography>平均報價報表內容</Typography>;
const QuotationTable = () => <Allcardetail/>
const CarConditionTable = () => <Typography>車況總表報表內容</Typography>;
const UsedCarDealerTable = () => <Typography>中古車商內容</Typography>;

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

export const Tabtable = ({ tableData }) => {
  const [value, setValue] = useState(0);
  console.log('Tabtable 接收到的 tableData:', tableData); // 調試日志

  const handleChange = (event, newValue) => {
    setValue(newValue);
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
        <AverageDaysListedTable />
      </TabPanel>
      <TabPanel value={value} index={1}>
        <AveragePriceTable />
      </TabPanel>
      <TabPanel value={value} index={2}>
        <Allcardetail tableData={tableData} />
      </TabPanel>
      <TabPanel value={value} index={3}>
        <CarConditionTable />
      </TabPanel>
      <TabPanel value={value} index={4}>
        <UsedCarDealerTable />
      </TabPanel>
    </Box>
  );
};