import { Box } from "@mui/material";
import React, { useEffect, useState, createContext } from "react";
import { Outlet } from "react-router";
import { BrowserView, MobileView } from "react-device-detect";

import { db } from "../database";
import Navigation from "../components/navigation/Navigation";

const EntryContext = createContext(null);

const Main = () => {
  const [entry, setEntry] = useState({});
  const [conversationId, setConversationId] = useState(null);
  const [conversation, setConversation] = useState([]);

  const updateEntry = async () => {
    const toUpdate = await db.activity.where("displayed").equals(1).toArray();
    for (let update of toUpdate) {
      await db.activity.update(update["id"], { seen: 1, displayed: 0 });
    }
    let newEntry = await db.activity.where("seen").equals(0).limit(1).toArray();

    while (
      newEntry.length > 0 &&
      ["Delete", "Tombstone"].indexOf(newEntry[0]["data"]["type"]) > -1
    ) {
      await db.activity.update(newEntry[0]["id"], { seen: 1, displayed: 0 });
      newEntry = await db.activity.where("seen").equals(0).limit(1).toArray();
    }

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
  return (
    <>
      <EntryContext.Provider value={{ entry, conversation, updateEntry }}>
        <BrowserView>
          <Box sx={{ maxWidth: "800px", marginLeft: "calc(50% - 400px)" }}>
            <Navigation />
            <Outlet />
          </Box>
        </BrowserView>
        <MobileView>
          <Navigation />
          <Outlet />
        </MobileView>
      </EntryContext.Provider>
    </>
  );
};

export default Main;
export { EntryContext };
