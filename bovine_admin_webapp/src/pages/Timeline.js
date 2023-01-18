import { Refresh } from "@mui/icons-material";
import { Button, Container, Divider } from "@mui/material";
import React, { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import AddFollower from "../AddFollower";
import CleanTimeline from "../components/CleanTimeline";
import TimelineEntry from "../components/timeline/TimelineEntry";

const Timeline = () => {
  const [timeline, setTimeline] = useState([]);

  const reloadTimeline = () => {
    fetch("/api/")
      .then((x) => x.json())
      .then((x) => setTimeline(x));
  };

  useEffect(() => {
    reloadTimeline();
  }, []);

  return (
    <Container>
      <CleanTimeline timeline={timeline} />
      <Button
        variant="contained"
        onClick={reloadTimeline}
        margin="normal"
        startIcon={<Refresh />}
      >
        Reload
      </Button>
      {timeline.map((entry) => (
        <TimelineEntry key={entry[1]?.id} entry={entry[1]} />
      ))}
      <Divider />
      <AddFollower />
    </Container>
  );
};

export default Timeline;
