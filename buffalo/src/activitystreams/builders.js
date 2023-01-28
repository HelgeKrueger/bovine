import { v4 as uuidv4 } from "uuid";
import { marked } from "marked";

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

const buildSource = (content) => {
  return {
    content: content,
    mediaType: "text/markdown",
  };
};

const buildTag = (hashtags, mentions) => {
  let tags = [];
  if (hashtags) {
    tags = tags.concat(
      hashtags?.map((x) => {
        return { name: x, type: "Hashtag" };
      })
    );
  }
  if (mentions) {
    tags = tags.concat(
      mentions?.map((x) => {
        return { href: x, name: x, type: "Mention" };
      })
    );
  }

  return tags;
};

const buildNote = (actor, content, properties) => {
  const id = actor + "/" + uuidv4();
  const formatted = marked.parse(content);
  let to = ["https://www.w3.org/ns/activitystreams#Public"];
  let cc = [actor + "/followers"];
  // if (properties?.to) {
  //   to = properties.to;
  // }
  if (properties?.replyToActor) {
    cc.push(properties?.replyToActor);
  }
  // if (properties?.cc) {
  //   cc = properties.cc;
  // }
  if (properties?.mentions) {
    cc = cc.concat(properties.mentions);
  }
  to = Array.from(new Set(to));
  cc = Array.from(new Set(cc));
  return {
    "@context": "https://www.w3.org/ns/activitystreams",
    atomUri: id,
    attachment: [],
    attributedTo: actor,
    cc: cc,
    content: formatted,
    contentMap: {
      en: content,
    },
    conversation: properties?.conversation,
    id: id,
    inReplyTo: properties?.inReplyTo,
    inReplyToAtomUri: properties?.inReplyToAtomUri,
    published: currentDate(),
    tag: buildTag(properties?.hashtags, properties?.mentions),
    replies: {
      type: "Collection",
      totalItems: 0,
      items: [],
    },
    source: buildSource(content),
    to: to,
    type: "Note",
    url: id.replace("/activitypub", ""),
  };
};

const buildCreateForNote = (note) => {
  const copyOfNote = { ...note };
  if (copyOfNote["@context"]) {
    delete copyOfNote["@context"];
  }
  return {
    "@context": [
      "https://www.w3.org/ns/activitystreams",
      {
        atomUri: "ostatus:atomUri",
        inReplyToAtomUri: "ostatus:inReplyToAtomUri",
        conversation: "ostatus:conversation",
        ostatus: "http://ostatus.org#",
      },
    ],
    actor: note?.attributedTo,
    cc: note?.cc,
    id: note?.id + "/activity",
    object: copyOfNote,
    published: note?.published,
    to: note?.to,
    type: "Create",
  };
};

export { buildLike, buildCreateForNote, buildNote };
