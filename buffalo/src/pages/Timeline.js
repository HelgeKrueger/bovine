import { Box, IconButton } from "@mui/material";
import React, { useEffect, useState } from "react";

import { useSwipeable } from "react-swipeable";
import { db } from "../database";
import { DisplayConversation } from "../components/timeline/DisplayConversation";
import { Message } from "@mui/icons-material";
import { DataUpdate } from "../components/DataUpdate";
import UnreadCountBadge from "../components/UnreadCountBadge";
import AllRead from "../components/navigation/AllRead";
import ToPost from "../components/navigation/ToPost";
import ToSketch from "../components/navigation/ToSketch";
import ToFetch from "../components/navigation/ToFetch";

import PullToRefresh from "react-simple-pull-to-refresh";
import { reloadTimeline } from "../utils/reloadTimeline";

const Timeline = () => {
  const [entry, setEntry] = useState({});
  const [conversationId, setConversationId] = useState(null);
  const [conversation, setConversation] = useState([]);

  const updateEntry = async () => {
    const toUpdate = await db.activity.where("displayed").equals(1).toArray();
    for (let update of toUpdate) {
      await db.activity.update(update["id"], { seen: 1, displayed: 0 });
    }
    const newEntry = await db.activity
      .where("seen")
      .equals(0)
      .limit(1)
      .toArray();

    if (newEntry.length === 0) {
      setEntry({});
      setConversationId(null);
      return;
    }

    const element = newEntry[0];
    setEntry(element["data"]);
    setConversationId(element["conversation"]);
  };

  const updateConversation = async () => {
    if (conversationId) {
      const convo = await db.activity
        .where("conversation")
        .equals(conversationId)
        .toArray();

      setConversation(convo);
    } else {
      setConversation([]);
    }
  };

  useEffect(() => {
    updateConversation();
  }, [conversationId]);

  const handlers = useSwipeable({
    onSwipedLeft: updateEntry,
  });

  return (
    <div {...handlers}>
      <Box
        sx={{
          backgroundColor: "white",
          paddingTop: 1,
          display: "flex",
        }}
      >
        <AllRead />
        <ToPost />
        <ToSketch />
        <ToFetch />
        <DataUpdate />
        <IconButton onClick={updateEntry} color="primary">
          <UnreadCountBadge>
            <Message />
          </UnreadCountBadge>
        </IconButton>
      </Box>
      <PullToRefresh onRefresh={reloadTimeline}>
        <DisplayConversation conversation={conversation} fallback={entry} />
      </PullToRefresh>
    </div>
  );
};

export default Timeline;
