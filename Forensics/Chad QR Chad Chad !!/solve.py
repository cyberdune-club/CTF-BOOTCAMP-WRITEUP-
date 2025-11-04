#!/usr/bin/env python3
import os
from PIL import Image, ImageSequence
import numpy as np
import cv2
from pyzbar import pyzbar

IN_GIF = "flag_qr.gif"
OUT_DIR = "qr_outputs"

os.makedirs(OUT_DIR, exist_ok=True)

def save_pil(img, path):
    img.convert("RGBA").save(path)

def pil_to_gray_np(img):
    return np.array(img.convert("L"))

def try_pyzbar(img_pil):
    decoded = pyzbar.decode(img_pil)
    return [d.data.decode(errors="ignore") for d in decoded]

def try_opencv(img_np):
    qr_decoder = cv2.QRCodeDetector()
    data, _, _ = qr_decoder.detectAndDecode(img_np)
    return [data] if data else []

def binarize_np(img_np):
    th = cv2.adaptiveThreshold(img_np,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                               cv2.THRESH_BINARY,11,2)
    _, otsu = cv2.threshold(img_np,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return th, otsu

print("Loading GIF:", IN_GIF)
gif = Image.open(IN_GIF)

frames = []
for i, frame in enumerate(ImageSequence.Iterator(gif)):
    f = frame.convert("RGBA")
    bg = Image.new("RGBA", f.size, (255,255,255,255))
    bg.paste(f, (0,0), f)
    f = bg.convert("RGB")
    frames.append(f)
    save_pil(f, os.path.join(OUT_DIR, f"frame_{i:03d}.png"))

print(f"{len(frames)} frames saved to {OUT_DIR}")

found = set()
for i, f in enumerate(frames):
    texts = try_pyzbar(f)
    texts += try_opencv(pil_to_gray_np(f))
    for t in texts:
        if t:
            found.add(t)
            print(f"Frame {i:03d} → {t}")

if not found:
    print("No flag found per-frame, trying composite methods...")
    stack = np.stack([pil_to_gray_np(f) for f in frames], axis=0).astype(np.float32)
    composites = {
        'mean': np.mean(stack, axis=0).astype(np.uint8),
        'median': np.median(stack, axis=0).astype(np.uint8),
        'max': np.max(stack, axis=0).astype(np.uint8),
    }
    for name, comp in composites.items():
        comp_pil = Image.fromarray(comp)
        comp_path = os.path.join(OUT_DIR, f"composite_{name}.png")
        comp_pil.sa_
