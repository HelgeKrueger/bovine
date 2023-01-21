import { Divider, Link, Paper } from "@mui/material";
import React from "react";
import Actor from "./Actor";
import Attachments from "./Attachments";
import ReplyToNote from "./ReplyToNote";
import Source from "./Source";

const CreateNote = ({ entry }) => {
  return (
    <Paper
      sx={{ backgroundColor: "white", padding: 2, margin: 2 }}
      elevation={2}
    >
      <Actor name={entry?.actor} /> posted a{" "}
      <Link href={entry?.object?.id} target="_blank">
        Status
      </Link>{" "}
      at {entry?.object?.published}
      <Divider />
      <div dangerouslySetInnerHTML={{ __html: entry?.object?.content }} />
      <Attachments attachments={entry?.object?.attachment} />
      <ReplyToNote entry={entry} />
      <Source entry={entry} />
    </Paper>
  );
};

export default CreateNote;
