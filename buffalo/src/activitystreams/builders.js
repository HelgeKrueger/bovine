import { v4 as uuidv4 } from "uuid";
import { marked } from "marked";

const defaults = {
  likeEmoji: "🐮",
  public: "https://www.w3.org/ns/activitystreams#Public",
};

const currentDate = () => new Date().toISOString();

const buildLike = (actor, object) => {
  return {
    "@context": "https://www.w3.org/ns/activitystreams",
    type: "Like",
    id: actor + "/like-" + uuidv4(),
    actor: actor,
    content: defaults.likeEmoji,
    object: object?.id,
    to: [object?.attributedTo],
    cc: [defaults.public],
    published: currentDate(),
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
      hashtags
        ?.filter((x) => x.length > 0)
        ?.map((x) => {
          return { name: x, type: "Hashtag" };
        })
    );
  }
  if (mentions) {
    tags = tags.concat(
      mentions
        ?.filter((x) => x.length > 0)
        ?.map((x) => {
          return { href: x, name: x, type: "Mention" };
        })
    );
  }

  return tags;
};

const publicToCc = (actor, properties) => {
  let to = [defaults.public];
  let cc = [actor + "/followers"];
  if (properties?.replyToActor) {
    cc.push(properties?.replyToActor);
  }

  if (properties?.mentions) {
    cc = cc.concat(properties.mentions.filter((x) => x.length > 0));
  }
  to = Array.from(new Set(to));
  cc = Array.from(new Set(cc));

  return { to, cc };
};

const buildNote = (actor, content, properties) => {
  const id = actor + "/" + uuidv4();
  const formatted = marked.parse(content);

  const { to, cc } = publicToCc(actor, properties);

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

const buildImage = (actor, imagePath, properties) => {
  const id = actor + "/" + uuidv4();
  const { to, cc } = publicToCc(actor, properties);
  return {
    "@context": "https://www.w3.org/ns/activitystreams",
    atomUri: id,
    attributedTo: actor,
    cc: cc,
    conversation: properties?.conversation,
    id: id,
    inReplyTo: properties?.inReplyTo,
    inReplyToAtomUri: properties?.inReplyToAtomUri,
    published: currentDate(),
    tag: buildTag(properties?.hashtags, properties?.mentions),
    content:
      "Apparently, Mastodon doesn't like Objects of type Image, so I'm adding some text here. My reply is just the image.",
    replies: {
      type: "Collection",
      totalItems: 0,
      items: [],
    },
    to: to,
    type: "Note",
    attachment: [
      {
        type: "Image",
        url: imagePath,
        mediaType: "image/png",
      },
    ],
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

export { buildLike, buildCreateForNote, buildNote, buildImage };
