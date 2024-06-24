from flask import Blueprint, render_template, request, redirect, url_for, send_file, session, flash
from services.service_manager import ServiceManager
from io import BytesIO

main = Blueprint('main', __name__)
service_manager = ServiceManager()

@main.route('/')
def index():
    return render_template('login.html')

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename = file.filename
            file_data = file.read()
            service_manager.upload_file(filename, file_data)
            return redirect(url_for('main.index'))
    return render_template('upload.html')

@main.route('/files')
def list_files():
    files = service_manager.list_files()
    return render_template('files.html', files=files)

@main.route('/download/<int:file_id>')
def download_file(file_id):
    file_record = service_manager.download_file(file_id)
    if file_record:
        filename, file_data = file_record
        return send_file(BytesIO(file_data), download_name=filename, as_attachment=True)
    return redirect(url_for('main.list_files'))

@main.route('/konversi', methods=['GET', 'POST'])
def konversi():
    if request.method == 'POST':
        file_id = request.form['file_id']
        result = service_manager.convert_file(file_id)
        if result:
            return send_file(BytesIO(result), download_name='converted.docx', as_attachment=True)
        else:
            flash('Konversi gagal.')
            return redirect(url_for('main.konversi'))

    files = service_manager.list_files()
    return render_template('konversi.html', files=files)

@main.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if service_manager.login(username, password):
        session['username'] = username  # Simpan username dalam session
        return redirect(url_for('main.dashboard'))
    else:
        return "Login gagal. Silakan coba lagi."

@main.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    else:
        return redirect(url_for('main.index'))
