import { Star } from "@mui/icons-material";
import { Button } from "@mui/material";
import React from "react";
import { buildLike } from "../../../activitystreams/builders";
import { sendToOutbox } from "../../../client";
import config from "../../../config";

const Like = ({ object }) => {
  const sendLike = () => {
    const like = buildLike(config.actor, object);
    console.log(like);
    sendToOutbox(like);
  };
  return (
    <Button
      startIcon={<Star />}
      onClick={() => {
        sendLike();
      }}
      variant="outlined"
      sx={{ margin: 1 }}
    >
      Like
    </Button>
  );
};

export default Like;
