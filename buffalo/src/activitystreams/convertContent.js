import { marked } from "marked";

const format = (content) => {
  let result = marked.parse(content);

  result = result.replaceAll("<blockquote>", '<blockquote class="h-quote">');

  return result;
};

export { format };
