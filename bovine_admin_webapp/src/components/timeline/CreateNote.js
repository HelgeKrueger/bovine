import { Divider, Link, Paper } from "@mui/material";
import React from "react";
import Actor from "./Actor";
import Attachments from "./Attachments";
import ReplyToNote from "./ReplyToNote";
import Source from "./Source";

const CreateNote = ({ note, source }) => {
  return (
    <Paper
      sx={{ backgroundColor: "white", padding: 2, margin: 2 }}
      elevation={2}
    >
      <Actor name={note.attributedTo} /> posted a{" "}
      <Link href={note.id} target="_blank">
        Status
      </Link>{" "}
      at {note.published}
      <ReplyToNote entry={note} />
      <Source entry={source} />
      <Divider />
      <div dangerouslySetInnerHTML={{ __html: note.content }} />
      <Attachments attachments={note.attachment} />
    </Paper>
  );
};

export default CreateNote;
