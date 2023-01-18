import { Box, Toolbar } from "@mui/material";
import React from "react";
import { Outlet } from "react-router";
import { Link } from "react-router-dom";
import Sidebar from "../components/Sidebar";

const Main = () => {
  return (
    <Box sx={{ display: "flex" }}>
      <Sidebar />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <h1 style={{ textAlign: "center" }}>My Math Rocks: Administration</h1>
        <Outlet />
      </Box>
    </Box>
  );
};

export default Main;
