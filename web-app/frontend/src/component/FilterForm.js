import React, { useState } from "react";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import dayjs from "dayjs";
import TextField from "@mui/material/TextField"; // 添加这一行
import "dayjs/locale/zh-cn";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Box from "@mui/material/Box";
const FilterForm = ({ onSearch }) => {
  const [startDate, setStartDate] = useState("");
  const [updateDate, setUpdateDate] = useState("");
  const [carBrand, setCarBrand] = useState("");
  const [productionYear, setProductionYear] = useState("");
  const [locale, setLocale] = React.useState("zh-cn");
  const handleSubmit = (event) => {
    event.preventDefault();
    const filters = {
      startDate,
      updateDate,
      ...(carBrand && { carBrand }),
      ...(productionYear && { productionYear }),
    };
    onSearch(filters);
  };
  const handleStartDate = (date) => {
    const selectedStartDate = date ? dayjs(date).format("YYYY/MM/DD") : "";
    setStartDate(selectedStartDate);
  };
  const handleUpdateDate = (date) => {
    const selectedUpdateDate = date ? dayjs(date).format("YYYY/MM/DD") : "";
    setUpdateDate(selectedUpdateDate);
  };
  const handleCarBrand = (e) => {
    const selectedCarBrand = e.target.value;
    setCarBrand(selectedCarBrand);
  };
  const handleProductYear = (date) => {
    const selectedProductYear = date ? dayjs(date).format("YYYY") : "";
    setProductionYear(selectedProductYear);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={locale}>
          <DemoContainer components={["DatePicker"]}>
            <DatePicker onChange={handleStartDate} required />
          </DemoContainer>
        </LocalizationProvider>
      </div>
      <div>
        <LocalizationProvider dateAdapter={AdapterDayjs} adapterLocale={locale}>
          <DemoContainer components={["DatePicker"]}>
            <DatePicker onChange={handleUpdateDate} required />
          </DemoContainer>
        </LocalizationProvider>
      </div>
      <div>
        <Box sx={{ minWidth: 120 }}>
          <FormControl>
            <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              onChange={handleCarBrand}
              sx={{ minWidth: 200 }}
            >
              <MenuItem value={"Toyota"}>Toyota</MenuItem>
              <MenuItem value={"Audi"}>Audi</MenuItem>
              <MenuItem value={"Ford"}>Ford</MenuItem>
            </Select>
          </FormControl>
        </Box>
      </div>
      <div>
        <label>出廠年份:</label>
        <LocalizationProvider dateAdapter={AdapterDayjs}>
          <DemoContainer components={["DatePicker"]}>
            <DatePicker
              views={["year"]}
              label="Year only"
              onChange={handleProductYear}
              openTo="year"
            />
          </DemoContainer>
        </LocalizationProvider>
      </div>
      <button type="submit">搜尋</button>
    </form>
  );
};

export default FilterForm;
