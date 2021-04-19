import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
from skimage.filters import threshold_local

from src.extractors import *
from src.utils import *


def show(image: np.array, desc='Imagem'):
    cv2.imshow(desc, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_image_text(image: np.array) -> str:
    image = Image.fromarray(image)
    return pytesseract.image_to_string(image)


def get_rois_from_cords(images: list, cords: tuple) -> list:
    x1, x2, y1, y2 = cords
    rois = [image[x1:x2, y1:y2] for image in images]
    return rois


def get_preds(items: list) -> list:
    return [get_image_text(item) for item in items]


def apply_morphological_operations(image: np.array, ks: tuple = (3, 3)) -> tuple:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, ks)
    top_hat = cv2.morphologyEx(image, cv2.MORPH_TOPHAT, kernel)
    black_hat = cv2.morphologyEx(image, cv2.MORPH_BLACKHAT, kernel)
    return kernel, top_hat, black_hat


def get_gray(image: np.array) -> np.array:
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def add_and_subtract(image: np.array, top_hat: np.array, black_hat: np.array) -> tuple:
    add = cv2.add(image, top_hat)
    subtract = cv2.subtract(add, black_hat)
    return add, subtract


def get_thresh(subtract: np.array, offset: int = 35) -> np.array:
    image_threshold = threshold_local(
        subtract, 29, offset=offset, method="gaussian", mode="mirror")

    thresh = (subtract > image_threshold).astype("uint8") * 255
    return cv2.bitwise_not(thresh)


def clean_image(image: np.array) -> tuple:
    gray_image = get_gray(image)
    kernel, top_hat, black_hat = apply_morphological_operations(
        gray_image)
    add, subtract = add_and_subtract(gray_image, top_hat, black_hat)
    thresh = get_thresh(subtract)
    return thresh, add, subtract


def get_image_contours(image: np.array) -> list:
    contours = cv2.findContours(
        image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return imutils.grab_contours(contours)


def draw_rect_from_countours(contours: list) -> list:
    return [cv2.minAreaRect(contour) for contour in contours]


def extract_rois(thresh_image: np.array, min_rect_area: int = 1800,
                 min_rect_height: int = 25, min_rect_width: int = 22) -> list:
    contours = get_image_contours(thresh_image)
    all_rects = draw_rect_from_countours(contours)
    rois_rects = []

    for rect in all_rects:
        rect_height, rect_width = rect[1]
        if rect_height <= 0:
            continue
        rect_area = rect_height*rect_width
        rect_ratio = float(rect_width)/rect_height
        if (rect_area > min_rect_area and rect_height > min_rect_height
                and rect_width > min_rect_width and (rect_ratio > 1 or rect_ratio < 0.5)):
            rois_rects.append(rect)
    return rois_rects


def transform_rect_in_box(rect: np.array) -> np.array:
    box = cv2.boxPoints(rect)
    return np.int0(box)


def get_cords_from_box(box: np.array) -> tuple:
    x = [row[0] for row in box]
    y = [col[1] for col in box]
    return min(x), max(x), min(y), max(y)


def check_is_rotated(rect_angle: float) -> tuple:
    is_rotated = False
    if rect_angle < -45:
        rect_angle += 90
        is_rotated = True
    return rect_angle, is_rotated


def calculate_centroid(x1, x2, y1, y2) -> tuple:
    center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
    size = (int((x2-x1)), int((y2 - y1)))
    return center, size


def crop_all_rois(image: np.array, rects: list, mult_height: float = 0.73,
                  mult_width: float = 0.97, top_height_crop: int = 30) -> tuple:
    crops, angles, data = [], [], []

    for rect in rects:
        box = transform_rect_in_box(rect)
        x1, x2, y1, y2 = get_cords_from_box(box)
        rect_height, rect_width, rect_angle = rect[1][1], rect[1][0], rect[2]
        rect_angle, is_rotated = check_is_rotated(rect_angle)
        center, size = calculate_centroid(x1, x2, y1, y2)
        rotation_matrix = cv2.getRotationMatrix2D(
            (size[0] / 2, size[1] / 2), rect_angle, 1.0)
        cropped = cv2.getRectSubPix(image, size, center)
        cropped = cv2.warpAffine(cropped, rotation_matrix, size)
        cropped_width = rect_width if not is_rotated else rect_height
        cropped_height = rect_height if not is_rotated else rect_width

        rect_ratio = float(cropped_width) / (cropped_height)
        rect_area = float(cropped_width) * cropped_height

        if (rect_ratio < 2 and rect_ratio > 16):
            continue

        cropped_rotated = cv2.getRectSubPix(
            image=cropped,
            patchSize=(int(cropped_width * mult_width),
                       int(cropped_height * mult_height if cropped_height < top_height_crop else cropped_height * 0.9)),
            center=(size[0] / 2, size[1] / 2)
        )
        angles.append(rect_angle)
        crops.append(cropped_rotated)
        data.append((cropped_rotated, rect_area, rect_ratio, rect_angle))

    return data, np.mean(np.array(angles)), np.std(np.array(angles))


def extract_all_informations_from_rois_preds(data: dict, text_preds: list, ratio: float) -> None:
    all_text_size = [len(text.strip()) for text in text_preds]

    if sum(all_text_size) == 0:
        return

    for text in text_preds:
        text = clean_text(text)

        words = len(re.findall(r"\w+", text))
        text_size = len(text.strip())
        if len(text.strip()) == 0:
            continue

        extract_cnh_number(data, text, ratio)
        extract_cpf_cnh(data, text, text_size, ratio)
        extract_rg_cnh(data, text, words, ratio)
        extract_dates_cnh(data, text, text_size, ratio)
        extract_name_cnh(data, text, words, ratio)


def read_all_rois(all_rois: list, mean_rect_angle: np.float64,
                  std_rect_angle: np.float64, crop_roi: tuple = (5, 0)) -> dict:
    data = get_default_data()
    for idx, (roi, roi_area, roi_ratio, roi_angle) in enumerate(all_rois):
        (height, width,) = roi.shape[:2]
        roi = roi[crop_roi[0]:height, crop_roi[1]:width]
        origin_roi = roi.copy()
        gray_roi = roi.copy()
        thresh_roi, _, gray_roi = clean_image(gray_roi)
        roi_preds = get_preds([origin_roi, thresh_roi, gray_roi])
        extract_all_informations_from_rois_preds(data, roi_preds, roi_ratio)
    return data


def extract_information_from_cnh(image: np.array, resize_w: int = 800) -> dict:
    resize_proc = imutils.resize(image, width=resize_w)
    resize_orig = imutils.resize(image, width=resize_w)

    thresh, _, subtract = clean_image(resize_proc)

    rects = extract_rois(thresh)
    rois, mean_angle, std_angle = crop_all_rois(resize_orig, rects)
    data = read_all_rois(rois, mean_angle, std_angle)
    return data
