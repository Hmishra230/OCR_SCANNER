import subprocess
import sys
import os

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"\u2713 Success: {cmd}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\u2717 Failed: {cmd}")
        print(f"Error: {e.stderr}")
        return False

print("=== Installing CPU-Only Dependencies ===")

# Uninstall any existing paddlepaddle
print("Cleaning existing installations...")
subprocess.run([sys.executable, "-m", "pip", "uninstall", "paddlepaddle", "-y"], capture_output=True)

# Install packages with timeout and retries
commands = [
    f"{sys.executable} -m pip install --upgrade pip",
    f"{sys.executable} -m pip install Flask==2.3.3 --timeout=300",
    f"{sys.executable} -m pip install Pillow==10.0.1 --timeout=300",
    f"{sys.executable} -m pip install numpy==1.24.3 --timeout=300",
    f"{sys.executable} -m pip install opencv-python==4.8.1.78 --timeout=300",
    f"{sys.executable} -m pip install PyMuPDF==1.23.5 --timeout=300",
    f"{sys.executable} -m pip install python-dateutil==2.8.2 --timeout=300",
    f"{sys.executable} -m pip install werkzeug==2.3.7 --timeout=300"
]

for cmd in commands:
    if not run_command(cmd):
        print(f"Retrying {cmd}...")
        run_command(cmd)

# Install CPU-only PaddlePaddle with multiple fallback methods
print("\n=== Installing CPU-Only PaddlePaddle ===")
paddle_commands = [
    f"{sys.executable} -m pip install paddlepaddle==2.5.1 -i https://pypi.tuna.tsinghua.edu.cn/simple/ --timeout=1000",
    f"{sys.executable} -m pip install paddlepaddle==2.5.1 -i https://pypi.douban.com/simple/ --timeout=1000",
    f"{sys.executable} -m pip install paddlepaddle==2.5.1 --timeout=1000 --retries=3",
    f"{sys.executable} -m pip install paddlepaddle --timeout=1000"
]

paddle_installed = False
for cmd in paddle_commands:
    print(f"Trying: {cmd}")
    if run_command(cmd):
        paddle_installed = True
        break

if not paddle_installed:
    print("\u274C PaddlePaddle installation failed. Try manual installation.")
    sys.exit(1)

# Install PaddleOCR
print("\n=== Installing PaddleOCR ===")
ocr_commands = [
    f"{sys.executable} -m pip install paddleocr==2.7.0.3 --timeout=600",
    f"{sys.executable} -m pip install paddleocr --timeout=600"
]

for cmd in ocr_commands:
    if run_command(cmd):
        break

print("\n=== Installation Complete ===")
print("\u2713 All dependencies installed successfully!")
print("You can now continue with the Flask application development.")

# Verify installation
try:
    import paddleocr
    print("\u2713 PaddleOCR import successful")
except ImportError as e:
    print(f"\u2717 PaddleOCR import failed: {e}") 