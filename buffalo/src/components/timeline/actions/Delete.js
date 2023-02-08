import { Delete as DeleteIcon } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import React, { useEffect, useState } from "react";
import { buildDelete } from "../../../activitystreams/builders";
import { sendToOutbox } from "../../../client";
import config from "../../../config";
import { db } from "../../../database";

const Delete = ({ object }) => {
  const [disabled, setDisabled] = useState(false);
  useEffect(() => {
    setDisabled(false);
  }, [object]);
  if (!object?.id.startsWith("https://mymath.rocks/")) {
    return <></>;
  }

  const sendDelete = () => {
    const like = buildDelete(config.actor, object);
    setDisabled(true);
    sendToOutbox(like);

    db.activity.where("id").equals(object.id).delete();
  };

  return (
    <IconButton
      onClick={() => {
        sendDelete();
      }}
      variant="outlined"
      color="primary"
      disabled={disabled}
    >
      <DeleteIcon />
    </IconButton>
  );
};

export default Delete;
