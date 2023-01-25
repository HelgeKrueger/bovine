import { Box, Button, Container } from "@mui/material";
import React, { useEffect, useState } from "react";
import AddUrl from "../components/timeline/AddUrl";

import { useLiveQuery } from "dexie-react-hooks";
import { db } from "../database";
import { DisplayConversation } from "../components/timeline/DisplayConversation";

const Timeline = () => {
  const [entry, setEntry] = useState({});
  const [conversationId, setConversationId] = useState(null);
  const [conversation, setConversation] = useState([]);

  const number = useLiveQuery(() =>
    db.activity.where("seen").equals(0).count()
  );

  updateEntry = async () => {
    if (entry?.id) {
      await db.activity.update(entry["id"], { seen: 1 });
    }
    const newEntry = await db.activity
      .where("seen")
      .equals(0)
      // .orderBy("updated")
      .limit(1)
      .toArray();

    if (newEntry.length === 0) {
      setEntry({});
      setConversationId(null);
      return;
    }

    // console.log("new entry", newEntry);
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

  return (
    <Container>
      <Box
        sx={{
          backgroundColor: "white",
          padding: 1,
          margin: 1,
          display: "flex",
        }}
      >
        <Button variant="contained" onClick={updateEntry} margin="normal">
          Next
        </Button>
        <AddUrl />
        Number: {number}
      </Box>
      <DisplayConversation conversation={conversation} fallback={entry} />
    </Container>
  );
};

export default Timeline;
