from base64 import encode
from json import JSONEncoder, load
import json
import cv2
import numpy as np

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

def serialize_image(data):
    img  = cv2.imread(data)
    serialized_image = json.dumps(img, cls=NumpyArrayEncoder)
    return serialized_image

# [[
# ]]

def deserialize_image(data):
    image_data = json.loads(data)
    deserialized_image = np.array(image_data, dtype=np.uint8)
    return deserialized_image

def show_image(img):
    deserialized_image = deserialize_image(img)
    cv2.imshow('Image', deserialized_image)
    cv2.waitKey(0)
