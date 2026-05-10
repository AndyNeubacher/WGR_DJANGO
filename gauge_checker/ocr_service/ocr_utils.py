import os
import cv2
import numpy as np
from typing import Optional, Dict
from .obj_detection import ObjDetection

try:
    from pyzbar import pyzbar
except ImportError:
    pyzbar = None

try:
    from pylibdmtx import pylibdmtx
except ImportError:
    pylibdmtx = None

ROBOFLOW_API_KEY = "hyav9bBDrlwRh16JGxo8"
GAUGE_MODEL_ID = "watermeter-vtc1a/4"
DIGIT_MODEL_ID = "gaugenumbers/2"


def detect_rotation(image: np.ndarray) -> int:
    """
    Detect the skew of a meter crop in degrees, rounded to the nearest int.
    """
    if image is None or image.size == 0:
        return 0

    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)

        min_len = max(20, min(image.shape[:2]) // 4)
        lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80,
                                minLineLength=min_len, maxLineGap=20)
        if lines is None:
            return 0

        angles = []
        for x1, y1, x2, y2 in lines[:, 0]:
            a = np.degrees(np.arctan2(y2 - y1, x2 - x1))
            if a < -45:
                a += 90
            elif a > 45:
                a -= 90
            angles.append(a)

        return int(round(float(np.median(angles))))
    except Exception:
        return 0


def rotate_image(image: np.ndarray, angle: float) -> np.ndarray:
    """Rotate image around its center by angle degrees."""
    if image is None or angle == 0:
        return image

    h, w = image.shape[:2]
    M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
    cos, sin = abs(M[0, 0]), abs(M[0, 1])
    new_w = int(h * sin + w * cos)
    new_h = int(h * cos + w * sin)
    M[0, 2] += (new_w - w) / 2
    M[1, 2] += (new_h - h) / 2
    return cv2.warpAffine(image, M, (new_w, new_h),
                          flags=cv2.INTER_CUBIC, borderValue=(255, 255, 255))


def barcode_robust_decode(image: np.ndarray) -> list:
    """
    Attempts to decode barcodes using multiple libraries and preprocessing steps.
    Returns a unified list of decoded objects.
    """
    if image is None:
        return []

    results = []

    if pyzbar:
        try:
            results.extend(pyzbar.decode(image))
        except Exception:
            pass

    if pylibdmtx:
        try:
            results.extend(pylibdmtx.decode(image))
        except Exception:
            pass

    if results:
        return results

    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        padded = cv2.copyMakeBorder(gray, 30, 30, 30, 30, cv2.BORDER_CONSTANT, value=255)
        _, thresh = cv2.threshold(padded, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        if pyzbar:
            try:
                results.extend(pyzbar.decode(thresh))
            except Exception:
                pass

        if pylibdmtx:
            try:
                results.extend(pylibdmtx.decode(thresh))
            except Exception:
                pass

        if not results:
            resized = cv2.resize(thresh, (0, 0), fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
            if pyzbar:
                try:
                    results.extend(pyzbar.decode(resized))
                except Exception:
                    pass
            if pylibdmtx:
                try:
                    results.extend(pylibdmtx.decode(resized))
                except Exception:
                    pass

    except Exception:
        pass

    return results


def run_ocr(image_path: str) -> Dict[str, Optional[str]]:
    """
    Run OCR on an image and extract serial number and meter reading.
    Returns a dictionary with 'serial_number' and 'consumed_volume' keys.
    """
    result = {
        'serial_number': None,
        'consumed_volume': None,
        'error': None
    }

    try:
        if not os.path.isfile(image_path):
            result['error'] = f"Invalid file path: {image_path}"
            return result

        try:
            img = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        except Exception:
            img = cv2.imread(image_path)

        if img is None:
            result['error'] = "Could not load image"
            return result

        obj_detection_model = ObjDetection(
            api_key=ROBOFLOW_API_KEY,
            model_id=GAUGE_MODEL_ID,
            offline_mode=True
        )
        digit_detection_model = ObjDetection(
            api_key=ROBOFLOW_API_KEY,
            model_id=DIGIT_MODEL_ID,
            offline_mode=True
        )

        consumption_probe = obj_detection_model.getBBoxImage(img, "consumption")
        rotation = detect_rotation(consumption_probe)
        if rotation != 0:
            img = rotate_image(img, rotation)

        serial_number: Optional[str] = None
        barcode_img = obj_detection_model.getBBoxImage(img, "barcode")
        if barcode_img is not None:
            for obj in barcode_robust_decode(barcode_img):
                try:
                    data = obj.data.decode('utf-8')
                    parts = data.split(';')
                    if parts and parts[0]:
                        serial_number = parts[0]
                        break
                except Exception:
                    pass

        if not serial_number:
            serial_img = obj_detection_model.getBBoxImage(img, "serialnumber")
            if serial_img is not None:
                try:
                    char_bboxes = digit_detection_model.getAllBBoxes(serial_img)
                    char_bboxes.sort(key=lambda b: b["bbox"][0])
                    chars = "".join(str(b.get("class", "")) for b in char_bboxes)
                    if chars:
                        serial_number = chars
                except Exception:
                    pass

        consumed_volume: Optional[str] = None
        consumption_img = obj_detection_model.getBBoxImage(img, "consumption")
        if consumption_img is not None:
            try:
                digit_bboxes = digit_detection_model.getAllBBoxes(consumption_img)
                digit_bboxes.sort(key=lambda b: b["bbox"][0])
                digits = "".join(str(b.get("class", "")) for b in digit_bboxes)
                if digits and digits.replace('.', '').isdigit():
                    consumed_volume = digits
            except Exception:
                pass

        result['serial_number'] = serial_number
        result['consumed_volume'] = consumed_volume
        obj_detection_model.Close()
        digit_detection_model.Close()

    except Exception as e:
        result['error'] = str(e)

    return result
