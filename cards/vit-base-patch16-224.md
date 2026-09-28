# vit-base-patch16-224

## What it does

`vit-base-patch16-224` classifies images. It cuts a picture into small patches and predicts a label such as "tabby cat" from the ImageNet label set. It does not read or translate text.

## License

Apache License 2.0.

## Training data

ImageNet-21k, then fine-tuned on ImageNet-1k. Inputs are images resized to 224 by 224 pixels.

## Limits

- It only assigns one class from a fixed list. It cannot explain a picture in a sentence.
- It expects a photograph-like image, not a PDF or a spreadsheet.
- Labels outside ImageNet, such as a specific person's name, are out of reach.
- It has no language license to discuss because it does not generate words, but the weights themselves are under Apache 2.0.
