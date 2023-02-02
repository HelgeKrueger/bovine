import { db } from "../database";
import transformInboxEntry from "./transformInboxEntry";

import config from "../config";
async function addActivity(timeline) {
  try {
    await db.activity.bulkAdd(timeline.map(transformInboxEntry));
  } catch (error) {
    // console.error(error);
  }
}

const reloadTimeline = async () => {
  const minArrayList = await db.activity
    .orderBy("remoteId")
    .reverse()
    .limit(1)
    .toArray();
  let min_id = 0;
  if (minArrayList.length > 0) {
    min_id = minArrayList[0].remoteId;
  }
  fetch(`${config.inbox}?min_id=${min_id}`, {
    headers: {
      Authorization: `Bearer ${config.accessToken}`,
      Accept: "application/activity+json",
    },
  })
    .then((x) => x.json())
    .then((x) => addActivity(x));
};

export { reloadTimeline };
