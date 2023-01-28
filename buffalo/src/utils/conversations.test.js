import { Experimental_CssVarsProvider } from "@mui/material";
import { buildTree } from "./conversations";

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

  expect(result).toStrictEqual(fallback);
});

test("buildTree fallback in conversation", () => {
  const conversation = [buildElement(1, null), buildElement(2, 1)];
  const fallback = conversation[1];

  const result = buildTree(conversation, fallback);

  expect(result.id).toStrictEqual(1);
});
