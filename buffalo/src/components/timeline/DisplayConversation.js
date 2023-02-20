import { Button, Container, IconButton } from "@mui/material";
import React, { useState } from "react";
import TimelineEntry from "./TimelineEntry";

import { buildTree, getDateForEntry } from "../../utils/conversations";
import { Download } from "@mui/icons-material";

export const DisplayConversation = ({ conversation, fallback }) => {
  if (conversation.length === 0) {
    return <TimelineEntry entry={fallback} />;
  }
  const root = buildTree(conversation, fallback);
  if (!root) {
    return <TimelineEntry entry={fallback} />;
  }

  return (
    <>
      <IconButton
        onClick={() => {
          console.log(root);
        }}
        style={{
          position: "absolute",
          top: 0,
          right: 0,
        }}
      >
        <Download />
      </IconButton>
      <DisplayTreeItem entry={root} />
    </>
  );
};

const isUnseen = (entry) => {
  if (entry?.seen !== 1) {
    return true;
  }

  const children = entry?.children;
  if (children) {
    for (let child of children) {
      if (isUnseen(child)) {
        return true;
      }
    }
  }

  return false;
};

const DisplayTreeItem = ({ entry }) => {
  const [showAll, setShowAll] = useState(false);
  if (!isUnseen(entry)) {
    return <TimelineEntry entry={entry?.data} seen={entry?.seen} />;
  }
  const children = entry?.children;
  let sortedChildren = children?.sort((a, b) => {
    return getDateForEntry(b) - getDateForEntry(a);
  });
  if (!sortedChildren) {
    sortedChildren = [];
  }
  const seen = entry?.seen;

  const unseenChildren = sortedChildren.filter(isUnseen);

  let showMore = "";
  if (!showAll && unseenChildren.length < sortedChildren.length) {
    showMore = <Button onClick={() => setShowAll(true)}>Show More</Button>;
  }

  const childrenToShow = showAll ? sortedChildren : unseenChildren;

  return (
    <>
      <TimelineEntry entry={entry?.data} seen={seen} />
      <Container
        style={{
          paddingRight: 0,
          marginRight: 0,
          marginLeft: 0,
          paddingLeft: "10px",
        }}
      >
        {childrenToShow.map((child) => {
          return <DisplayTreeItem entry={child} key={child.id} />;
        })}
        {showMore}
      </Container>
    </>
  );
};
