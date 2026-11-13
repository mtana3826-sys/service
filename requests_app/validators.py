from django.core.exceptions import ValidationError
from PIL import Image

MAX_SIZE = 10 * 1024 * 1024

def validate_photo(photo):
    if photo.size > MAX_SIZE:
        raise ValidationError("Размер фотографии не должен превышать 10 МБ.")

    try:
        image = Image.open(photo)
        if image.format not in ["JPEG", "PNG", "WEBP"]:
            raise ValidationError("Разрешены только JPEG, PNG и WEBP.")

        image.verify()
        photo.seek(0)

    except (OSError, Image.UnidentifiedImageError):
        raise ValidationError("Файл не является корректным изображением.")