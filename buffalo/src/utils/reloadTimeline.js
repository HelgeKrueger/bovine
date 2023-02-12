import { db } from "../database";
import { transformActivity } from "./transformInboxEntry";

import config from "../config";

const fetchFromResult = async (url, type) => {
  fetch(url, {
    headers: {
      Authorization: `Bearer ${config.accessToken}`,
      Accept: "application/activity+json",
    },
  })
    .then((x) => x.json())
    .then(async (result) => {
      console.log(result);
      if (result?.prev && result?.orderedItems?.length > 0) {
        try {
          await db.activity.bulkAdd(result.orderedItems.map(transformActivity));
          await fetchFromResult(result.prev, type);
        } catch (error) {
          // console.log(error);
          await fetchFromResult(result.prev, type);

          if (result.prev) {
            await db.meta.put({ key: `prev${type}`, value: result["prev"] });
          }
          // await fetchFromResult(result.prev);
        }
      } else {
        if (result.prev) {
          // console.log(result);
          await db.meta.put({ key: `prev${type}`, value: result["prev"] });
        }
      }
    });
};

const updateFrom = async (url, type) => {
  db.meta
    .where("key")
    .equals(`prev${type}`)
    .toArray()
    .then(async (x) => {
      if (x.length > 0) {
        url = x[0].value;
        await fetchFromResult(url, type);
      } else {
        fetch(url, {
          headers: {
            Authorization: `Bearer ${config.accessToken}`,
            Accept: "application/activity+json",
          },
        })
          .then((x) => x.json())
          .then(async (result) => {
            if (result.last) {
              await fetchFromResult(result.last, type);
            }
          });
      }
    });
};

const reloadTimeline = async () => {
  await updateFrom(config.inbox, "inbox");
  await updateFrom(config.outbox, "outbox");
};

export { reloadTimeline };
