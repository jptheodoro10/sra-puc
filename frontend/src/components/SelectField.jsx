import React from "react";
import { FormControl, InputLabel, Select, MenuItem } from "@mui/material";

const toId = (str) => (str || "select").toLowerCase().replace(/\s+/g, "-");

const SelectField = ({
  label,
  value,
  onChange,
  options,
  required,
  sx,
  size = "small",
  fullWidth = true,
  hideLabel = false,
  selectSx,
}) => {
  const appliedLabel = hideLabel ? undefined : label;
  const labelId = hideLabel ? undefined : `${toId(label)}-label`;
  const selectId = `${toId(label)}-select`;
  return (
    <FormControl
      fullWidth={fullWidth}
      size={size}
      required={required}
      sx={{ mb: 2, ...sx }}
    >
      {!hideLabel && <InputLabel>{label}</InputLabel>}
      <Select
        id={selectId}
        labelId={labelId}
        label={appliedLabel}
        value={value}
        onChange={onChange}
        displayEmpty={hideLabel}
        sx={{ ...selectSx }}
      >
        {options.map((option, i) => (
          <MenuItem
            key={i}
            value={option}
            sx={{
              whiteSpace: "nowrap",
              overflow: "hidden",
              textOverflow: "ellipsis",
              boxSizing: "border-box",
            }}
          >
            {option}
          </MenuItem>
        ))}
      </Select>
    </FormControl>
  );
};

export default SelectField;
