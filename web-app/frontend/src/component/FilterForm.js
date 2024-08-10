import React, { useState, useEffect } from "react";
import { DemoContainer } from "@mui/x-date-pickers/internals/demo";
import { AdapterDayjs } from "@mui/x-date-pickers/AdapterDayjs";
import { LocalizationProvider } from "@mui/x-date-pickers/LocalizationProvider";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import dayjs from "dayjs";
import TextField from "@mui/material/TextField"; // 添加这一行
import "dayjs/locale/zh-cn";
import Fuse from "fuse.js";
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
  OutlinedInput,
  Button,
} from "@mui/material";
import FormControlLabel from "@mui/material/FormControlLabel";
import "../style/FilterForm.css";
import axios from "axios";
import {
  brandsAndModels,
  Colorlist,
  Equiplist,
  Locationlist,
} from "./brandsAndModes";

const FilterForm = ({ onSearch }) => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");

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
  const [verifyCheck, setVerifyCheck] = useState(false);
  const [verify, setVerify] = useState("");
  const [selectedEquip, setSelectedEquip] = useState([]);
  const [selectedCity, setSelectedCity] = useState([]);
  const [city, setCity] = useState("");
  const [selectedLoc, setSelectedLoc] = useState([]);
  const [loc, setLoc] = useState("");
  const [lowView, setLowView] = useState("");
  const [highView, setHighView] = useState("");
  const [lowAsknum, setLowAsknum] = useState("");
  const [highAsknum, setHighAsknum] = useState("");
  const [seller, setSeller] = useState("");

  const convertToUrlFormat = (name) => {
    return name.toLowerCase().replace(/\s+/g, "-");
  };
  const BooltoYN = (name) => (name ? "Y" : "");
  const arrayToString2 = (arr) => {
    if (arr.length > 0) {
      const strArr = arr.map((element) => `"${element}"`).join(", ");
      return strArr;
    }
    return "";
  };
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
  const handleSubmit = (event) => {
    event.preventDefault();

    // setCity(arrayToString2(selectedCity));
    // console.log(city);
    // setLoc(arrayToString2(selectedLoc));
    const filters = {
      startDate,
      endDate,
      ...(productYear && { productYear }),
      ...(typeYear && { typeYear }),
      ...(carBrand && { carBrand }),
      ...(selectedBrands && { selectedBrands }),
      ...(carModel && { carModel }),
      ...(color && { color }),
      ...(lowMilage && { lowMilage }),
      ...(highMilage && { highMilage }),
      ...(video && { video }),
      ...(verify && { verify }),
      ...(selectedEquip && { selectedEquip }),
      ...(city && { city }),
      ...(loc && { loc }),
      ...(lowView && { lowView }),
      ...(highView && { highView }),
      ...(lowAsknum && { lowAsknum }),
      ...(highAsknum && { highAsknum }),
      ...(seller && { seller }),
    };
    onSearch(filters);
  };
  const handleStartDate = (date) => {
    const selectedStartDate = date ? dayjs(date).format("YYYY/MM/DD") : "";
    setStartDate(selectedStartDate);
  };
  const handleEndDate = (date) => {
    const selectedEndDate = date ? dayjs(date).format("YYYY/MM/DD") : "";
    setEndDate(selectedEndDate);
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
  useEffect(() => {
    setProductYear(arrayToString2(selectedProductYear));
  }, [selectedProductYear]);
  const handleSelectedTypeYear = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedTypeYear(typeof value === "string" ? value.split(",") : value);
  };
  useEffect(() => {
    setTypeYear(arrayToString2(selectedTypeYear));
  }, [selectedTypeYear]);
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
  useEffect(() => {
    setCarBrand(arrayToString2(selectedBrands));
  }, [selectedBrands]);
  const handleModelChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedModels(typeof value === "string" ? value.split(",") : value);
  };
  useEffect(() => {
    setCarModel(arrayToString(selectedModels));
  }, [selectedModels]);
  const handleColorChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedColor(typeof value === "string" ? value.split(",") : value);
  };
  useEffect(() => {
    setColor(arrayToString2(selectedColor));
  }, [selectedColor]);
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
  const handleVideoCheck = (event) => {
    const checked = event.target.checked;
    setVideoCheck(checked);
  };
  useEffect(() => {
    setVideo(BooltoYN(videoCheck));
  }, [videoCheck]);

  const handleVerifyCheck = (event) => {
    const checked = event.target.checked;
    setVerifyCheck(checked);
  };
  useEffect(() => {
    setVerify(BooltoYN(verifyCheck));
  }, [verifyCheck]);

  const handleEquipChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedEquip(typeof value === "string" ? value.split(",") : value);
  };
  const handleCityChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedCity(typeof value === "string" ? value.split(",") : value);

    setSelectedLoc([]);
  };
  useEffect(() => {
    setCity(arrayToString2(selectedCity));
  }, [selectedCity]);

  const handleLocChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedLoc(typeof value === "string" ? value.split(",") : value);
  };
  useEffect(() => {
    setLoc(arrayToString2(selectedLoc));
  }, [selectedLoc]);

  const getLoc = () => {
    let location = [];
    selectedCity.forEach((city) => {
      location = [...location, ...Locationlist[city]];
    });
    return [...new Set(location)]; // 移除重複的車型
  };

  const handleLowView = (event) => {
    setLowView(event.target.value);
  };
  const handleHighView = (event) => {
    setHighView(event.target.value);
  };
  const handleLowAsknum = (event) => {
    setLowAsknum(event.target.value);
  };
  const handleHighAsknum = (event) => {
    setHighAsknum(event.target.value);
  };

  const handleSeller = (event) => {
    setSeller(event.target.value);
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
                onChange={handleEndDate}
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
        <Box sx={{ width: "250px" }}>
          <FormControlLabel
            control={
              <Checkbox checked={videoCheck} onChange={handleVideoCheck} />
            }
            label="影片看車"
          />
        </Box>
        <Box sx={{ width: "250px" }}>
          <FormControlLabel
            control={
              <Checkbox checked={verifyCheck} onChange={handleVerifyCheck} />
            }
            label="第三方鑑定"
          />
        </Box>
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="model-select-label" sx={{ fontSize: 15 }}>
            配備
          </InputLabel>
          <Select
            labelId="model-select-label"
            id="model-select"
            multiple
            value={selectedEquip}
            onChange={handleEquipChange}
            input={<OutlinedInput label="配備" />}
            renderValue={(selected) => selected.join(", ")}
            MenuProps={MenuProps}
          >
            {Equiplist.map((c) => (
              <MenuItem key={c} value={c}>
                <Checkbox checked={selectedEquip.indexOf(c) > -1} />
                <ListItemText primary={c} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="city-select-label">縣市</InputLabel>
          <Select
            labelId="city-select-label"
            id="city-select"
            multiple
            value={selectedCity}
            onChange={handleCityChange}
            input={<OutlinedInput label="縣市" />}
            renderValue={(selected) => selected.join(", ")}
            MenuProps={MenuProps}
          >
            {Object.keys(Locationlist).map((city) => (
              <MenuItem key={city} value={city}>
                <Checkbox checked={selectedCity.indexOf(city) > -1} />
                <ListItemText primary={city} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl sx={{ width: 250 }}>
          <InputLabel id="loc-select-label">區域</InputLabel>
          <Select
            labelId="loc-select-label"
            id="loc-select"
            multiple
            value={selectedLoc}
            onChange={handleLocChange}
            input={<OutlinedInput label="區域" />}
            renderValue={(selected) => selected.join(", ")}
            MenuProps={MenuProps}
          >
            {getLoc().map((loc) => (
              <MenuItem key={loc} value={loc}>
                <Checkbox checked={selectedLoc.indexOf(loc) > -1} />
                <ListItemText primary={loc} />
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <div className="inputItem">
          <Box sx={{ width: "120px" }}>
            <TextField
              id="outlined-basic"
              label="最低瀏覽"
              value={lowView}
              onChange={handleLowView}
            />
          </Box>
          <Box sx={{ width: "120px" }}>
            <TextField
              id="outlined-basic"
              label="最高瀏覽"
              value={highView}
              onChange={handleHighView}
            />
          </Box>
        </div>
      </div>
      <div className="filter2">
        <div className="inputItem">
          <Box sx={{ width: "120px" }}>
            <TextField
              id="outlined-basic"
              label="最低諮詢"
              value={lowAsknum}
              onChange={handleLowAsknum}
            />
          </Box>
          <Box sx={{ width: "120px" }}>
            <TextField
              id="outlined-basic"
              label="最高諮詢"
              value={highAsknum}
              onChange={handleHighAsknum}
            />
          </Box>
        </div>
        <Box sx={{ width: "400px" }}>
          <TextField
            id="outlined-basic"
            label="車商搜尋"
            value={seller}
            onChange={handleSeller}
          />
        </Box>
      </div>
      <Button variant="contained" type="Submit">
        搜尋
      </Button>
    </form>
  );
};

export default FilterForm;
