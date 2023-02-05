import React from "react";
import { Badge } from "@mui/material";
import { useLiveQuery } from "dexie-react-hooks";
import { db } from "../database";

const UnreadCountBadge = ({ children }) => {
  const number = useLiveQuery(() =>
    db.activity.where({ seen: 0, displayed: 0 }).count()
  );

  return (
    <Badge badgeContent={number} color="secondary" max={999}>
      {children}
    </Badge>
  );
};

export default UnreadCountBadge;
