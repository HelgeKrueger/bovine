import { Button, Paper, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import { v4 as uuidv4 } from "uuid";

import config from "../config";

const Post = () => {
  const [content, setContent] = useState("");
  const [hashtags, setHashtags] = useState("");

  const sendPost = () => {
    const id = config.actor + "/" + uuidv4();
    const published = new Date().toISOString();
    const data = {
      "@context": [
        "https://www.w3.org/ns/activitystreams",
        {
          inReplyToAtomUri: "ostatus:inReplyToAtomUri",
          conversation: "ostatus:conversation",
          ostatus: "http://ostatus.org#",
        },
      ],
      actor: config.actor,
      cc: [config.actor + "/followers"],
      id: id,
      object: {
        "@context": "https://www.w3.org/ns/activitystreams",
        attributedTo: config.actor,
        cc: [config.actor + "/followers"],
        content: `<p>${content}</p>`,
        id: id,
        inReplyTo: null,
        published: published,
        to: ["https://www.w3.org/ns/activitystreams#Public"],
        type: "Note",
      },
      published: published,
      to: ["https://www.w3.org/ns/activitystreams#Public"],
      type: "Create",
    };

    fetch(config.outbox, {
      method: "post",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${config.accessToken}`,
      },
      body: JSON.stringify(data),
    })
      .then(console.log)
      .catch(console.error);
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
