# bert-base-multilingual-uncased-sentiment

## What it does

`bert-base-multilingual-uncased-sentiment` scores the sentiment of a product review from 1 star to 5 stars. It can read reviews in several European languages. It is not a translator.

## License

Apache License 2.0.

## Training data

Multilingual product reviews, on top of multilingual BERT.

## Limits

- The output is a star rating, not an explanation.
- Languages and review styles outside that training set are weaker.
- It lowercases text, so it drops emphasis from capitals.
- It does not work with images.
