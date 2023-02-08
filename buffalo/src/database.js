import Dexie from "dexie";

export const db = new Dexie("activities");
db.version(1).stores({
  activity: "&id, conversation, seen",
});
db.version(2).stores({
  activity: "&id, conversation, seen, updated",
});
db.version(3).stores({
  activity: "&id, conversation, seen, updated, remoteId",
});
db.version(4).stores({
  activity: "&id, conversation, seen, displayed, updated, remoteId",
});
db.version(5).stores({
  activity: "&id, conversation, seen, displayed, updated, remoteId",
  meta: "&key",
});
