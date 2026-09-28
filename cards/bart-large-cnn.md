# bart-large-cnn

## What it does

`bart-large-cnn` summarizes English news articles. You give it an article and it returns a short summary. It was fine-tuned from BART on the CNN/DailyMail summarization set.

## License

MIT License.

## Training data

BART's general English pretraining, then CNN and DailyMail article-summary pairs.

## Limits

- It is built for news, not for chats, code, or licenses.
- Summaries can drop a crucial fact or slightly change a number.
- It does not translate into another language as its job.
- It does not look at images.
