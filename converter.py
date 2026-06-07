import os
import img2pdf

from PIL import Image
from pdf2image import convert_from_path


def pdf_to_images(
    pdf_path,
    output_dir,
    image_format="PNG",
    dpi=200
):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(
            f"PDF not found: {pdf_path}"
        )

    os.makedirs(
        output_dir,
        exist_ok=True
    )

    pages = convert_from_path(
        pdf_path,
        dpi=dpi
    )

    output_files = []

    for index, page in enumerate(pages):

        ext = image_format.lower()

        output_path = os.path.join(
            output_dir,
            f"page_{index + 1}.{ext}"
        )

        page.save(
            output_path,
            image_format
        )

        output_files.append(
            output_path
        )

    return output_files


def image_to_pdf(
    image_path,
    output_pdf
):
    if not os.path.exists(image_path):
        raise FileNotFoundError(
            image_path
        )

    os.makedirs(
        os.path.dirname(output_pdf)
        or ".",
        exist_ok=True
    )

    with open(
        output_pdf,
        "wb"
    ) as f:

        f.write(
            img2pdf.convert(
                image_path
            )
        )

    return output_pdf


def images_to_pdf(
    image_paths,
    output_pdf
):
    valid_images = [
        image
        for image in image_paths
        if os.path.exists(image)
    ]

    if not valid_images:
        raise ValueError(
            "No valid images found"
        )

    os.makedirs(
        os.path.dirname(output_pdf)
        or ".",
        exist_ok=True
    )

    with open(
        output_pdf,
        "wb"
    ) as f:

        f.write(
            img2pdf.convert(
                valid_images
            )
        )

    return output_pdf


def get_image_info(
    image_path
):
    try:

        img = Image.open(
            image_path
        )

        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode
        }

    except Exception:

        return None


def get_file_size(
    file_path
):
    try:
        return os.path.getsize(
            file_path
        )
    except Exception:
        return 0


def is_pdf(file_name):
    return file_name.lower().endswith(
        ".pdf"
    )


def is_image(file_name):
    return file_name.lower().endswith(
        (
            ".png",
            ".jpg",
            ".jpeg",
            ".webp"
        )
    )


def delete_file(
    file_path
):
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


def clear_folder(
    folder_path
):
    if not os.path.exists(
        folder_path
    ):
        return

    for file in os.listdir(
        folder_path
    ):

        path = os.path.join(
            folder_path,
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