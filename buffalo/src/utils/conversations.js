const determineAncestor = (id, parents) => {
  for (let parent in parents) {
    let list = parents[parent];
    if (list.indexOf(id) > -1) {
      return parent;
    }
  }
};

const buildTree = (conversation, fallback) => {
  let root = null;
  let idToElement = {};
  let parents = {};

  for (let entry of conversation) {
    idToElement[entry.id] = entry;
    const entryData = entry.data;
    if (!entryData?.inReplyTo) {
      root = entryData?.id;
    } else {
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

  // idToElement[fallback.id] = fallback;

  for (let parent of Object.keys(parents)) {
    if (!idToElement[parent]) {
      idToElement[parent] = {};
    }
    const childrenIds = Array.from(new Set(parents[parent]));
    idToElement[parent].children = childrenIds.map((id) => idToElement[id]);
  }

  // console.log(fallback.id, parents);

  return idToElement[currentAncestor];
};

export { buildTree };
