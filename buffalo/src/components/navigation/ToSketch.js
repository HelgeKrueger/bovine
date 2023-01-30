import React from "react";
import { Brush } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import { useNavigate } from "react-router";

const ToSketch = () => {
  const navigate = useNavigate();
  return (
    <IconButton
      onClick={() => {
        navigate("/sketch");
      }}
      color="primary"
    >
      <Brush />
    </IconButton>
  );
};

export default ToSketch;
