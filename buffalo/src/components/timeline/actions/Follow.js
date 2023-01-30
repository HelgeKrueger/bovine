import { PersonAdd } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import React, { useEffect, useState } from "react";
import { buildFollow } from "../../../activitystreams/builders";
import { sendToOutbox } from "../../../client";

const Follow = ({ actor }) => {
  const [disabled, setDisabled] = useState(false);
  const sendFollow = () => {
    const like = buildFollow(actor?.id);
    setDisabled(true);
    sendToOutbox(like);
  };
  useEffect(() => {
    setDisabled(false);
  }, [actor]);
  return (
    <IconButton
      onClick={() => {
        sendFollow();
      }}
      variant="outlined"
      color="primary"
      disabled={disabled}
    >
      <PersonAdd />
    </IconButton>
  );
};

export default Follow;
