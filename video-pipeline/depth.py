"""Depth-based 2.5D parallax: MiDaS-small (ONNX, CPU) estimates depth, frames are warped so near things
move more than far things as the virtual camera drifts."""
import os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "models", "midas_small.onnx")
_sess = None


def depth_map(path):
    """Normalized inverse depth (1 = nearest) at the image's resolution, cached next to the image."""
    cache = path.rsplit(".", 1)[0] + "_depth.npy"
    if os.path.exists(cache):
        return np.load(cache)
    global _sess
    if _sess is None:
        import onnxruntime as ort
        _sess = ort.InferenceSession(MODEL, providers=["CPUExecutionProvider"])
    img = Image.open(path).convert("RGB")
    x = np.asarray(img.resize((256, 256), Image.BICUBIC), np.float32) / 255.0
    x = (x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]
    out = _sess.run(None, {_sess.get_inputs()[0].name: x.transpose(2, 0, 1)[None].astype(np.float32)})[0][0]
    out = (out - out.min()) / max(1e-6, out.max() - out.min())
    d = Image.fromarray((out * 255).astype(np.uint8)).resize(img.size, Image.BICUBIC)
    d = d.filter(ImageFilter.GaussianBlur(radius=max(2, img.size[0] // 200)))  # soft edges hide warp seams
    d = np.asarray(d, np.float32) / 255.0
    np.save(cache, d)
    return d


def warp(rgb, depth, dx, dy, zoom=1.0, focus=0.35):
    """Backward-warp rgb (H, W, C uint8) so pixels shift by (depth - focus) * (dx, dy); bilinear sampling."""
    h, w = depth.shape
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    k = depth - focus
    cx, cy = w / 2, h / 2
    sx = (xs - cx) / zoom + cx - k * dx
    sy = (ys - cy) / zoom + cy - k * dy
    np.clip(sx, 0, w - 1.001, out=sx)
    np.clip(sy, 0, h - 1.001, out=sy)
    x0 = sx.astype(np.int32); y0 = sy.astype(np.int32)
    fx = (sx - x0)[..., None]; fy = (sy - y0)[..., None]
    a = rgb[y0, x0].astype(np.float32); b = rgb[y0, x0 + 1]
    c = rgb[y0 + 1, x0]; d = rgb[y0 + 1, x0 + 1]
    top = a * (1 - fx) + b * fx
    bot = c * (1 - fx) + d * fx
    return (top * (1 - fy) + bot * fy).astype(np.uint8)
