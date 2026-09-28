# whisper-tiny

## What it does

`whisper-tiny` transcribes speech. You give it audio and it returns text. It can also translate spoken language into English text. It does not translate a written document, and it does not look at images.

## License

MIT License.

## Training data

A large set of weakly labeled audio and transcripts collected from the web.

## Limits

- The tiny size makes more word errors than the larger Whisper models.
- Overlapping speakers, strong accents, and noisy audio reduce accuracy.
- It is a speech model. A folder of Markdown files is the wrong input.
- It can hallucinate phrases during silence.
