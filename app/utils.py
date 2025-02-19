from PIL import Image
import io


def compress_image(image, max_size_kb=1000):
    """
    Resize and compress an image to fit within a specified maximum KB limit.
    If the image size is already smaller than or equal to the limit, no changes are made.

    :param image: The image file (Django model image field or a BytesIO object)
    :param max_size_kb: The maximum allowed image size in KB (e.g., 1000KB)
    :return: A BytesIO object of the compressed image or the original image if no compression is needed
    """
    img = Image.open(image)

    img_io = io.BytesIO()
    img.save(img_io, format='JPEG', quality=95)
    img_size_kb = img_io.tell() / 1024

    if img_size_kb <= max_size_kb:
        image.seek(0)
        return image

    quality = 85
    while True:
        img_io = io.BytesIO()
        img.save(img_io, format='JPEG', quality=quality)
        img_size_kb = img_io.tell() / 1024

        if img_size_kb <= max_size_kb or quality <= 10:
            break
        quality -= 5

    img_io.seek(0)
    return img_io
