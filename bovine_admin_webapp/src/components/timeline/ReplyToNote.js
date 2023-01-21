import { Reply } from "@mui/icons-material";
import { Button, Paper, TextField, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";

const ReplyToNote = ({ entry }) => {
  const [content, setContent] = useState("");
  const [hashtags, setHashtags] = useState("");
  const [mentions, setMentions] = useState("");
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let newHashtags = [];
    let newMentions = [];

    for (let tag of entry?.tag) {
      if (tag?.type === "Mention") {
        newMentions.push(tag?.href);
      } else if (tag?.type === "Hashtag") {
        newHashtags.push(tag?.name);
      }
    }

    setHashtags(newHashtags.join(", "));
    setMentions(newMentions.join(", "));
  }, [entry]);

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

  const sendPost = () => {
    const data = {
      content: content,
      hashtags: hashtags.split(",").map((x) => x.trim()),
      mentions: mentions.split(",").map((x) => x.trim()),
      previous_cc: entry?.cc,
      conversation: entry?.conversation,
      reply_to_id: entry?.id,
      reply_to_atom_uri: entry?.atomUri,
      reply_to_actor: entry?.attributedTo,
    };

    fetch("/api/post", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }).then(() => {
      setOpen(false);
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
      <TextField
        value={mentions}
        onChange={(e) => setMentions(e.target.value)}
        label="Mentions"
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
