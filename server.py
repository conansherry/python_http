from http.server import BaseHTTPRequestHandler, HTTPServer
from http import HTTPStatus
from urllib.parse import urlparse
import os
import cv2
import cgi
import json
import base64
import numpy as np
from lockfile import FileLock

class PythonServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        self._set_headers()

        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.data_json = json.loads(self.data_string)

        self.send_response(200)
        self.end_headers()

        if 'filedata' in self.data_json and 'filename' in self.data_json:
            filedata = base64.b64decode(self.data_json['filedata'])
            filedata = np.fromstring(filedata, np.uint8)
            img = cv2.imdecode(filedata, cv2.IMREAD_COLOR)
            save_file_name = os.path.join('./', self.data_json['filename'])
            lock = FileLock(save_file_name)
            with lock:
                cv2.imwrite(save_file_name, img)
            print('save', self.data_json['filename'])
        else:
            self.wfile.write(b'Hello world')

    def do_GET(self):
        parsed_path = urlparse(self.path)
        filepath = os.path.join('./', parsed_path.path[1:])
        print(filepath)
        if os.path.isfile(filepath):
            self.send_response(200)
            self.send_header("Content-type", "image/jpg")
            self.end_headers()
            lock = FileLock(filepath)
            with lock:
                f = open(filepath, 'rb')
                self.wfile.write(f.read())
                f.close()
        else:
            self.send_response(HTTPStatus.OK)
            self.end_headers()
            self.wfile.write(b'Hello world')

if __name__ =='__main__':
    sever = HTTPServer(('', 12345), PythonServer)
    print('Starting server, use <Ctrl-C> to stop')
    sever.serve_forever()
