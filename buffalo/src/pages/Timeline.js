import React, { useContext } from "react";

import { useSwipeable } from "react-swipeable";
import { DisplayConversation } from "../components/timeline/DisplayConversation";

import PullToRefresh from "react-simple-pull-to-refresh";
import { reloadTimeline } from "../utils/reloadTimeline";
import { EntryContext } from "./Main";

const Timeline = () => {
  const { entry, conversation, updateEntry } = useContext(EntryContext);

  const handlers = useSwipeable({
    onSwipedLeft: updateEntry,
  });

  return (
    <div {...handlers}>
      <PullToRefresh onRefresh={reloadTimeline}>
        <DisplayConversation conversation={conversation} fallback={entry} />
      </PullToRefresh>
    </div>
  );
};

export default Timeline;
