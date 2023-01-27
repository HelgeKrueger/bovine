import { Favorite, Star } from "@mui/icons-material";
import { Button, IconButton } from "@mui/material";
import React, { useEffect, useState } from "react";
import { buildLike } from "../../../activitystreams/builders";
import { sendToOutbox } from "../../../client";
import config from "../../../config";

const Like = ({ object }) => {
  const [disabled, setDisabled] = useState(false);
  const sendLike = () => {
    const like = buildLike(config.actor, object);
    setDisabled(true);
    sendToOutbox(like);
  };
  useEffect(() => {
    setDisabled(false);
  }, [object]);
  return (
    <IconButton
      onClick={() => {
        sendLike();
      }}
      variant="outlined"
      color="primary"
      disabled={disabled}
    >
      <Favorite />
      {/* <Star /> */}
    </IconButton>
  );
};

export default Like;
