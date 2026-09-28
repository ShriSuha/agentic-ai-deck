# distilbert-base-uncased

## What it does

`distilbert-base-uncased` is a smaller, faster copy of BERT. It reads English text and produces word representations for classification and similar tasks. "Uncased" means it lowercases the input.

## License

Apache License 2.0.

## Training data

The same kind of English data as BERT: Wikipedia and books. The small model was trained to imitate the full BERT.

## Limits

- It is less accurate than full `bert-base-uncased`.
- It inherits biases from Wikipedia and books.
- It ignores capitalization.
- It does not generate paragraphs or translate text.
