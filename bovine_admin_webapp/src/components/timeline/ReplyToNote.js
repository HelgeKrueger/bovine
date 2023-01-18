import { Reply } from "@mui/icons-material";
import { Button, Paper, TextField, Typography } from "@mui/material";
import React, { useState } from "react";

const ReplyToNote = ({ entry }) => {
  const [content, setContent] = useState("");
  const [hashtags, setHashtags] = useState("");
  const [open, setOpen] = useState(false);

  if (!open) {
    return (
      <Button
        startIcon={<Reply />}
        onClick={() => {
          setOpen(true);
        }}
      >
        Reply
      </Button>
    );
  }

  const { object } = entry;

  const sendPost = () => {
    const data = {
      content: content,
      hashtags: hashtags.split(",").map((x) => x.trim()),
      conversation: object?.conversation,
      reply_to_id: object?.id,
      reply_to_atom_uri: object?.atomUri,
      reply_to_actor: object?.attributedTo,
    };

    fetch("/api/post", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  };

  return (
    <Paper sx={{ margin: 2, padding: 2 }} elevation={3}>
      <Typography variant="h6">Reply</Typography>
      <TextField
        value={content}
        onChange={(e) => setContent(e.target.value)}
        label="Content"
        multiline
        fullWidth
        margin="normal"
      />
      <TextField
        value={hashtags}
        onChange={(e) => setHashtags(e.target.value)}
        label="Hashtags"
        fullWidth
        margin="normal"
      />
      <Button
        onClick={sendPost}
        variant="contained"
        fullWidth
        startIcon={<Reply />}
      >
        Reply
      </Button>
    </Paper>
  );
};

export default ReplyToNote;
