import { ArrowBack, Search } from "@mui/icons-material";
import { Button, Paper, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import { useNavigate } from "react-router";
import { sendFetch } from "../client";

const Fetch = () => {
  const [url, setUrl] = useState("");

  const navigate = useNavigate();

  const handleFetch = () => {
    const data = {
      url,
    };

    sendFetch(data).then(() => {
      navigate("/");
    });
  };

  return (
    <Paper sx={{ margin: 2, padding: 2 }} elevation={3}>
      <Typography variant="h3">Fetch</Typography>
      <TextField
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        label="Url"
        fullWidth
        sx={{ margin: 1 }}
      />
      <Button
        onClick={handleFetch}
        variant="contained"
        fullWidth
        startIcon={<Search />}
        sx={{ margin: 1 }}
      >
        Fetch
      </Button>
      <Button
        onClick={() => {
          navigate("/");
        }}
        variant="contained"
        fullWidth
        startIcon={<ArrowBack />}
        sx={{ margin: 1 }}
      >
        Back
      </Button>
    </Paper>
  );
};

export default Fetch;
