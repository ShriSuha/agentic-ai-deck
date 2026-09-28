# bert-base-uncased

## What it does

`bert-base-uncased` is an English language model. It reads text and builds a numeric representation of each word that later models can use for tasks such as classification, named-entity recognition, and extractive question answering.

"Uncased" means the model lowercases words before it reads them, so `Apple` and `apple` look the same. It does not write new paragraphs. It fills in missing words and scores whether one sentence follows another.

## License

Apache License 2.0.

## Training data

It was trained on English Wikipedia and the BookCorpus collection of books.

## Limits

- It handles English text. It is not a translation model.
- It ignores capitalization, so it is a poor fit when uppercase letters carry meaning.
- It reads at most about 512 tokens at a time.
- It can repeat biases present in Wikipedia and books.
- It does not follow chat instructions. A person fine-tunes it, or attaches another model, before using it for a specific job.
