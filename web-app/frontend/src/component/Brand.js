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

    setSelectedModels([]);
  };

  const handleModelChange = (event) => {
    const {
      target: { value },
    } = event;
    setSelectedModels(typeof value === "string" ? value.split(",") : value);
  };
  const getModels = () => {
    let models = [];
    selectedBrands.forEach((brand) => {
      models = [...models, ...brandsAndModels[brand]];
    });
    return [...new Set(models)]; // 移除重複的車型
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

// const names = {
//   "Alfa Romeo":["156","159","4C","Brera","GIULIA","Giulietta","Mito","Spider","Stelvio"],
//   "Aston Martin":["DB11","DB7","DB9","DBS","DBX","Rapide","V8 Vantage","Vanquish","Vantage","Virage"],
//   "Audi":["A1","A1 Sportback","A3 5D","A3 Sedan","A3 Sportback","A4 Allroad","A4 Avant","A4 Sedan","A5","A5 Coupe","A5 Sportback","A6 Allroad",
//     "A6 Avant","A6 Sedan","A7","A7",
//   ],
//   "Austin",
//   "Abarth",
//   "Bentley",
//   "BMW",
//   "BRABUS",
//   "Citroen/雪鐵龍",
//   "Ferrai/法拉利",
//   "Fiat",
//   "Infiniti",
//   "Jaguar",
//   "Jeep/吉普",
//   "Lamborghini/藍寶堅尼",
//   "Land Rover",
//   "Lexus",
//   "Lotus/蓮花",
//   "Mercedes-Benz/賓士",
//   "Maserati/瑪莎拉蒂",
//   "Mini",
//   "McLaren/麥拉倫",
//   "Opel/歐寶",
//   "Peugeot",
//   "Porsche/保時捷",
//   "Rolls-Royce/勞斯萊斯",
//   "Skoda",
//   "Smart",
//   "Tesla/特斯拉",
//   "Volvo",
//   "Toyota",
//   "Nissan",
//   "Mitsubishi",
//   "VW",
// };

// export default function Brand() {
//   const [personName, setPersonName] = React.useState([]);

//   const handleChange = (event) => {
//     const {
//       target: { value },
//     } = event;
//     setPersonName(
//       // On autofill we get a stringified value.
//       typeof value === "string" ? value.split(",") : value
//     );
//   };

//   return (
//     <div>
//       <FormControl sx={{ width: 250 }}>
//         <InputLabel id="demo-multiple-checkbox-label">品牌</InputLabel>
//         <Select
//           labelId="demo-multiple-checkbox-label"
//           id="demo-multiple-checkbox"
//           multiple
//           value={personName}
//           onChange={handleChange}
//           input={<OutlinedInput label="Tag" />}
//           renderValue={(selected) => selected.join(", ")}
//           MenuProps={MenuProps}
//         >
//           {names.map((name) => (
//             <MenuItem key={name} value={name}>
//               <Checkbox checked={personName.indexOf(name) > -1} />
//               <ListItemText primary={name} />
//             </MenuItem>
//           ))}

//         </Select>
//       </FormControl>
//       <FormControl sx={{ width: 250 }}>
//         <InputLabel id="demo-multiple-checkbox-label">車型</InputLabel>
//         <Select
//           labelId="demo-multiple-checkbox-label"
//           id="demo-multiple-checkbox"
//           multiple
//           value={personName}
//           onChange={handleChange}
//           input={<OutlinedInput label="Tag" />}
//           renderValue={(selected) => selected.join(", ")}
//           MenuProps={MenuProps}
//         >
//           {names.map((name) => (
//             <MenuItem key={name} value={name}>
//               <Checkbox checked={personName.indexOf(name) > -1} />
//               <ListItemText primary={name} />
//             </MenuItem>
//           ))}

//         </Select>
//       </FormControl>
//     </div>
//   );
// }
