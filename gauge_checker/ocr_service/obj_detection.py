import os
import base64
import cv2
import numpy as np
import requests
import threading
import sys

os.environ.setdefault("CORE_MODEL_SAM_ENABLED",  "False")
os.environ.setdefault("CORE_MODEL_SAM2_ENABLED", "False")
os.environ.setdefault("CORE_MODEL_SAM3_ENABLED", "False")
os.environ.setdefault("CORE_MODEL_GAZE_ENABLED", "False")
os.environ.setdefault("CORE_MODEL_YOLO_WORLD_ENABLED", "False")
os.environ.setdefault("CORE_MODEL_CLIP_ENABLED", "False")
os.environ.setdefault("CORE_MODEL_GROUNDINGDINO_ENABLED", "False")
os.environ.setdefault("DISABLE_VERSION_CHECK", "True")
os.environ.setdefault("INFERENCE_WARNINGS_DISABLED", "True")
os.environ.setdefault("METRICS_ENABLED", "False")
os.environ.setdefault("PALIGEMMA_ENABLED", "False")
os.environ.setdefault("FLORENCE2_ENABLED", "False")
os.environ.setdefault("QWEN_2_5_ENABLED", "False")
os.environ.setdefault("QWEN_3_ENABLED", "False")
os.environ.setdefault("SMOLVLM2_ENABLED", "False")
os.environ.setdefault("DEPTH_ESTIMATION_ENABLED", "False")
os.environ.setdefault("MOONDREAM2_ENABLED", "False")
os.environ.setdefault("CORE_MODEL_PE_ENABLED", "False")

if getattr(sys, 'frozen', False):
    _base_dir = os.path.dirname(os.path.abspath(sys.executable))
else:
    _base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

cache_dir = os.path.join(_base_dir, "roboflow_cache")
os.environ.setdefault("MODEL_CACHE_DIR", cache_dir)
os.environ.setdefault("INFERENCE_CACHE_DIR", cache_dir)
os.environ.setdefault("CORE_MODEL_CACHE_DIR", cache_dir)
os.environ.setdefault("ONNXRUNTIME_EXECUTION_PROVIDERS", "[CPUExecutionProvider]")
os.environ.setdefault("MPLBACKEND", "Agg")

if os.name == 'nt':
    import shutil
    def mock_symlink(src, dst, *args, **kwargs):
        if os.path.exists(dst):
            return
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)
    os.symlink = mock_symlink


class ObjDetection:
    def __init__(self, api_key: str, model_id: str, api_url: str = 'https://serverless.roboflow.com', offline_mode: bool = False):
        self.api_url = api_url
        self.api_key = api_key
        self.model_id = model_id
        self.offline = offline_mode

        self._local_model = None
        self._is_loading = False
        self._local_model_failed = False
        self._model_loaded_callback = None
        self._closing = False
        self._load_thread = None

        if self.offline:
            self._load_thread = threading.Thread(target=self._load_local_model, daemon=True)
            self._load_thread.start()

    def set_model_loaded_callback(self, callback):
        self._model_loaded_callback = callback

    def Close(self):
        self._closing = True
        if hasattr(self, '_load_thread') and self._load_thread is not None:
            if self._load_thread.is_alive():
                self._load_thread.join(timeout=1.0)

    def _encode_frame(self, frame: np.ndarray) -> str:
        success, buffer = cv2.imencode('.jpg', frame)
        if not success:
            raise ValueError("Could not encode frame as JPEG")
        return base64.b64encode(buffer).decode('utf-8')

    def _load_local_model(self):
        if self._is_loading:
            return

        self._is_loading = True
        try:
            from inference import get_model
            self._local_model = get_model(self.model_id, api_key=self.api_key)

            if self._model_loaded_callback:
                self._model_loaded_callback("VisionModel loaded")
        except Exception as e:
            self._local_model = None
            self._local_model_failed = True

            if self._model_loaded_callback:
                self._model_loaded_callback("VisionModel failed")
        finally:
            self._is_loading = False

    def getAllBBoxes(self, image: np.ndarray) -> list:
        bboxes = []
        try:
            if self.offline:
                if getattr(self, '_closing', False) or self._local_model is None:
                    if getattr(self, '_local_model_failed', False):
                        return []
                    if not self._is_loading:
                        self._load_thread = threading.Thread(target=self._load_local_model, daemon=True)
                        self._load_thread.start()
                    return []

                results = self._local_model.infer(image)
                if not results:
                    return []
                if not isinstance(results, list):
                    results = [results]

                all_preds = []
                for r in results:
                    preds = getattr(r, 'predictions', None)
                    if preds:
                        all_preds.extend(preds)

                for pred in all_preds:
                    x = getattr(pred, 'x', None)
                    y = getattr(pred, 'y', None)
                    w = getattr(pred, 'width', None)
                    h = getattr(pred, 'height', None)
                    cls = getattr(pred, 'class_name', getattr(pred, 'class', ''))
                    conf = getattr(pred, 'confidence', 0.0)
                    if all(v is not None for v in (x, y, w, h)):
                        x0, y0 = int(x - w / 2), int(y - h / 2)
                        x1, y1 = int(x + w / 2), int(y + h / 2)
                        bboxes.append({"bbox": [x0, y0, x1, y1], "class": cls, "confidence": conf})
        except Exception as e:
            pass

        return bboxes

    def getBBoxImage(self, image: np.ndarray, class_name: str) -> np.ndarray | None:
        bboxes = self.getAllBBoxes(image)
        for bbox_info in bboxes:
            if bbox_info.get("class") == class_name:
                x0, y0, x1, y1 = bbox_info.get("bbox")

                h, w = image.shape[:2]
                x0 = max(0, min(x0, w))
                y0 = max(0, min(y0, h))
                x1 = max(0, min(x1, w))
                y1 = max(0, min(y1, h))

                if x1 > x0 and y1 > y0:
                    return image[y0:y1, x0:x1]
        return None
