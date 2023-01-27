import { Expand, ExpandMore } from "@mui/icons-material";
import { Divider, Link, Paper, Button } from "@mui/material";
import React, { useEffect, useState } from "react";
import Actor from "./Actor";
import Attachments from "./Attachments";
import ReplyToNote from "./ReplyToNote";
import Source from "./Source";

const NoteContent = ({ collapse, note }) => {
  if (collapse) {
    return <></>;
  }

  return (
    <>
      <Divider />
      <div dangerouslySetInnerHTML={{ __html: note.content }} />
      <Attachments attachments={note.attachment} />
    </>
  );
};

const CreateNote = ({ note, source, seen }) => {
  const [collapse, setCollapse] = useState(seen === 1);
  useEffect(() => {
    setCollapse(seen === 1);
  }, [note, seen]);
  if (collapse) {
    return (
      <Paper
        style={{
          paddingRight: 0,
          paddingLeft: 0,
          marginLeft: 0,
          marginRight: 0,
        }}
        sx={{ backgroundColor: "lightgray", padding: 0, margin: 0 }}
        elevation={2}
      >
        <Actor name={note.attributedTo} /> posted a{" "}
        <Link href={note.id} target="_blank">
          Status
        </Link>{" "}
        at {note.published}
        <Button
          variant="outlined"
          onClick={() => setCollapse(false)}
          startIcon={<ExpandMore />}
          size="small"
        >
          Open
        </Button>
      </Paper>
    );
  }

  return (
    <Paper
      sx={{
        backgroundColor: "white",
        padding: 1,
        margin: 0,

        marginTop: 2,
        marginBottom: 2,
      }}
      elevation={2}
    >
      <Actor name={note.attributedTo} /> posted a{" "}
      <Link href={note.id} target="_blank">
        Status
      </Link>{" "}
      at {note.published}
      <ReplyToNote entry={note} />
      <Source entry={source} />
      <NoteContent collapse={collapse} note={note} />
    </Paper>
  );
};

export default CreateNote;
