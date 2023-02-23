import { Close, Reply } from "@mui/icons-material";
import {
  Button,
  IconButton,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import React, { useEffect, useState } from "react";

import { buildNote, buildCreateForNote } from "../../activitystreams/builders";
import { sendToOutbox } from "../../client";
import config from "../../config";

const ReplyToNote = ({ entry }) => {
  const [content, setContent] = useState("");
  const [hashtags, setHashtags] = useState("");
  const [mentions, setMentions] = useState("");
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let newHashtags = [];
    let newMentions = [];

    let tags = entry?.tag;

    if (tags) {
      if (typeof tags == "object" && !(0 in tags)) {
        tags = [tags];
      }
      try {
        for (let tag of tags) {
          if (tag?.type === "Mention") {
            newMentions.push(tag?.href);
          } else if (tag?.type === "Hashtag") {
            newHashtags.push(tag?.name);
          }
        }
      } catch {
        console.error("Error processing tags");
        console.error(tags);
      }
    }

    if (entry?.attributedTo) {
      let attributedTo = entry?.attributedTo;
      if (typeof attributedTo === "object") {
        attributedTo = attributedTo?.id;
      }
      newMentions.push(attributedTo);
    }
    setHashtags(newHashtags.join(", "));
    setMentions(newMentions.join(", "));
  }, [entry]);

  if (!open) {
    return (
      <IconButton
        onClick={() => {
          setOpen(true);
        }}
        color="primary"
        sx={{ margin: 1 }}
      >
        <Reply />
      </IconButton>
    );
  }

  const sendPost = () => {
    const note = buildNote(config.actor, content, {
      content: content,
      hashtags: hashtags.split(",").map((x) => x.trim()),
      mentions: mentions.split(",").map((x) => x.trim()),
      cc: entry?.cc,
      to: entry?.to,
      conversation: entry?.conversation,
      inReplyTo: entry?.id,
      inReplyToAtomUri: entry?.atomUri,
      replyToActor: entry?.attributedTo,
    });

    const data = buildCreateForNote(note);
    sendToOutbox(data).then(() => {
      setOpen(false);
    });
  };

  return (
    <Paper sx={{ margin: 2, padding: 2 }} elevation={3}>
      <Typography variant="h6">
        Reply{" "}
        <Button
          variant="outlined"
          startIcon={<Close />}
          onClick={() => setOpen(false)}
        >
          Close
        </Button>
      </Typography>
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
