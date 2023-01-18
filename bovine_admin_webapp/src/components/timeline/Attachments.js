import { Link } from "@mui/material";
import React from "react";

const Attachment = ({ entry }) => {
  return (
    <Link target="_blank" href={entry?.url}>
      {entry?.mediaType}
    </Link>
  );
};

const Attachments = ({ attachments }) => {
  if (!attachments || attachments.length === 0) {
    return <></>;
  }

  return attachments.map((entry) => (
    <Attachment entry={entry} key={entry?.url} />
  ));
};

export default Attachments;
