import os

from rembg import remove
from PIL import Image


def ensure_folder(folder):
    os.makedirs(
        folder,
        exist_ok=True
    )


def get_file_size(file_path):
    try:
        return os.path.getsize(
            file_path
        )
    except Exception:
        return 0


def is_valid_image(file_path):

    if not os.path.exists(
        file_path
    ):
        return False

    if not file_path.lower().endswith(
        (
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        )
    ):
        return False

    try:
        with Image.open(
            file_path
        ) as img:
            img.verify()

        return True

    except Exception:
        return False


def get_image_info(file_path):

    try:

        with Image.open(
            file_path
        ) as img:

            return {
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode
            }

    except Exception:

        return None


def remove_background(
    input_path,
    output_path
):

    if not os.path.exists(
        input_path
    ):
        raise FileNotFoundError(
            "Input image not found"
        )

    if not is_valid_image(
        input_path
    ):
        raise ValueError(
            "Invalid image"
        )

    ensure_folder(
        os.path.dirname(
            output_path
        ) or "."
    )

    with open(
        input_path,
        "rb"
    ) as f:

        input_data = f.read()

    output_data = remove(
        input_data
    )

    with open(
        output_path,
        "wb"
    ) as f:

        f.write(
            output_data
        )

    return output_path


def process_telegram_image(
    image_path,
    output_folder="data/output"
):

    ensure_folder(
        output_folder
    )

    name = os.path.splitext(
        os.path.basename(
            image_path
        )
    )[0]

    output_path = os.path.join(
        output_folder,
        f"{name}_nobg.png"
    )

    return remove_background(
        image_path,
        output_path
    )


def delete_file(file_path):

    try:

        if os.path.exists(
            file_path
        ):
            os.remove(
                file_path
            )

        return True

    except Exception:

        return False


def clear_folder(folder):

    if not os.path.exists(
        folder
    ):
        return

    for file in os.listdir(
        folder
    ):

        path = os.path.join(
            folder,
            file
        )

        try:

            if os.path.isfile(
                path
            ):
                os.remove(
                    path
                )

        except Exception:
            pass