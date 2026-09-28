# flan-t5-small

## What it does

`flan-t5-small` follows short written instructions. You can ask it to summarize, classify, or translate a sentence. It is the small FLAN-tuned version of T5.

## License

Apache License 2.0.

## Training data

T5's web-text pretraining, then a mixture of instruction tasks.

## Limits

- The small size follows instructions poorly compared with larger FLAN-T5 models.
- It can ignore the instruction and ramble.
- It is not grounded in a private document unless you paste the document into the prompt.
- It does not see images.
