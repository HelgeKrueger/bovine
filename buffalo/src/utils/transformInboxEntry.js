const transformInboxEntry = (entry) => {
  let data = entry[1];
  let remoteId = entry[0];
  if (data.type === "Create" || data.type === "Update") {
    data = data?.object;
  }
  const id = data?.id;
  const conversation = data?.conversation;
  let seen = 0;
  const displayed = 0;

  if (data.type === "Announce") {
    seen = 1;
  }

  let updated = data?.updated;
  if (!updated) {
    updated = data?.published;
  }

  return {
    id,
    conversation,
    seen,
    updated,
    data,
    displayed,
    remoteId,
  };
};

export default transformInboxEntry;
