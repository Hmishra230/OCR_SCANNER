from flask import Flask, render_template, request, redirect, url_for, flash
import os
import logging
from werkzeug.utils import secure_filename
from utils.ocr_processor import DocumentProcessor
from PIL import Image

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Ensure upload directory exists and is writable
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    try:
        os.makedirs(app.config['UPLOAD_FOLDER'])
    except Exception as e:
        raise RuntimeError(f"Could not create upload directory: {e}")
if not os.access(app.config['UPLOAD_FOLDER'], os.W_OK):
    raise RuntimeError(f"Upload directory '{app.config['UPLOAD_FOLDER']}' is not writable.")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_input(file):
    if not file or file.filename == '':
        return False, 'No file selected.'
    if not allowed_file(file.filename):
        return False, 'Invalid file type. Only JPG, JPEG, PNG, and PDF are allowed.'
    return True, ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        driver_license = request.files.get('driver_license')
        insurance_card = request.files.get('insurance_card')

        valid_dl, msg_dl = validate_input(driver_license)
        valid_ic, msg_ic = validate_input(insurance_card)
        if not valid_dl or not valid_ic:
            flash(msg_dl if not valid_dl else msg_ic, 'warning')
            return redirect(url_for('index'))

        dl_filename = secure_filename(driver_license.filename)
        ic_filename = secure_filename(insurance_card.filename)
        dl_path = os.path.join(app.config['UPLOAD_FOLDER'], dl_filename)
        ic_path = os.path.join(app.config['UPLOAD_FOLDER'], ic_filename)
        driver_license.save(dl_path)
        insurance_card.save(ic_path)

        return redirect(url_for('process', dl=dl_filename, ic=ic_filename))
    except Exception as e:
        logger.error(f'Error during file upload: {e}', exc_info=True)
        flash('An unexpected error occurred during file upload.', 'danger')
        return redirect(url_for('index'))

@app.route('/process', methods=['GET'])
def process():
    dl_filename = request.args.get('dl')
    ic_filename = request.args.get('ic')
    if not dl_filename or not ic_filename:
        flash('Missing uploaded files for processing.', 'warning')
        return redirect(url_for('index'))
    dl_path = os.path.join(app.config['UPLOAD_FOLDER'], dl_filename)
    ic_path = os.path.join(app.config['UPLOAD_FOLDER'], ic_filename)
    processor = DocumentProcessor()
    try:
        # Check if files exist
        if not os.path.exists(dl_path) or not os.path.exists(ic_path):
            flash('One or both uploaded files could not be found.', 'danger')
            logger.error(f'File not found: {dl_path if not os.path.exists(dl_path) else ic_path}')
            return redirect(url_for('index'))

        # Process Driver License
        try:
            if dl_filename.lower().endswith('.pdf'):
                dl_image = processor.process_pdf(dl_path)
            else:
                dl_image = Image.open(dl_path)
            dl_image = processor.preprocess_image(dl_image)
            dl_text = processor.extract_text(dl_image)
            license_info = processor.extract_license_info(dl_text)
        except Exception as e:
            logger.error(f'OCR processing error for driver license: {e}', exc_info=True)
            flash('Error processing driver license file.', 'danger')
            return redirect(url_for('index'))

        # Process Insurance Card
        try:
            if ic_filename.lower().endswith('.pdf'):
                ic_image = processor.process_pdf(ic_path)
            else:
                ic_image = Image.open(ic_path)
            ic_image = processor.preprocess_image(ic_image)
            ic_text = processor.extract_text(ic_image)
            insurance_info = processor.extract_insurance_info(ic_text)
        except Exception as e:
            logger.error(f'OCR processing error for insurance card: {e}', exc_info=True)
            flash('Error processing insurance card file.', 'danger')
            return redirect(url_for('index'))

        # Validate extracted dates
        def valid_date(dt):
            import datetime
            return isinstance(dt, (datetime.date, datetime.datetime))

        license_issue_date = license_info.get('issue_date')
        license_expiry_date = license_info.get('expiry_date')
        insurance_issue_date = insurance_info.get('issue_date')
        insurance_expiry_date = insurance_info.get('expiry_date')

        if license_issue_date and not valid_date(license_issue_date):
            logger.warning(f'Invalid license issue date extracted: {license_issue_date}')
            flash('Invalid license issue date extracted.', 'warning')
            license_issue_date = ''
        if license_expiry_date and not valid_date(license_expiry_date):
            logger.warning(f'Invalid license expiry date extracted: {license_expiry_date}')
            flash('Invalid license expiry date extracted.', 'warning')
            license_expiry_date = ''
        if insurance_issue_date and not valid_date(insurance_issue_date):
            logger.warning(f'Invalid insurance issue date extracted: {insurance_issue_date}')
            flash('Invalid insurance issue date extracted.', 'warning')
            insurance_issue_date = ''
        if insurance_expiry_date and not valid_date(insurance_expiry_date):
            logger.warning(f'Invalid insurance expiry date extracted: {insurance_expiry_date}')
            flash('Invalid insurance expiry date extracted.', 'warning')
            insurance_expiry_date = ''

        return render_template(
            'result.html',
            license_info=license_info,
            insurance_info=insurance_info
        )
    except Exception as e:
        logger.error(f'Error processing documents: {e}', exc_info=True)
        flash('An unexpected error occurred during document processing.', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 