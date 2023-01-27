import { buildLike, buildNote, buildCreateForNote } from "./builders";

test("test buildLike", () => {
  const result = buildLike("actor", "objectid");

  expect(result["@context"]).toBe("https://www.w3.org/ns/activitystreams");
});

test("test buildNote", () => {
  const result = buildNote("my_actor", "content");

  expect(result.content).toBe("<p>content</p>");
  expect(result.hashtags).toBeFalsy();
});

test("test buildNote with hashtags", () => {
  const result = buildNote("my_actor", "content", {
    hashtags: ["#tag1", "#tag2"],
  });

  expect(result.hashtags).toStrictEqual(["#tag1", "#tag2"]);
});

test("test buildCreateForNote", () => {
  const note = {
    id: "my_id",
    attributedTo: "my_actor",
    to: "my_to",
    cc: "my_cc",
    published: "my_date",
  };
  const result = buildCreateForNote(note);

  expect(result["@context"]).toContain("https://www.w3.org/ns/activitystreams");
  expect(result.actor).toBe("my_actor");
  expect(result.cc).toBe("my_cc");
  expect(result.to).toBe("my_to");
  expect(result.id).toBe("my_id/activity");
  expect(result.published).toBe("my_date");
});
