import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = ui_path = os.getenv(
    "TESSERACT_PATH", r"E:\Program Files\Tesseract-OCR\tesseract.exe")
