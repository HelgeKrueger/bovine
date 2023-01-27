import { Box } from "@mui/material";
import React from "react";
import { Outlet } from "react-router";
import { BrowserView, MobileView } from "react-device-detect";
const Main = () => {
  return (
    <>
      <BrowserView>
        <Box sx={{ maxWidth: "800px", marginLeft: "calc(50% - 400px)" }}>
          <Outlet />
        </Box>
      </BrowserView>
      <MobileView>
        <Outlet />
      </MobileView>
    </>
  );
};

export default Main;
