import { Container } from "@mui/material";
import React from "react";
import TimelineEntry from "./TimelineEntry";

const buildTree = (conversation) => {
  let root = null;
  let idToElement = {};
  let parents = {};

  for (let entry of conversation) {
    // console.log(entry);
    idToElement[entry.id] = entry;
    const entryData = entry.data;
    if (!entryData?.inReplyTo) {
      root = entryData?.id;
    } else {
      if (!parents[entryData.inReplyTo]) {
        parents[entryData.inReplyTo] = [];
      }
      parents[entryData.inReplyTo].push(entryData.id);
    }
  }

  for (let parent of Object.keys(parents)) {
    if (!idToElement[parent]) {
      idToElement[parent] = {};
    }
    const childrenIds = Array.from(new Set(parents[parent]));
    idToElement[parent].children = childrenIds.map((id) => idToElement[id]);
  }

  //   console.log(root, parents);
  return idToElement[root];
};

export const DisplayConversation = ({ conversation, fallback }) => {
  const root = buildTree(conversation);
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
  return (
    <>
      <TimelineEntry entry={entry?.data} seen={entry?.seen} />
      <Container style={{ paddingRight: 0, marginRight: 0 }}>
        {sortedChildren?.map((child) => (
          <DisplayTreeItem entry={child} key={child?.id} />
        ))}
      </Container>
    </>
  );
};
