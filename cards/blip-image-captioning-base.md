# blip-image-captioning-base

## What it does

`blip-image-captioning-base` writes a short caption for an image. You pass in a picture and it returns a sentence about what is in the picture. It works with images.

## License

BSD 3-Clause License.

## Training data

Image and caption pairs from public captioning datasets, including COCO.

## Limits

- Captions are short and can be generic.
- It can invent objects that are not in the picture.
- It does not translate a written paragraph.
- Fine details, such as exact counts and brand names, are unreliable.
