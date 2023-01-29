import { buildTree, getDateForEntry } from "./conversations";

const buildElement = (id, inReplyTo) => {
  return {
    id: id,
    data: {
      id: id,
      inReplyTo: inReplyTo,
    },
  };
};

test("buildTree fallback not in conversation", () => {
  const conversation = [buildElement(1, null), buildElement(2, 1)];
  const fallback = buildElement(3, null);

  const result = buildTree(conversation, fallback);

  expect(result).toBeFalsy();
});

test("buildTree fallback in conversation", () => {
  const conversation = [buildElement(1, null), buildElement(2, 1)];
  const fallback = conversation[1];

  const result = buildTree(conversation, fallback);

  expect(result.id).toStrictEqual(1);
});

test("buildTree fallback is root of conversation", () => {
  const conversation = [buildElement(1, null), buildElement(2, 1)];
  const fallback = conversation[0];

  const result = buildTree(conversation, fallback);

  expect(result.id).toStrictEqual(1);
});

test("getDateForEntry", () => {
  const entry = { updated: "2023-01-27T12:58:26Z" };

  const date = getDateForEntry(entry);

  expect(date.getDate()).toBe(27);
});

test("getDateForEntry with children", () => {
  const entry = {
    updated: "2023-01-27T12:58:26Z",
    children: [
      { updated: "2023-01-28T12:58:26Z" },
      { updated: "2023-01-26T12:58:26Z" },
    ],
  };

  const date = getDateForEntry(entry);

  expect(date.getDate()).toBe(28);
});
