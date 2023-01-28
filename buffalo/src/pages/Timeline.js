import { Box, IconButton } from "@mui/material";
import React, { useEffect, useState } from "react";

import { useNavigate } from "react-router-dom";
import { useSwipeable } from "react-swipeable";
import { useLiveQuery } from "dexie-react-hooks";
import { db } from "../database";
import { DisplayConversation } from "../components/timeline/DisplayConversation";
import { Check, Create, NavigateNext } from "@mui/icons-material";
import { DataUpdate } from "../components/timeline/DataUpdate";

const Timeline = () => {
  const [entry, setEntry] = useState({});
  const [conversationId, setConversationId] = useState(null);
  const [conversation, setConversation] = useState([]);

  const navigate = useNavigate();

  const number = useLiveQuery(() =>
    db.activity.where("seen").equals(0).count()
  );

  const updateEntry = async () => {
    const toUpdate = await db.activity.where("displayed").equals(1).toArray();
    for (let update of toUpdate) {
      await db.activity.update(update["id"], { seen: 1, displayed: 0 });
    }
    const newEntry = await db.activity
      // .orderBy("updated")
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

      // console.log("convo", convo);

      setConversation(convo);
    } else {
      setConversation([]);
    }
  };

  useEffect(() => {
    updateConversation();
  }, [conversationId]);

  const allRead = () => {
    db.activity
      .where("seen")
      .equals(0)
      .toArray()
      .then((data) => {
        for (let entry of data) {
          db.activity.update(entry.id, { seen: 1 });
        }
      });
  };

  const handlers = useSwipeable({
    onSwipedLeft: updateEntry,
  });

  return (
    <div {...handlers}>
      <Box
        sx={{
          backgroundColor: "white",
          // padding: 1,
          // margin: 1,
          display: "flex",
          // maxWidth: "800px",
        }}
      >
        <IconButton onClick={updateEntry} color="primary">
          <NavigateNext />
        </IconButton>
        <IconButton onClick={allRead} color="primary">
          <Check />
        </IconButton>
        <IconButton
          color="primary"
          onClick={() => {
            navigate("/post");
          }}
        >
          <Create />
        </IconButton>
        <DataUpdate />
        Number: {number}
      </Box>
      <DisplayConversation conversation={conversation} fallback={entry} />
    </div>
  );
};

export default Timeline;
