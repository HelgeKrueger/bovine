import { ExpandMore } from "@mui/icons-material";
import { Divider, Link, Paper, Box, IconButton } from "@mui/material";
import React, { useEffect, useState } from "react";
import Like from "./actions/Like";
import Actor from "./Actor";
import Attachments from "./Attachments";
import ReplyToNote from "./ReplyToNote";
import ReplyWithSketch from "./ReplyWithSketch";
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
    const publishedDate = new Date(note.published);
    const formattedDate = publishedDate.toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
    });
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
        <small>
          <Actor name={note.attributedTo} short />
          &lsquo;s
          <Link href={note.id} target="_blank">
            Status
          </Link>{" "}
          at {formattedDate}
          <IconButton
            onClick={() => setCollapse(false)}
            color="primary"
            sx={{ padding: 0 }}
          >
            <ExpandMore />
          </IconButton>
        </small>
      </Paper>
    );
  }

  return (
    <Paper
      sx={{
        backgroundColor: "white",
        padding: 0,
        margin: 0,

        marginTop: 2,
        marginBottom: 2,
      }}
      elevation={2}
    >
      <Box sx={{ backgroundColor: "#cccccc", padding: 1 }}>
        <Actor name={note.attributedTo} /> posted a{" "}
        <Link href={note.id} target="_blank">
          Status
        </Link>{" "}
        at {note.published}
      </Box>
      <Box sx={{ padding: 2 }}>
        <NoteContent collapse={collapse} note={note} />
      </Box>
      <Box sx={{ backgroundColor: "#cccccc", padding: 0 }}>
        <ReplyToNote entry={note} />
        <ReplyWithSketch entry={note} />
        <Source entry={source} />
        <Like object={note} />
      </Box>
    </Paper>
  );
};

export default CreateNote;
