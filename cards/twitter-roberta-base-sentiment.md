# twitter-roberta-base-sentiment

## What it does

`twitter-roberta-base-sentiment` labels a short English post as negative, neutral, or positive. It is RoBERTa fine-tuned on tweets.

## License

MIT License.

## Training data

Tweets collected for sentiment benchmarks, on top of RoBERTa's English pretraining.

## Limits

- Three labels only. It does not explain why a post feels that way.
- Tweets are a biased sample of how people write. The model can treat dialect and identity words unfairly.
- It is a poor fit for long articles or for text in other languages.
- It does not translate and it does not see images.
