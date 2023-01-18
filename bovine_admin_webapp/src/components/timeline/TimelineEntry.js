import { Paper } from "@mui/material";
import React from "react";
import AcceptFollow from "./AcceptFollow";
import Announce from "./Announce";
import CreateNote from "./CreateNote";
import UpdateQuestion from "./UpdateQuestion";

const TimelineEntry = ({ entry }) => {
  if (entry?.type === "Accept" && entry?.object?.type === "Follow") {
    return <AcceptFollow entry={entry} />;
  }

  if (entry?.type === "Create" && entry?.object?.type === "Note") {
    return <CreateNote entry={entry} />;
  }

  if (entry?.type === "Announce") {
    return <Announce entry={entry} />;
  }

  if (entry?.type === "Update" && entry?.object?.type === "Question") {
    return <UpdateQuestion entry={entry} />;
  }

  const text = JSON.stringify(entry, null, 2);

  return (
    <Paper
      sx={{ backgroundColor: "white", padding: 2, margin: 2 }}
      elevation={2}
    >
      <pre>{text}</pre>
    </Paper>
  );
};

export default TimelineEntry;
