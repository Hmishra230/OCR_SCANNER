OCR_SCANNER ⚡
A lightweight yet powerful desktop OCR (Optical Character Recognition) tool that extracts printed text from images, screenshots, and PDF pages using Tesseract. Designed for fast and accurate text capture with minimal setup.

📋 Description
The OCR Scanner enables users to quickly retrieve text from visual sources. It supports batch processing, image pre-processing, and delivers results via both CLI and GUI. Ideal for productivity workflows, research, and data entry tasks.

🧩 Features
Tesseract-based OCR for multi-language support (English by default)

CLI interface for single or multiple image processing

Optional GUI for intuitive drag‑and‑drop operation

Image pre-processing: grayscale conversion, thresholding

Support for PNG, JPEG, TIFF, and PDF inputs (converted to images)

Configurable output formats: plain text, JSON, or clipboard copy

Error handling with user-friendly messages

🗂️ Project Structure
pgsql
Copy
Edit
OCR_SCANNER/
├── ocr_scanner.py         # Main CLI & GUI entrypoint
├── ocr_engine.py          # Tesseract OCR wrapper & preprocessing
├── file_utils.py          # Image loading, format conversion
├── gui_interface.py       # (Optional) drag‑and‑drop GUI setup
├── config.py              # Default settings & thresholds
├── requirements.txt       # Dependencies (e.g. pytesseract, pillow)
└── README.md              # Project overview & usage guide
🚀 Getting Started
Prerequisites
Python 3.7+

Tesseract OCR installed and in your PATH

Windows: Download from UB Mannheim

macOS: brew install tesseract

Linux: sudo apt-get install tesseract-ocr

Installation
bash
Copy
Edit
git clone https://github.com/Hmishra230/OCR_SCANNER.git
cd OCR_SCANNER
pip install -r requirements.txt
🛠️ Usage
Command-Line
bash
Copy
Edit
# Single image processing
python ocr_scanner.py --input ./images/doc1.png --lang eng

# Batch processing
python ocr_scanner.py --input ./images/ --output results.txt

# Clipboard mode
python ocr_scanner.py --input image.png --clipboard
GUI Mode
bash
Copy
Edit
python ocr_scanner.py --gui
Drag & drop images onto the window

Click “Process” to start OCR

Copy, save, or view text directly

⚙️ Configuration
Keys available in config.py:

Setting	Description	Default
OCR_LANG	Language for OCR	"eng"
PREPROCESS_METHOD	Options: "gray", "thresh"	"gray"
OUTPUT_FORMAT	Options: "txt", "json", clipboard	"txt"

📦 Deployment
Package as standalone executable using PyInstaller:

bash
Copy
Edit
pip install pyinstaller
pyinstaller --onefile ocr_scanner.py
🎯 Contributing
Contributions welcome! Submit issues and pull requests via GitHub.

🔒 License
Distributed under the MIT License. See LICENSE for details.
