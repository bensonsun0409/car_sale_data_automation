import React, { useState } from "react";
import {
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Checkbox,
  ListItemText,
  OutlinedInput,
} from "@mui/material";

import brandsAndModels from "./brandsAndModes";

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

export default function Brand() {
  const [selectedBrands, setSelectedBrands] = useState([]);
  const [selectedModels, setSelectedModels] = useState([]);

  const handleBrandChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedBrands(typeof value === "string" ? value.split(",") : value);

    // Reset models when brands change
    setSelectedModels([]);
  };

  const handleModelChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedModels(typeof value === "string" ? value.split(",") : value);
  };

  const getModels = () => {
    if (!selectedBrands.length) return []; // If no brands selected, return empty array
    let models = [];
    selectedBrands.forEach((brand) => {
      models = [...models, ...(brandsAndModels[brand] || [])]; // Check if brand has models
    });
    return [...new Set(models)]; // Remove duplicates
  };

  return (
    <div>
      <FormControl sx={{ width: 250, marginBottom: 2 }}>
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
    </div>
  );
}
