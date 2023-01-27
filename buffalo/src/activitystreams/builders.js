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

export { buildLike };
