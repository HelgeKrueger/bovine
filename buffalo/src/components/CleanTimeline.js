import { Button } from "@mui/material";
import React, { useState } from "react";

const CleanTimeline = ({ timeline }) => {
  const [disabled, setDisabled] = useState(false);

  if (!timeline) {
    return <></>;
  }

  const cleanUp = () => {
    setDisabled(true);
    const maxId = Math.max(...timeline.map((x) => x[0]));

    fetch(`/api/cleanup?max_id=${maxId}`)
      .then((x) => x.json())
      .then((x) => {
        if (x["status"] === "done") {
          window.location.reload();
        }
      });
  };

  return (
    <Button variant="contained" onClick={cleanUp} disabled={disabled}>
      Cleanup Timline
    </Button>
  );
};

export default CleanTimeline;
