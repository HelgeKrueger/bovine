import { Box, Button, Container, Divider } from "@mui/material";
import React, { useEffect, useState } from "react";
import AddUrl from "../components/timeline/AddUrl";

import { useNavigate } from "react-router-dom";

import { useLiveQuery } from "dexie-react-hooks";
import { db } from "../database";
import { DisplayConversation } from "../components/timeline/DisplayConversation";
import TimelineEntry from "../components/timeline/TimelineEntry";
import { Check, Create } from "@mui/icons-material";

const Timeline = () => {
  const [entry, setEntry] = useState({});
  const [conversationId, setConversationId] = useState(null);
  const [conversation, setConversation] = useState([]);

  const navigate = useNavigate();

  const number = useLiveQuery(() =>
    db.activity.where("seen").equals(0).count()
  );

  updateEntry = async () => {
    // if (entry?.id) {
    // await db.activity.update(entry["id"], { seen: 1 });
    // }
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

  return (
    <>
      <Box
        sx={{
          backgroundColor: "white",
          // padding: 1,
          // margin: 1,
          display: "flex",
          // maxWidth: "800px",
        }}
      >
        <Button variant="contained" onClick={updateEntry} margin="normal">
          Next
        </Button>
        <Button
          variant="contained"
          onClick={allRead}
          margin="normal"
          startIcon={<Check />}
        >
          All Read
        </Button>
        Number: {number}
        <Button
          variant="contained"
          margin="normal"
          startIcon={<Create />}
          onClick={() => {
            navigate("/post");
          }}
        >
          Post
        </Button>
      </Box>
      <TimelineEntry entry={entry} seen={0} />
      <Divider />
      <DisplayConversation conversation={conversation} fallback={entry} />
    </>
  );
};

export default Timeline;
