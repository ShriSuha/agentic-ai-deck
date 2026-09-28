# detr-resnet-50

## What it does

`detr-resnet-50` finds objects in images. Given a picture, it returns boxes and class names, such as "person" or "bicycle". The visual backbone is a ResNet-50.

## License

Apache License 2.0.

## Training data

The COCO detection dataset, photographs labeled with object boxes.

## Limits

- It only knows the COCO object classes.
- It works with images, not with plain text files.
- Small or crowded objects are often missed.
- It does not describe the scene in sentences.
