import config from "./config";

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

export { sendToOutbox };