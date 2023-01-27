import { buildLike } from "./builders";

test("test buildLike", () => {
  const result = buildLike("actor", "objectid");

  expect(result["@context"]).toBe("https://www.w3.org/ns/activitystreams");
});
