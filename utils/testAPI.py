import requests
from werkzeug.datastructures import FileStorage
import io
import numpy as np
from PIL import Image
import cv2


def plotData(image, winname="noname"):

    cv2.namedWindow(winname)  # Create a named window
    cv2.moveWindow(winname, 40, 30)  # Move it to (40,30)
    cv2.imshow(winname, image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


def test_open_image():
    f = open('..\\hue.jpg', 'rb')
    file = FileStorage(f)
    file.save("file_storage_image.jpg")

    content = file.read()
    print(">> Content of file storgae : " + str(content))
    f.close()


def test_image2nuparray():
    f = open('..\\hue.jpg', 'rb')
    file = FileStorage(f)
    binary_array = file.read()
    print(">> Content in test : " + str(binary_array))
    img = Image.open(io.BytesIO(binary_array))
    arr = np.asarray(img)
    plotData(arr)
    print(">> NP array " + str(arr))
    f.close()


def test_request_multipart():
    f = open('..\\hue.jpg', 'rb')
    file = FileStorage(f)
    temp = file.read()
    print(">> Client content : " + str(temp))
    response = requests.post('http://127.0.0.1:5000/roomtemp', files=dict(file=file))
    print(">> Request response : " + str(response))
    f.close()


def test_request_json():
    json_data = {"sensor": "hue", "data": "array of values" }
    response = requests.post('http://127.0.0.1:5000/roomtemp', json=json_data)
    print(">> " + str(response))

def create_user():
    json_data = {"username": "admin", "password": "megadeth96"}
    response = requests.post("http://127.0.0.1:5000/register", json=json_data)
    print(">>  Resp : " + str(response))

def test_login():
    json_data = {"username":"admin", "password":"megadeth96"}
    response = requests.post("http://127.0.0.1:5000/login", json=json_data)
    print(">> resp : " + str(response))
    import json
    bearer= json.loads(response.text)['token']
    print(">> resp : " + str(bearer))

    header = {'x-access-token': bearer}
    resp = requests.get("http://127.0.0.1:5000/roomtemp", headers=header)
    print(">> Raspuns : " + str(resp.text))


if __name__ == "__main__":
    # test_request_multipart()
    # test_image2nuparray()
    # test_request_json()
    # create_user()
    test_login()
    import datetime
    # print(datetime.datetime.utcnow())