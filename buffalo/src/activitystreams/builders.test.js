import { buildLike, buildNote, buildCreateForNote } from "./builders";

test("test buildLike", () => {
  const result = buildLike("actor", "objectid");

  expect(result["@context"]).toBe("https://www.w3.org/ns/activitystreams");
});

test("test buildNote", () => {
  const result = buildNote("my_actor", "content");

  expect(result.content).toBe("<p>content</p>\n");
  expect(result.contentMap.en).toBe(result.content);

  expect(result.source).toStrictEqual({
    content: "content",
    mediaType: "text/markdown",
  });
  expect(result.tag).toStrictEqual([]);
});

test("test buildNote which is broken", () => {
  const note = buildNote("config.actor", "content", {
    hashtags: "".split(",").map((x) => x.trim()),
    mentions: "".split(",").map((x) => x.trim()),
  });

  expect(note.to).toStrictEqual([
    "https://www.w3.org/ns/activitystreams#Public",
  ]);
  expect(note.cc).toStrictEqual(["config.actor/followers"]);
});

test("test buildNote with hashtags", () => {
  const result = buildNote("my_actor", "content", {
    hashtags: ["#tag1", "#tag2"],
  });

  expect(result.tag).toStrictEqual([
    { name: "#tag1", type: "Hashtag" },
    { name: "#tag2", type: "Hashtag" },
  ]);
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
