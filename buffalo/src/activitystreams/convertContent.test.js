import { format } from "./convertContent";

test("format adds microformat to quote", () => {
  const original = `
> This is a quote
`;

  const result = format(original);

  expect(result.replaceAll("\n", "")).toBe(
    '<blockquote class="h-quote"><p>This is a quote</p></blockquote>'
  );
});

// test("format deals with math", () => {
//   const original = `
// \\[\\mathrm{e}{\\pi \\mathrm{i}} +1 = 0 \\]
// `;

//   const result = format(original);

//   expect(result.replaceAll("\n", "")).toBe(
//     '<blockquote class="h-quote"><p>This is a quote</p></blockquote>'
//   );
// });
