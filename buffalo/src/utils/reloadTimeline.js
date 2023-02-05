import { db } from "../database";
import { transformActivity } from "./transformInboxEntry";

import config from "../config";

const fetchFromResult = async (url) => {
  fetch(url, {
    headers: {
      Authorization: `Bearer ${config.accessToken}`,
      Accept: "application/activity+json",
    },
  })
    .then((x) => x.json())
    .then(async (result) => {
      if (result?.next && result?.orderedItems?.length > 0) {
        try {
          await db.activity.bulkAdd(result.orderedItems.map(transformActivity));
          await fetchFromResult(result.next);
        } catch (error) {
          return false;
        }
      }
    });
};

const updateFrom = async (url) => {
  fetch(url, {
    headers: {
      Authorization: `Bearer ${config.accessToken}`,
      Accept: "application/activity+json",
    },
  })
    .then((x) => x.json())
    .then(async (result) => {
      if (result.first) {
        await fetchFromResult(result.first);
      }
    });
};

const reloadTimeline = async () => {
  await updateFrom(config.inbox);
  await updateFrom(config.outbox);
};

export { reloadTimeline };
