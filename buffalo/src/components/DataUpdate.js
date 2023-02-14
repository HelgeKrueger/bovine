import React, { useEffect, useState } from "react";

import { IconButton } from "@mui/material";
import { Refresh } from "@mui/icons-material";
import { reloadTimeline } from "../utils/reloadTimeline";

import { EventSourcePolyfill } from "event-source-polyfill";

import config from "../config";

import { transformActivity } from "../utils/transformInboxEntry";
import { db } from "../database";

export const DataUpdate = () => {
  const [source, setSource] = useState();

  useEffect(() => {
    if (!source) {
      db.activity
        .orderBy("remoteId")
        .reverse()
        .limit(1)
        .toArray()
        .then((x) => {
          const lastEventId = x[0].remoteId;

          const headers = {
            "Last-Event-Id": lastEventId,
            Authorization: `Bearer ${config.accessToken}`,
            Accept: "text/event-stream",
          };

          const source = new EventSourcePolyfill(
            "https://mymath.rocks/activitypub/helge/serverSideEvents",
            { headers }
          );

          source.addEventListener("inbox", async (entry) => {
            const activity = transformActivity(
              JSON.parse(entry.data),
              entry.lastEventId
            );
            await db.activity.add(activity);
          });
          setSource(source);
        });
    }
  }, []);

  const buttonClick = () => {
    reloadTimeline();
  };

  return (
    <IconButton onClick={buttonClick} color="primary">
      <Refresh />
    </IconButton>
  );
};
