import { Paper } from "@mui/material";
import React, { useEffect, useState } from "react";
import TimelineEntry from "../components/timeline/TimelineEntry";
import { db } from "../database";

const Outbox = () => {
  const [elements, setElements] = useState([]);

  useEffect(() => {
    db.activity
      .where("id")
      .startsWith("https://mymath.rocks/")
      .toArray()
      .then((els) => els.map((entry) => entry.data))
      .then((els) => els.filter((obj) => obj?.type !== "Follow"))
      .then((els) => setElements(els));
  }, []);

  return (
    <Paper>
      {elements.map((entry) => (
        <TimelineEntry entry={entry} key={entry.id} />
      ))}
    </Paper>
  );
};

export default Outbox;
