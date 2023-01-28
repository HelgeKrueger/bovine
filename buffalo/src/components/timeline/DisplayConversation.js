import { Container } from "@mui/material";
import React from "react";
import TimelineEntry from "./TimelineEntry";

import { buildTree } from "../../utils/conversations";

export const DisplayConversation = ({ conversation, fallback }) => {
  const root = buildTree(conversation, fallback);
  if (!root) {
    return <TimelineEntry entry={fallback} />;
  }
  return <DisplayTreeItem entry={root} />;
};

const DisplayTreeItem = ({ entry }) => {
  //   console.log(entry);
  const children = entry?.children;
  const sortedChildren = children?.sort((a, b) => {
    // console.log(a, new Date(a?.updated));
    return new Date(b?.updated) - new Date(a?.updated);
  });
  // console.log(sortedChildren);
  const seen = entry?.seen;
  return (
    <>
      <TimelineEntry entry={entry?.data} seen={seen} />
      <Container style={{ paddingRight: 0, marginRight: 0 }}>
        {sortedChildren?.map((child) => {
          // console.log(child.id);
          return <DisplayTreeItem entry={child} key={child.id} />;
        })}
      </Container>
    </>
  );
};
