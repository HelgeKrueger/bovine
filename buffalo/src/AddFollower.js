import { Button, Paper, TextField } from "@mui/material";
import React, { useState } from "react";

const AddFollower = () => {
  const [username, setUsername] = useState("");

  const handleAdd = () => {
    fetch("/api/add_follow", {
      method: "post",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ account: username.trim() }),
    })
      .then((x) => x.json())
      .then(console.log);
  };
  return (
    <Paper
      sx={{ backgroundColor: "white", padding: 2, margin: 2 }}
      elevation={2}
    >
      <TextField
        label="Username to follow"
        value={username}
        onChange={(e) => {
          setUsername(e.target.value);
        }}
      />
      <Button onClick={handleAdd} variant="contained">
        Add
      </Button>
    </Paper>
  );
};

export default AddFollower;
