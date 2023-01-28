import { Brush, Close, Reply } from "@mui/icons-material";
import {
  Button,
  IconButton,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import React, { useEffect, useRef, useState } from "react";
import { v4 as uuidv4 } from "uuid";
import { Stage, Layer, Line, Rect } from "react-konva";

import { buildCreateForNote, buildImage } from "../../activitystreams/builders";
import config from "../../config";
import { dataURItoBlob } from "../../utils/image";

const ReplyWithSketch = ({ entry }) => {
  const [lines, setLines] = useState([]);
  const isDrawing = useRef(false);
  const stageRef = React.useRef(null);

  const [hashtags, setHashtags] = useState("");
  const [mentions, setMentions] = useState("");
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let newHashtags = [];
    let newMentions = [];

    const tags = entry?.tag;

    if (tags) {
      for (let tag of tags) {
        if (tag?.type === "Mention") {
          newMentions.push(tag?.href);
        } else if (tag?.type === "Hashtag") {
          newHashtags.push(tag?.name);
        }
      }
    }

    if (entry?.attributedTo) {
      newMentions.push(entry?.attributedTo);
    }
    setHashtags(newHashtags.join(", "));
    setMentions(newMentions.join(", "));
  }, [entry]);

  const handleMouseDown = (e) => {
    isDrawing.current = true;
    const pos = e.target.getStage().getPointerPosition();
    setLines([...lines, { tool: "pen", points: [pos.x, pos.y] }]);
  };

  const handleMouseMove = (e) => {
    if (!isDrawing.current) {
      return;
    }
    const stage = e.target.getStage();
    const point = stage.getPointerPosition();
    let lastLine = lines[lines.length - 1];
    lastLine.points = lastLine.points.concat([point.x, point.y]);
    lines.splice(lines.length - 1, 1, lastLine);
    setLines(lines.concat());
  };

  const handleMouseUp = () => {
    isDrawing.current = false;
  };

  if (!open) {
    return (
      <IconButton
        onClick={() => {
          setOpen(true);
        }}
        color="primary"
        sx={{ margin: 1 }}
      >
        <Brush />
      </IconButton>
    );
  }

  const sendPost = () => {
    const image = stageRef.current.toDataURL();
    const formData = new FormData();

    const imageName = uuidv4();

    formData.append(imageName, dataURItoBlob(image, "image/png"), "image.png");
    const imageObject = buildImage(config.actor, config.storage + imageName, {
      hashtags: hashtags.split(",").map((x) => x.trim()),
      mentions: mentions.split(",").map((x) => x.trim()),
      cc: entry?.cc,
      to: entry?.to,
      conversation: entry?.conversation,
      inReplyTo: entry?.id,
      inReplyToAtomUri: entry?.atomUri,
      replyToActor: entry?.attributedTo,
    });

    const data = buildCreateForNote(imageObject);

    formData.append("activity", JSON.stringify(data));

    fetch(config.outbox, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${config.accessToken}`,
      },
      body: formData,
    }).then(() => {
      setOpen(false);
    });
  };

  return (
    <Paper sx={{ margin: 2, padding: 2 }} elevation={3}>
      <Typography variant="h6">
        Sketch{" "}
        <Button
          variant="outlined"
          startIcon={<Close />}
          onClick={() => setOpen(false)}
        >
          Close
        </Button>
      </Typography>
      <div>
        <Stage
          ref={stageRef}
          width={300}
          height={300}
          onMouseDown={handleMouseDown}
          onMousemove={handleMouseMove}
          onMouseup={handleMouseUp}
          onTouchStart={handleMouseDown}
          onTouchEnd={handleMouseUp}
          onTouchMove={handleMouseMove}
        >
          <Layer>
            <Rect x={0} y={0} width={300} height={300} fill={"#fec"} />
            {lines.map((line, i) => (
              <Line
                key={i}
                points={line.points}
                stroke="black"
                strokeWidth={5}
                tension={0.5}
                lineCap="round"
                lineJoin="round"
                globalCompositeOperation={"source-over"}
              />
            ))}
          </Layer>
        </Stage>
      </div>
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

export default ReplyWithSketch;
