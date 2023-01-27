import { Button, Paper, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import { useNavigate } from "react-router";
import { v4 as uuidv4 } from "uuid";
import { sendToOutbox } from "../client";

import config from "../config";
import { buildNote, buildCreateForNote } from "../activitystreams/builders";

const Post = () => {
  const [content, setContent] = useState("");
  const [hashtags, setHashtags] = useState("");

  const navigate = useNavigate();

  const sendPost = () => {
    const id = config.actor + "/" + uuidv4();

    const note = buildNote(config.actor, content, {
      hashtags: hashtags.split(",").map((x) => x.trim()),
    });
    const data = buildCreateForNote(note);

    sendToOutbox(data).then(() => {
      navigate("/");
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
