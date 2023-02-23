import config from "./config";

import { db } from "./database";
import { transformActivity } from "./utils/transformInboxEntry";
const sendToOutbox = (activity) => {
  return fetch(config.outbox, {
    method: "post",
    headers: {
      "Content-Type": "application/activity+json",
      Authorization: `Bearer ${config.accessToken}`,
    },
    body: JSON.stringify(activity),
  }).catch(console.error);
};

const sendFetch = (url, useAdd) => {
  return fetch(config.proxyUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
      Authorization: `Bearer ${config.accessToken}`,
    },
    body: new URLSearchParams({ id: url }),
  })
    .then((x) => x.json())
    .then(async (data) => {
      const activity = transformActivity(data);
      if (useAdd) {
        await db.activity.add(activity);
      } else {
        await db.activity.put(activity);
      }
    });
};

export { sendToOutbox, sendFetch };
