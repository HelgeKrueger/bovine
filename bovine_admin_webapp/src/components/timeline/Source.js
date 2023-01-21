import React, { useEffect, useState } from "react";
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  FormControlLabel,
  Switch,
} from "@mui/material";

const Source = ({ entry }) => {
  const [useContext, setUseContext] = useState(false);
  const [text, setText] = useState("");

  useEffect(() => {
    let data = { ...entry };
    if (!useContext) {
      delete data["@context"];
    }
    setText(JSON.stringify(data, null, 2));
  }, [useContext]);

  return (
    <Accordion>
      <AccordionSummary>Source</AccordionSummary>
      <FormControlLabel
        label="Display Context"
        control={
          <Switch
            checked={useContext}
            onChange={(e) => setUseContext(e.target.checked)}
          />
        }
      />
      <AccordionDetails>
        <small>
          <pre>{text}</pre>
        </small>
      </AccordionDetails>
    </Accordion>
  );
};

export default Source;
