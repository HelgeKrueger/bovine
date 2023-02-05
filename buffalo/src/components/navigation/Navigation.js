import React, { useContext } from "react";
import { Box, IconButton } from "@mui/material";

import { Message } from "@mui/icons-material";
import { DataUpdate } from "../DataUpdate";
import UnreadCountBadge from "../UnreadCountBadge";
import AllRead from "./AllRead";
import ToPost from "./ToPost";
import ToSketch from "./ToSketch";
import ToFetch from "./ToFetch";

import { EntryContext } from "../../pages/Main";
import { useNavigate } from "react-router";

const Navigation = () => {
  const { updateEntry } = useContext(EntryContext);

  const navigate = useNavigate();

  const handleMessageClick = () => {
    updateEntry();
    navigate("/");
  };
  return (
    <Box
      sx={{
        backgroundColor: "white",
        paddingTop: 1,
        display: "flex",
      }}
    >
      <AllRead />
      <ToPost />
      <ToSketch />
      <ToFetch />
      <DataUpdate />
      <IconButton onClick={handleMessageClick} color="primary">
        <UnreadCountBadge>
          <Message />
        </UnreadCountBadge>
      </IconButton>
    </Box>
  );
};

export default Navigation;
