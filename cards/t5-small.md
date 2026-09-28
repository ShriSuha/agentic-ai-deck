# t5-small

## What it does

`t5-small` treats every job as text in, text out. The same model can summarize, answer a question, or translate text when the input starts with a short task name such as "translate English to German:".

## License

Apache License 2.0.

## Training data

The Colossal Clean Crawled Corpus, a large cleaned slice of public web text, plus supervised task examples.

## Limits

- The small size is much weaker than larger T5 models.
- Translation is only one of its tasks, and it is not as strong as a dedicated translation model.
- Pretraining is English-heavy, so other languages suffer.
- It was not trained as a chat assistant.
