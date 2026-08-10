"""
Resize an uploaded preview image to a manageable width, saved as WebP.
"""
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image

PREVIEW_IMAGE_WIDTH = 800


def resize_image(image, width=PREVIEW_IMAGE_WIDTH):
    """Return a WebP-encoded ``ContentFile`` of ``image`` resized to ``width``."""
    im = Image.open(image)
    w, h = im.size
    ratio = w / h
    height = int(width / ratio)
    im = im.resize((width, height))

    buffer = BytesIO()
    im.save(buffer, format="WebP", quality=90)
    new_image = ContentFile(buffer.getvalue())
    buffer.close()
    return new_image
