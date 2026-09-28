# clip-vit-base-patch32

## What it does

`clip-vit-base-patch32` links images and text. You can ask which caption matches a picture, or search images with a phrase. It works with images. It is not a translator of written documents.

## License

MIT License.

## Training data

Hundreds of millions of image and caption pairs collected from the public web.

## Limits

- It scores matches. It does not write a full caption by itself in this base form.
- Web captions contain stereotypes, so the model can reflect those biases.
- It can fail on fine print, counting, and unusual scenes.
- It is not a detector that draws boxes around every object.
