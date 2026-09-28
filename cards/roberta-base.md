# roberta-base

## What it does

`roberta-base` reads English text and builds word representations, like BERT, with a longer and cleaner training recipe. People fine-tune it for classification, tagging, and question answering over a given passage.

## License

MIT License.

## Training data

A large mix of public English text, including Wikipedia, books, news, and web crawl data.

## Limits

- It does not write free-form answers by itself. A task-specific head is added first.
- It can reflect biases in news and web text.
- It is English-first.
- It does not accept images.
