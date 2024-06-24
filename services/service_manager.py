from data_manager.data_manager import DataManager
import cloudmersive_convert_api_client
from cloudmersive_convert_api_client.rest import ApiException
import os
from io import BytesIO

class ServiceManager:
    def __init__(self):
        self.data_manager = DataManager()
        self.api_key = 'af171045-29ee-40f2-9cd4-ba20624e32e1'  # Ganti dengan API Key Anda

    def login(self, username, password):
        # Implementasi sederhana untuk memeriksa username dan password
        return username == 'admin' and password == 'admin'

    def upload_file(self, filename, file_data):
        self.data_manager.insert_file(filename, file_data)

    def list_files(self):
        return self.data_manager.get_files()

    def download_file(self, file_id):
        return self.data_manager.get_file(file_id)

    def convert_file(self, file_id):
        file_data = self.data_manager.get_file_data(file_id)
        if file_data:
            return self.convert_pdf_to_docx(BytesIO(file_data))

    def convert_pdf_to_docx(self, file_data):
        configuration = cloudmersive_convert_api_client.Configuration()
        configuration.api_key['Apikey'] = self.api_key
        api_instance = cloudmersive_convert_api_client.ConvertDocumentApi(cloudmersive_convert_api_client.ApiClient(configuration))
        
        # Simpan file sementara
        temp_filename = 'temp.pdf'
        with open(temp_filename, 'wb') as temp_file:
            temp_file.write(file_data.getbuffer())

        try:
            # Convert PDF to Word DOCX Document
            api_response = api_instance.convert_document_pdf_to_docx(temp_filename)
            os.remove(temp_filename)  # Hapus file sementara
            return api_response
        except ApiException as e:
            os.remove(temp_filename)  # Hapus file sementara jika ada kesalahan
            print("Exception when calling ConvertDocumentApi->convert_document_pdf_to_docx: %s\n" % e)
            return None
