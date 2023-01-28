import React, { useEffect, useState } from "react";
import { db } from "../../database";
import config from "../../config";
import { Button, IconButton } from "@mui/material";
import { Refresh } from "@mui/icons-material";

const transformEntry = (entry) => {
  let data = entry[1];
  let remoteId = entry[0];
  if (data.type === "Create" || data.type === "Update") {
    data = data?.object;
  }
  const id = data?.id;
  const conversation = data?.conversation;
  const seen = 0;

  let updated = data?.updated;
  if (!updated) {
    updated = data?.published;
  }

  return {
    id,
    conversation,
    seen,
    updated,
    data,
    remoteId,
  };
};

export const DataUpdate = () => {
  const [timeline, setTimeline] = useState([]);
  const [intervalId, setIntervalId] = useState(null);

  const reloadTimeline = async () => {
    const minArrayList = await db.activity
      .orderBy("remoteId")
      .reverse()
      .limit(1)
      .toArray();
    let min_id = 0;
    if (minArrayList.length > 0) {
      min_id = minArrayList[0].remoteId;
    }
    fetch(`https://mymath.rocks/activitypub/helge/inbox_tmp?min_id=${min_id}`, {
      headers: {
        Authorization: `Bearer ${config.accessToken}`,
      },
    })
      .then((x) => x.json())
      .then((x) => setTimeline(x));
  };
  useEffect(() => {
    async function addActivity() {
      try {
        await db.activity.bulkAdd(timeline.map(transformEntry));
      } catch (error) {
        // console.error(error);
      }
    }
    addActivity();
  }, [timeline]);

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
