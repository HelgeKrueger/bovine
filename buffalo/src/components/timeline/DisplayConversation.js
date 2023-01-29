import { Container } from "@mui/material";
import React from "react";
import TimelineEntry from "./TimelineEntry";

import { buildTree, getDateForEntry } from "../../utils/conversations";

export const DisplayConversation = ({ conversation, fallback }) => {
  if (conversation.length === 0) {
    return <TimelineEntry entry={fallback} />;
  }
  const root = buildTree(conversation, fallback);
  if (!root) {
    return <TimelineEntry entry={fallback} />;
  }
  return <DisplayTreeItem entry={root} />;
};

const DisplayTreeItem = ({ entry }) => {
  const children = entry?.children;
  const sortedChildren = children?.sort((a, b) => {
    return getDateForEntry(b) - getDateForEntry(a);
  });
  const seen = entry?.seen;
  return (
    <>
      <TimelineEntry entry={entry?.data} seen={seen} />
      <Container style={{ paddingRight: 0, marginRight: 0 }}>
        {sortedChildren?.map((child) => {
          return <DisplayTreeItem entry={child} key={child.id} />;
        })}
      </Container>
    </>
  );
};
