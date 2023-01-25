import { Box, CssBaseline } from "@mui/material";
import React from "react";
import ReactDOM from "react-dom/client";

import { Link, RouterProvider } from "react-router-dom";
import { DataUpdate } from "./helpers/DataUpdate";
import router from "./router";

const App = () => {
  return (
    <>
      <CssBaseline />
      <RouterProvider router={router} />
      <DataUpdate />
    </>
  );
};

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<App />);
