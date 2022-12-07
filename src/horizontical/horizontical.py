from typing import Tuple
from PIL import Image, ImageFilter


def image_box_fit(image: Image, box: Tuple[int, int]) -> Image:
    """Return a copy of `image` that completely (and snugly) fits `box`."""

    box_w, box_h = box
    cur_w, cur_h = image.size

    # Use the smaller of the horizontal and vertical scaling ratios
    # to ensure the image fits the box.
    horz_scale_ratio = box_w / cur_w
    vert_scale_ratio = box_h / cur_h
    if horz_scale_ratio < vert_scale_ratio:
        new_w = box_w
        new_h = int(horz_scale_ratio * cur_h)
    else:
        new_w = int(vert_scale_ratio * cur_w)
        new_h = box_h
    return image.resize((new_w, new_h))


def image_box_fill(image: Image, box: Tuple[int, int]) -> Image:
    """Return a copy of `image` that completely fills `box`, preserving
    the original aspect ratio of `image` and centering any overspill."""

    box_w, box_h = box
    cur_w, cur_h = image.size

    # Use the larger of the horizontal and vertical scaling ratios
    # to ensure the image fills the box.  After resizing, crop the
    # resized image to fit the box (centering it).
    scale_ratio = max((box_w / cur_w), (box_h / cur_h))
    new_w = int(scale_ratio * cur_w)
    new_h = int(scale_ratio * cur_h)
    width_offset = int((new_w - box_w) / 2.0) if new_w > box_w else 0
    height_offset = int((new_h - box_h) / 2.0) if new_h > box_h else 0
    crop_box = (width_offset, height_offset, box_w + width_offset, box_h + height_offset)
    return image.resize((new_w, new_h)).crop(crop_box)


def horizonticalize(image: Image, box: Tuple[int, int]) -> Image:
    """Return an Image comprised of a scaled-to-fit and center copy of `image`
    overlaying a scaled-to-fill and blurred copy of the same."""

    # For the background, we scale the image to fill the box and blur it.
    bg_image = image_box_fill(image, box)
    bg_image = bg_image.filter(ImageFilter.GaussianBlur(16))

    # Now we get a copy of the (original) image scaled to fit the box.
    fg_image = image_box_fit(image, box)

    # Finally, we paste the fitted image atop the blurred background and
    # return the result.
    box_w, box_h = box
    new_w, new_h = fg_image.size
    width_offset = int((box_w - new_w) / 2.0) if box_w > new_w else 0
    height_offset = int((box_h - new_h) / 2.0) if box_h > new_h else 0
    bg_image.paste(fg_image, (width_offset, height_offset))
    return bg_image

