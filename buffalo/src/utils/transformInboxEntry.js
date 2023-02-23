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
    if (!data.object.startsWith("https://mymath")) {
      seen = 1;
    }
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

const transformActivity = (data, entryId) => {
  if (data.type === "Create" || data.type === "Update") {
    const actor = data?.actor;
    data = data?.object;
    if (data.attributedTo === actor?.id) {
      data.attributedTo = actor;
    }
  }
  const id = data?.id;
  const conversation = data?.conversation;
  let seen = 0;
  const displayed = 0;

  if (data.type === "Announce") {
    if (!data.object.startsWith("https://mymath")) {
      seen = 1;
    }
  }

  if (["Tombstone", "Delete"].indexOf(data.type) > -1) {
    seen = 1;
  }

  let updated = data?.updated;
  if (!updated) {
    updated = data?.published;
  }

  let remoteId = 0;
  if (entryId) {
    remoteId = parseInt(entryId, 10);
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

export { transformInboxEntry, transformActivity };
