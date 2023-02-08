import { Container } from "@mui/system";
import React, { useEffect, useState } from "react";
import TimelineEntry from "../components/timeline/TimelineEntry";

import { db } from "../database";

const shouldFilter = (entry) => {
  if (entry?.type === "Like" || entry?.type === "Follow") {
    return true;
  }

  if (!entry?.tag) {
    return false;
  }
  if (entry?.tag?.length === 0) {
    return false;
  }
  if (
    entry?.attributedTo &&
    entry?.attributedTo === "https://mymath.rocks/activitypub/helge"
  ) {
    return false;
  }

  for (let tag of entry.tag) {
    if (tag?.type === "Mention") {
      if (tag?.href.startsWith("https://mymath")) {
        return true;
      }
    }
  }

  return false;
};

const Mentions = () => {
  const [entries, setEntries] = useState([]);

  useEffect(() => {
    db.activity.toArray().then((x) => {
      const data = x.map((entry) => entry.data).filter(shouldFilter);
      setEntries(data);
      console.log(data);
    });
  }, []);

  return (
    <Container>
      {entries.map((entry) => (
        <TimelineEntry entry={entry} key={entry.id} seen={false} />
      ))}
    </Container>
  );
};

export default Mentions;
