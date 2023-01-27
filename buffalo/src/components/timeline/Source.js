import React, { useEffect, useState } from "react";
import {
  Button,
  FormControlLabel,
  IconButton,
  Paper,
  Switch,
  Typography,
} from "@mui/material";
import { Code, CodeOff } from "@mui/icons-material";

const Source = ({ entry }) => {
  const [useContext, setUseContext] = useState(false);
  const [text, setText] = useState("");
  const [open, setOpen] = useState(false);

  useEffect(() => {
    let data = { ...entry };
    if (!useContext) {
      delete data["@context"];
    }
    setText(JSON.stringify(data, null, 2));
  }, [useContext]);

  if (!open) {
    return (
      <IconButton
        onClick={() => {
          setOpen(true);
        }}
        color="primary"
        variant="outlined"
      >
        <Code />
      </IconButton>
    );
  }

  return (
    <Paper>
      <Typography variant="h4">
        Source
        <FormControlLabel
          label="Display Context"
          control={
            <Switch
              checked={useContext}
              onChange={(e) => setUseContext(e.target.checked)}
            />
          }
          sx={{ margin: 1 }}
        />
        <Button
          startIcon={<CodeOff />}
          variant="outlined"
          onClick={() => setOpen(false)}
          sx={{ margin: 1 }}
        >
          Close
        </Button>
      </Typography>
      <small>
        <pre>{text}</pre>
      </small>
    </Paper>
  );
};

export default Source;
