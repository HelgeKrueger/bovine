import { Box, Paper } from "@mui/material";
import React from "react";
import Follow from "./actions/Follow";
import Source from "./Source";

const Person = ({ entry }) => {
  return (
    <Paper
      sx={{ backgroundColor: "white", padding: 2, margin: 2 }}
      elevation={2}
    >
      <Box sx={{ backgroundColor: "#cccccc", padding: 1 }}>
        <b>Name:</b> {entry?.name} <br />
        <b>Username:</b> {entry?.preferredUsername}
      </Box>
      <div dangerouslySetInnerHTML={{ __html: entry?.summary }} />
      <Follow actor={entry} />
      <Source entry={entry} />
    </Paper>
  );
};

export default Person;
