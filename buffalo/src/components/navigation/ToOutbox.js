import React from "react";
import { Outbox } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import { useNavigate } from "react-router";

const ToOutbox = () => {
  const navigate = useNavigate();
  return (
    <IconButton
      onClick={() => {
        navigate("/outbox");
      }}
      color="primary"
    >
      <Outbox />
    </IconButton>
  );
};

export default ToOutbox;
