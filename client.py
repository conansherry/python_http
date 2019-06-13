import requests
import cv2
import json
import base64

url = 'http://localhost:12345'
if __name__ =='__main__':

    test_file = r'G:\test_seg.png'
    with open(test_file, 'rb') as image_file:
        filedata = base64.b64encode(image_file.read()).decode('ascii')

    data = {'filename': 'aaa.png', 'filedata': filedata}
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=url, headers=headers, data=json.dumps(data))
    print(r.url, r.text)
