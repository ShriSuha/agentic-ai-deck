# resnet-50

## What it does

`resnet-50` classifies images into ImageNet categories. It is a convolutional network with 50 layers, widely used as a starting point for other image tasks.

## License

Apache License 2.0.

## Training data

ImageNet-1k photographs and their class labels.

## Limits

- One label per image, from a fixed set of about 1,000 classes.
- It does not read text inside the picture reliably.
- It does not translate language.
- Photos that look nothing like ImageNet, such as medical scans, need a different training set.
