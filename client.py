import requests
import cv2
import json
import base64
import numpy as np

url = 'http://47.93.19.29:12345'
url = 'http://localhost:12345'
if __name__ =='__main__':

    test_file = r'G:\tmp_show.png'
    img = cv2.imread(test_file)
    retval, buffer = cv2.imencode('.jpg', img)
    filedata = base64.b64encode(buffer).decode('ascii')

    # filedata = base64.b64decode(filedata)
    # filedata = np.fromstring(filedata, np.uint8)
    # img = cv2.imdecode(filedata, cv2.IMREAD_COLOR)

    data = {'filename': 'aaa.jpg', 'filedata': filedata}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    print(r.url, r.text)
