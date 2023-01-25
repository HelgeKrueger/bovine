import { QuestionMark } from "@mui/icons-material";
import { Link, Paper } from "@mui/material";
import React from "react";
import Actor from "./Actor";

const UpdateQuestion = ({ entry }) => {
  const { actor, object } = entry;

  return (
    <Paper
      sx={{ backgroundColor: "white", padding: 2, margin: 2 }}
      elevation={2}
    >
      <QuestionMark />
      <Actor name={actor} />
      's{" "}
      <Link href={object?.id} target="_blank">
        Question
      </Link>{" "}
      has been updated
    </Paper>
  );
};

export default UpdateQuestion;
