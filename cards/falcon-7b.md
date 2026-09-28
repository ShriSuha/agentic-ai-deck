# falcon-7b

## What it does

`falcon-7b` generates English text. It is a 7-billion-parameter model trained mostly on web pages. It completes a prompt. It is not an image model and it is not a dedicated translator.

## License

Apache License 2.0.

## Training data

RefinedWeb, a filtered set of public web pages, plus some curated text.

## Limits

- It can state false claims with a confident tone.
- Web training data contains social biases, and the model can repeat them.
- This base model is not tuned for chat.
- It has no tool for opening a file or searching a folder.
