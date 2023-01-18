import { Check } from "@mui/icons-material";
import { Paper } from "@mui/material";
import React from "react";
import Actor from "./Actor";

const AcceptFollow = ({ entry }) => {
  const actor = entry?.actor;

  return (
    <Paper
      sx={{ backgroundColor: "white", padding: 2, margin: 2 }}
      elevation={2}
    >
      <Check /> <Actor name={actor} /> accepted your follow request
    </Paper>
  );
};

export default AcceptFollow;
