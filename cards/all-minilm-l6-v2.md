# all-MiniLM-L6-v2

## What it does

`all-MiniLM-L6-v2` turns a sentence into a vector so that similar sentences land near each other. People use it to search text. It does not translate and it does not classify images.

## License

Apache License 2.0.

## Training data

More than a billion sentence pairs from public sources, used to train the MiniLM student model.

## Limits

- It returns numbers, not an answer sentence.
- It is weaker on long documents than on single sentences.
- It was trained mostly on English-style text.
- It cannot read an image.
