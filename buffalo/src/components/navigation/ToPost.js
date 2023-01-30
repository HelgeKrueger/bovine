import React from "react";
import { Create } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import { useNavigate } from "react-router";

const ToPost = () => {
  const navigate = useNavigate();
  return (
    <IconButton
      onClick={() => {
        navigate("/post");
      }}
      color="primary"
    >
      <Create />
    </IconButton>
  );
};

export default ToPost;
