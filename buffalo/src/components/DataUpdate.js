import React, { useEffect, useState } from "react";

import { IconButton } from "@mui/material";
import { Refresh } from "@mui/icons-material";
import { reloadTimeline } from "../utils/reloadTimeline";

import { EventSourcePolyfill } from "event-source-polyfill";

import config from "../config";

import { transformActivity } from "../utils/transformInboxEntry";
import { db } from "../database";

export const DataUpdate = () => {
  // const [intervalId, setIntervalId] = useState(null);
  const [source, setSource] = useState();

  useEffect(() => {
    if (!source) {
      const headers = {
        Authorization: `Bearer ${config.accessToken}`,
        Accept: "text/event-stream",
      };
      const source = new EventSourcePolyfill(
        "https://mymath.rocks/activitypub/helge/serverSideEvents",
        { headers }
      );

      source.addEventListener("outbox", async (entry) => {
        const activity = transformActivity(JSON.parse(entry.data));
        await db.activity.add(activity);
      });
      setSource(source);
    }
  }, []);

  // useEffect(() => {
  //   const id = setInterval(reloadTimeline, 5 * 60 * 1000);
  //   setIntervalId(id);
  // }, []);

  const buttonClick = () => {
    // clearInterval(intervalId);
    reloadTimeline();

    // const id = setInterval(reloadTimeline, 5 * 60 * 1000);
    // setIntervalId(id);
  };

  return (
    <IconButton onClick={buttonClick} color="primary">
      <Refresh />
    </IconButton>
  );
};
