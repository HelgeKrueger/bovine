import React from "react";
import { Search } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import { useNavigate } from "react-router";

const ToFetch = () => {
  const navigate = useNavigate();
  return (
    <IconButton
      onClick={() => {
        navigate("/fetch");
      }}
      color="primary"
    >
      <Search />
    </IconButton>
  );
};

export default ToFetch;
