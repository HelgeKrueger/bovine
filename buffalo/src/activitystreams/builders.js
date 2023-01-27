import { v4 as uuidv4 } from "uuid";

const currentDate = () => new Date().toISOString();

const buildLike = (actor, object) => {
  return {
    "@context": "https://www.w3.org/ns/activitystreams",
    type: "Like",
    id: actor + "/like-" + uuidv4(),
    actor: actor,
    object: object?.id,
    to: [object?.attributedTo],
    // published: currentDate(),
  };
};

const buildNote = (actor, content, properties) => {
  return {
    "@context": "https://www.w3.org/ns/activitystreams",
    attributedTo: actor,
    cc: [actor + "/followers"],
    content: `<p>${content}</p>`,
    id: actor + "/" + uuidv4(),
    inReplyTo: null,
    published: currentDate(),
    hashtags: properties?.hashtags,
    to: ["https://www.w3.org/ns/activitystreams#Public"],
    type: "Note",
  };
};

const buildCreateForNote = (note) => {
  return {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      {
        inReplyToAtomUri: "ostatus:inReplyToAtomUri",
        conversation: "ostatus:conversation",
        ostatus: "http://ostatus.org#",
      },
    ],
    actor: note?.attributedTo,
    cc: note?.cc,
    id: note?.id + "/activity",
    object: note,
    published: note?.published,
    to: note?.to,
    type: "Create",
  };
};

export { buildLike, buildCreateForNote, buildNote };
