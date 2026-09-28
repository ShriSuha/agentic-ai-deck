# bert-base-NER

## What it does

`bert-base-NER` finds named entities in English text, such as people, organizations, locations, and miscellaneous names. It is BERT fine-tuned for that tagging job.

## License

MIT License.

## Training data

The CoNLL-2003 English newswire set, on top of BERT's Wikipedia and book pretraining.

## Limits

- It only tags four entity types. It does not answer open questions.
- It was tuned on news, so chat messages and scientific names are weaker.
- It does not translate text.
- It does not look at images.
