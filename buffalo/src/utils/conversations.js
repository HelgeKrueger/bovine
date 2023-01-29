const determineAncestor = (id, parents) => {
  for (let parent in parents) {
    let list = parents[parent];
    if (list.indexOf(id) > -1) {
      return parent;
    }
  }
};

const buildTree = (conversation, fallback) => {
  let idToElement = {};
  let parents = {};

  for (let entry of conversation) {
    idToElement[entry.id] = entry;
    const entryData = entry.data;
    if (entryData?.inReplyTo) {
      if (!parents[entryData.inReplyTo]) {
        parents[entryData.inReplyTo] = [];
      }
      parents[entryData.inReplyTo].push(entryData.id);
    }
  }

  let currentAncestor = fallback.id;
  let nextAncestor = determineAncestor(currentAncestor, parents);

  while (nextAncestor) {
    currentAncestor = nextAncestor;
    nextAncestor = determineAncestor(currentAncestor, parents);
  }

  for (let parent of Object.keys(parents)) {
    if (!idToElement[parent]) {
      idToElement[parent] = {};
    }
    const childrenIds = Array.from(new Set(parents[parent]));
    idToElement[parent].children = childrenIds.map((id) => idToElement[id]);
  }

  if (!idToElement[currentAncestor]) {
    return;
  }

  return idToElement[currentAncestor];
};

export { buildTree };
