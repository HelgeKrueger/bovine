import { Check } from "@mui/icons-material";
import { IconButton } from "@mui/material";
import React from "react";
import { db } from "../../database";

const AllRead = () => {
  const markAllRead = () => {
    db.activity
      .where("seen")
      .equals(0)
      .toArray()
      .then((data) => {
        for (let entry of data) {
          db.activity.update(entry.id, { seen: 1 });
        }
      });
  };

  return (
    <IconButton onClick={markAllRead} color="primary">
      <Check />
    </IconButton>
  );
};

export default AllRead;
