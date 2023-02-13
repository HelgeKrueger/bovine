import { Add } from "@mui/icons-material";
import { Button, Container, TextField } from "@mui/material";
import React, { useState } from "react";

import { transformActivity } from "../../utils/transformInboxEntry";
import { db } from "../../database";

const AddUrl = () => {
  const [urlToFetch, setUrlToFetch] = useState("");

  const performFetch = () => {
    fetch("/", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ id: urlToFetch }),
    })
      .then((x) => x.json())
      .then(async (data) => {
        const activity = transformActivity(data);
        await db.activity.add(activity);
      });
  };

  return (
    <Container>
      <TextField
        label="url"
        value={urlToFetch}
        onChange={(e) => setUrlToFetch(e.target.value)}
      />
      <Button onClick={performFetch} startIcon={<Add />} variant="contained">
        Fetch
      </Button>
    </Container>
  );
};

export default AddUrl;
