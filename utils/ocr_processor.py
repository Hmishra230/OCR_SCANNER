import re
import datetime
import numpy as np
import cv2
from PIL import Image
import fitz  # PyMuPDF
from paddleocr import PaddleOCR

class DocumentProcessor:
    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='en')

    def process_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        page = doc.load_page(0)  # first page
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        return img

    def preprocess_image(self, image):
        if image.width > 2000:
            ratio = 2000 / image.width
            new_size = (2000, int(image.height * ratio))
            image = image.resize(new_size, Image.ANTIALIAS)
        return image

    def extract_text(self, image):
        result = self.ocr.ocr(np.array(image), cls=True)
        text_list = [line[1][0] for line in result[0]] if result and result[0] else []
        return text_list

    def extract_license_info(self, text_list):
        name = None
        issue_date = None
        expiry_date = None

        # Look for name
        for i, line in enumerate(text_list):
            upper_line = line.upper()
            if any(key in upper_line for key in ["NAME", "HOLDER"]):
                # Try to extract name after the keyword
                parts = re.split(r':|\s{2,}', line)
                for part in parts:
                    if any(key in part.upper() for key in ["NAME", "HOLDER"]):
                        idx = parts.index(part)
                        if idx + 1 < len(parts):
                            name = parts[idx + 1].strip()
                        elif i + 1 < len(text_list):
                            name = text_list[i + 1].strip()
                        break
                if name:
                    break
            elif "DL NO" in upper_line and i + 1 < len(text_list):
                # Sometimes name is after DL NO
                name = text_list[i + 1].strip()
                break

        # Look for issue date
        for line in text_list:
            upper_line = line.upper()
            if any(key in upper_line for key in ["ISSUED", "ISS", "DATE OF ISSUE"]):
                dates = self.extract_dates([line])
                if dates:
                    issue_date = dates[0]
                    break

        # Look for expiry date
        for line in text_list:
            upper_line = line.upper()
            if any(key in upper_line for key in ["EXPIRES", "EXP", "EXPIRY"]):
                dates = self.extract_dates([line])
                if dates:
                    expiry_date = dates[0]
                    break

        expired = None
        if expiry_date:
            expired = self.is_expired(expiry_date)

        return {
            'name': name,
            'issue_date': issue_date,
            'expiry_date': expiry_date,
            'expired': expired
        }

    def extract_insurance_info(self, text_list):
        name = None
        issue_date = None
        expiry_date = None

        # Look for policyholder name
        for i, line in enumerate(text_list):
            upper_line = line.upper()
            if any(key in upper_line for key in ["INSURED", "POLICY HOLDER", "NAME"]):
                parts = re.split(r':|\s{2,}', line)
                for part in parts:
                    if any(key in part.upper() for key in ["INSURED", "POLICY HOLDER", "NAME"]):
                        idx = parts.index(part)
                        if idx + 1 < len(parts):
                            name = parts[idx + 1].strip()
                        elif i + 1 < len(text_list):
                            name = text_list[i + 1].strip()
                        break
                if name:
                    break

        # Look for issue/effective date
        for line in text_list:
            upper_line = line.upper()
            if any(key in upper_line for key in ["EFFECTIVE", "POLICY DATE", "ISSUED"]):
                dates = self.extract_dates([line])
                if dates:
                    issue_date = dates[0]
                    break

        # Look for expiry date
        for line in text_list:
            upper_line = line.upper()
            if any(key in upper_line for key in ["EXPIRES", "EXPIRY", "ENDS"]):
                dates = self.extract_dates([line])
                if dates:
                    expiry_date = dates[0]
                    break

        expired = None
        if expiry_date:
            expired = self.is_expired(expiry_date)

        return {
            'name': name,
            'issue_date': issue_date,
            'expiry_date': expiry_date,
            'expired': expired
        }

    def extract_dates(self, text_list):
        date_patterns = [
            r'\b(\d{2}[\/\-.]\d{2}[\/\-.]\d{4})\b',  # DD/MM/YYYY, DD-MM-YYYY, DD.MM.YYYY
            r'\b(\d{4}[\/\-.]\d{2}[\/\-.]\d{2})\b',  # YYYY/MM/DD, YYYY-MM-DD, YYYY.MM.DD
        ]
        found_dates = []
        for text in text_list:
            for pattern in date_patterns:
                matches = re.findall(pattern, text)
                for date_str in matches:
                    dt = self.parse_date_string(date_str)
                    if dt:
                        found_dates.append(dt)
        return found_dates

    def parse_date_string(self, date_str):
        date_formats = [
            "%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y",
            "%m/%d/%Y", "%m-%d-%Y", "%m.%d.%Y",
            "%Y/%m/%d", "%Y-%m-%d", "%Y.%m.%d",
        ]
        for fmt in date_formats:
            try:
                return datetime.datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    def is_expired(self, date_obj):
        return date_obj < datetime.datetime.now() 