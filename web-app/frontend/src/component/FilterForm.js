import React, { useState, useEffect } from "react";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import dayjs from "dayjs";
import TextField from "@mui/material/TextField"; // 添加这一行
import "dayjs/locale/zh-cn";
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
  OutlinedInput,
} from "@mui/material";
import FormControlLabel from "@mui/material/FormControlLabel";
import "../style/FilterForm.css";
import axios from "axios";

import { brandsAndModels, Colorlist } from "./brandsAndModes";
const FilterForm = ({ onSearch }) => {
  const [startDate, setStartDate] = useState("");
  const [updateDate, setUpdateDate] = useState("");

  const [locale, setLocale] = React.useState("zh-cn");
  const [selectedProductYear, setSelectedProductYear] = useState([]);
  const [productYear, setProductYear] = useState("");
  const [selectedTypeYear, setSelectedTypeYear] = useState([]);
  const [typeYear, setTypeYear] = useState("");
  const [selectedColor, setSelectedColor] = useState([]);
  const [color, setColor] = useState("");
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [carBrand, setCarBrand] = useState("");
  const [selectedModels, setSelectedModels] = useState([]);
  const [carModel, setCarModel] = useState("");
  const [yearOptions, setYearOptions] = useState([]);
  const [lowMilage, setLowMilage] = useState("");
  const [highMilage, setHighMilage] = useState("");
  const [videoCheck, setVideoCheck] = useState(false);
  const [video, setVideo] = useState("");
  const convertToUrlFormat = (name) => {
    return name.toLowerCase().replace(/\s+/g, "-");
  };
  const BooltoYN = (name) => {
    if (name == true) {
      return "Y";
    } else {
      return "";
    }
  };
  const handleSubmit = (event) => {
    event.preventDefault();
    const arrayToString = (arr) => {
      let strArr = "";
      if (arr != []) {
        arr.forEach(
          (element) => (strArr = strArr + convertToUrlFormat(element) + ",")
        );
        strArr = strArr.slice(0, -1);
      }
      return strArr;
    };

    setCarBrand(arrayToString(selectedBrands));
    setCarModel(arrayToString(selectedModels));
    setProductYear(arrayToString(selectedProductYear));
    setTypeYear(arrayToString(selectedTypeYear));
    setColor(arrayToString(selectedColor));
    setVideo(BooltoYN(videoCheck));

    const filters = {
      startDate,
      updateDate,
      ...(productYear && { productYear }),
      ...(typeYear && { typeYear }),
      ...(carBrand && { carBrand }),
      ...(carModel && { carModel }),
      ...(color && { color }),
      ...(lowMilage && { lowMilage }),
      ...(highMilage && { highMilage }),
      ...(video && { video }),
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

  useEffect(() => {
    const currentYear = new Date().getFullYear();
    const years = Array.from({ length: 41 }, (_, i) => currentYear - i);
    setYearOptions(years);
  }, []);

  const handleSelectedProductYear = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedProductYear(
      typeof value === "string" ? value.split(",") : value
    );
  };

  const handleSelectedTypeYear = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedTypeYear(typeof value === "string" ? value.split(",") : value);
  };

  const ITEM_HEIGHT = 48;
  const ITEM_PADDING_TOP = 8;
  const MenuProps = {
    PaperProps: {
      style: {
        maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
        width: 250,
      },
    },
  };

  const handleBrandChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedBrands(typeof value === "string" ? value.split(",") : value);

    setSelectedModels([]);
  };

  const handleModelChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedModels(typeof value === "string" ? value.split(",") : value);
  };
  const handleColorChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedColor(typeof value === "string" ? value.split(",") : value);
  };
  const getModels = () => {
    let models = [];
    selectedBrands.forEach((brand) => {
      models = [...models, ...brandsAndModels[brand]];
    });
    return [...new Set(models)]; // 移除重複的車型
  };
  const handleLowMilage = (event) => {
    setLowMilage(event.target.value);
  };
  const handleHighMilage = (event) => {
    setHighMilage(event.target.value);
  };
  const handleVideo = (event) => {
    setVideoCheck(event.target.value);
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="filter">
        <Box sx={{ maxWidth: 250, fontSize: 3 }}>
          <LocalizationProvider
            dateAdapter={AdapterDayjs}
            adapterLocale={locale}
          >
            <DemoContainer components={["DatePicker"]}>
              <DatePicker
                label="資料開始日期"
                onChange={handleStartDate}
                renderInput={(params) => (
                  <TextField
                    {...params}
                    sx={{
                      "& .MuiInputBase-input": {
                        fontSize: 12, // 调整输入框字体大小
                      },
                      "& .MuiInputLabel-root": {
                        fontSize: 12, // 调整标签字体大小
                      },
                      "& .MuiSvgIcon-root": {
                        fontSize: 20, // 调整图标大小（可选）
                      },
                    }}
                    required
                  />
                )}
              />
            </DemoContainer>
          </LocalizationProvider>
        </Box>

        <Box sx={{ maxWidth: 250 }}>
          <LocalizationProvider
            dateAdapter={AdapterDayjs}
            adapterLocale={locale}
          >
            <DemoContainer components={["DatePicker"]}>
              <DatePicker
                label="資料結束日期"
                onChange={handleUpdateDate}
                required
              />
            </DemoContainer>
          </LocalizationProvider>
        </Box>
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="year-select-label">出廠年份</InputLabel>
          <Select
            labelId="year-select-label"
            id="year-select"
            multiple
            value={selectedProductYear}
            onChange={handleSelectedProductYear}
            input={<OutlinedInput label="出廠年份" />}
            renderValue={(selected) => selected.join(", ")}
          >
            {yearOptions.map((year) => (
              <MenuItem key={year} value={year}>
                <Checkbox checked={selectedProductYear.indexOf(year) > -1} />
                <ListItemText primary={year} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="year-select-label">年式</InputLabel>
          <Select
            labelId="year-select-label"
            id="year-select"
            multiple
            value={selectedTypeYear}
            onChange={handleSelectedTypeYear}
            input={<OutlinedInput label="年式" />}
            renderValue={(selected) => selected.join(", ")}
          >
            {yearOptions.map((year) => (
              <MenuItem key={year} value={year}>
                <Checkbox checked={selectedTypeYear.indexOf(year) > -1} />
                <ListItemText primary={year} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="brand-select-label">品牌</InputLabel>
          <Select
            labelId="brand-select-label"
            id="brand-select"
            multiple
            value={selectedBrands}
            onChange={handleBrandChange}
            input={<OutlinedInput label="品牌" />}
            renderValue={(selected) => selected.join(", ")}
            MenuProps={MenuProps}
          >
            {Object.keys(brandsAndModels).map((brand) => (
              <MenuItem key={brand} value={brand}>
                <Checkbox checked={selectedBrands.indexOf(brand) > -1} />
                <ListItemText primary={brand} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="model-select-label">車型</InputLabel>
          <Select
            labelId="model-select-label"
            id="model-select"
            multiple
            value={selectedModels}
            onChange={handleModelChange}
            input={<OutlinedInput label="車型" />}
            renderValue={(selected) => selected.join(", ")}
            MenuProps={MenuProps}
          >
            {getModels().map((model) => (
              <MenuItem key={model} value={model}>
                <Checkbox checked={selectedModels.indexOf(model) > -1} />
                <ListItemText primary={model} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl sx={{ width: 250 }}>
          <InputLabel id="model-select-label" sx={{ fontSize: 15 }}>
            顏色
          </InputLabel>
          <Select
            labelId="model-select-label"
            id="model-select"
            multiple
            value={selectedColor}
            onChange={handleColorChange}
            input={<OutlinedInput label="顏色" />}
            renderValue={(selected) => selected.join(", ")}
            MenuProps={MenuProps}
          >
            {Colorlist.map((c) => (
              <MenuItem key={c} value={c}>
                <Checkbox checked={selectedColor.indexOf(c) > -1} />
                <ListItemText primary={c} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
      <div className="filter2">
        <div className="inputItem">
          <Box sx={{ width: "120px" }}>
            <TextField
              id="outlined-basic"
              label="最低里程"
              value={lowMilage}
              onChange={handleLowMilage}
            />
          </Box>
          <Box sx={{ width: "120px" }}>
            <TextField
              id="outlined-basic"
              label="最高里程"
              value={highMilage}
              onChange={handleHighMilage}
            />
          </Box>
        </div>
        <FormControlLabel
          control={<Checkbox />}
          checked={videoCheck}
          onChange={handleVideo}
          label="影片看車"
        />
      </div>
      <button type="submit">搜尋</button>
    </form>
  );
};

export default FilterForm;
