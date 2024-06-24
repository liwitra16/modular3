import psycopg2

class DataManager:
    def __init__(self):
        self.connection_params = {
            'host': 'localhost',
            'database': 'login_example',
            'user': 'postgres',
            'password': 'khanza22'
        }

    def connect_db(self):
        return psycopg2.connect(**self.connection_params)

    def insert_file(self, filename, file_data):
        conn = self.connect_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO pdf_files (filename, file_data) VALUES (%s, %s)", (filename, file_data))
        conn.commit()
        cur.close()
        conn.close()

    def get_files(self):
        conn = self.connect_db()
        cur = conn.cursor()
        cur.execute("SELECT id, filename FROM pdf_files")
        files = cur.fetchall()
        cur.close()
        conn.close()
        return files

    def get_file(self, file_id):
        conn = self.connect_db()
        cur = conn.cursor()
        cur.execute("SELECT filename, file_data FROM pdf_files WHERE id = %s", (file_id,))
        file_record = cur.fetchone()
        cur.close()
        conn.close()
        return file_record

    def get_file_data(self, file_id):
        conn = self.connect_db()
        cur = conn.cursor()
        cur.execute("SELECT file_data FROM pdf_files WHERE id = %s", (file_id,))
        file_record = cur.fetchone()
        cur.close()
        conn.close()
        if file_record:
            return file_record[0]
        return None
