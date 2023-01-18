import { Button, Paper, TextField, Typography } from "@mui/material";
import React, { useState } from "react";

const Post = () => {
  const [content, setContent] = useState("");
  const [hashtags, setHashtags] = useState("");

  const sendPost = () => {
    const data = {
      content: content,
      hashtags: hashtags.split(",").map((x) => x.trim()),
    };

    fetch("/api/post", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
  };

  return (
    <Paper sx={{ margin: 2, padding: 2 }} elevation={3}>
      <Typography variant="h3">New Post</Typography>
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
      <Button onClick={sendPost} variant="contained" fullWidth>
        Post
      </Button>
    </Paper>
  );
};

export default Post;
