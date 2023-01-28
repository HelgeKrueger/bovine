import { Paper } from "@mui/material";
import React, { useEffect } from "react";
import AcceptFollow from "./AcceptFollow";
import Announce from "./Announce";
import CreateNote from "./CreateNote";
import UpdateQuestion from "./UpdateQuestion";
import { db } from "../../database";

const TimelineEntry = ({ entry, seen }) => {
  useEffect(() => {
    if (entry?.id) {
      db.activity.update(entry["id"], { displayed: 1 });
    }
  }, [entry]);

  if (entry?.type === "Accept" && entry?.object?.type === "Follow") {
    return <AcceptFollow entry={entry} />;
  }

  if (entry?.type === "Create" && entry?.object?.type === "Note") {
    return <CreateNote note={entry?.object} source={entry} seen={seen} />;
  }
  if (entry?.type === "Note") {
    return <CreateNote note={entry} source={entry} seen={seen} />;
  }

  if (entry?.type === "Announce") {
    return <Announce entry={entry} />;
  }

  if (entry?.type === "Update" && entry?.object?.type === "Question") {
    return <UpdateQuestion entry={entry} />;
  }

  const text = JSON.stringify(entry, null, 2);

  return (
    <Paper sx={{ backgroundColor: "white" }} elevation={2}>
      <pre>{text}</pre>
    </Paper>
  );
};

export default TimelineEntry;
