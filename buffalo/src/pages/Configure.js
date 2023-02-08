import { Button, Container, Paper, TextField, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { db } from "../database";

const Configure = () => {
  const [actorUrl, setActorUrl] = useState("");
  const [accessToken, setAccessToken] = useState("");

  useEffect(() => {
    db.meta.toArray().then((data) => {
      for (let value of data) {
        if (value.key === "actor") {
          setActorUrl(value.value);
        }
        if (value.key === "accessToken") {
          setAccessToken(value.value);
        }
      }
    });
  }, []);

  const loadActor = () => {
    fetch(actorUrl, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        Accept: "application/activity+json",
      },
    })
      .then((x) => x.json())
      .then(async (data) => {
        db.meta.put({ key: "actor", value: actorUrl });
        db.meta.put({ key: "accessToken", value: accessToken });
        db.meta.put({ key: "outbox", value: data.outbox });
        db.meta.put({ key: "inbox", value: data.inbox });

        console.log(data);
      });
  };
  return (
    <Container>
      <Typography variant="h5">Configuration</Typography>

      <Paper>
        <TextField
          label="Actor Url"
          value={actorUrl}
          onChange={(e) => setActorUrl(e.target.value)}
          fullWidth
          margin="normal"
        />
        <TextField
          label="AccessToken"
          value={accessToken}
          onChange={(e) => setAccessToken(e.target.value)}
          fullWidth
          margin="normal"
        />
        <Button
          onClick={loadActor}
          fullWidth
          variant="contained"
          sx={{ margin: 2, padding: 2 }}
        >
          Sign In
        </Button>
      </Paper>
    </Container>
  );
};

export default Configure;
