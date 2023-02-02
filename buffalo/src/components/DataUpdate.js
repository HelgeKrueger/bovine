import React, { useEffect, useState } from "react";

import { IconButton } from "@mui/material";
import { Refresh } from "@mui/icons-material";
import { reloadTimeline } from "../utils/reloadTimeline";

export const DataUpdate = () => {
  const [intervalId, setIntervalId] = useState(null);

  useEffect(() => {
    const id = setInterval(reloadTimeline, 5 * 60 * 1000);
    setIntervalId(id);
  }, []);

  const buttonClick = () => {
    clearInterval(intervalId);
    reloadTimeline();

    const id = setInterval(reloadTimeline, 5 * 60 * 1000);
    setIntervalId(id);
  };

  return (
    <IconButton onClick={buttonClick} color="primary">
      <Refresh />
    </IconButton>
  );
};
