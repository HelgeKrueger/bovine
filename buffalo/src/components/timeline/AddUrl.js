import { Add } from "@mui/icons-material";
import { Button, Container, TextField } from "@mui/material";
import React, { useState } from "react";

const AddUrl = () => {
  const [urlToFetch, setUrlToFetch] = useState("");

  const performFetch = () => {
    // FIXME use this to query proxy endpoint
    // fetch('/', {method:"POST", headers: {
    //   'Content-Type': 'application/x-www-form-urlencoded'
    // },
    // body: new URLSearchParams({"id": "uuid"})})
    fetch("/api/fetch", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        url: urlToFetch,
      }),
    }).then(() => {
      window.location.reload();
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
