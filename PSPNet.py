from keras.models import load_model
from keras.utils import get_file
from keras import layers
from keras.backend import tf as ktf
import cv2
import numpy as np
import random


class Interp(layers.Layer):
    def __init__(self, new_size, **kwargs):
        self.new_size = new_size
        super(Interp, self).__init__(**kwargs)

    def build(self, input_shape):
        super(Interp, self).build(input_shape)

    def call(self, inputs, **kwargs):
        new_height, new_width = self.new_size
        resized = ktf.image.resize_images(inputs, [new_height, new_width], align_corners=True)
        return resized

    def compute_output_shape(self, input_shape):
        return tuple([None, self.new_size[0], self.new_size[1], input_shape[3]])

    def get_config(self):
        config = super(Interp, self).get_config()
        config['new_size'] = self.new_size
        return config


def get_image_arr(path, width, height):
    if type(path) is np.ndarray:
        img = path
    else:
        img = cv2.imread(path, 1)
        
    img = cv2.resize(img, (width, height))
    img = img.astype(np.float32)
    img[:,:,0] -= 103.939
    img[:,:,1] -= 116.779
    img[:,:,2] -= 123.68
    img = img[:,:,::-1]
    return img


def predict_segmentation(input_name, output_name):
    random.seed(0)
    class_colors = [(random.randint(0,255),random.randint(0,255),random.randint(0,255)) for _ in range(5000)]
    
    model_url = "https://getfile.dokpub.com/yandex/get/https://yadi.sk/d/BR1EAlZ-UQMzQQ"
    model_config = get_file('PSP-Net.h5', model_url)
    model = load_model(model_config, custom_objects={'Interp': Interp})

    inp = cv2.imread(input_name)
    orininal_h = inp.shape[0]
    orininal_w = inp.shape[1]
    output_width = output_height = input_width = input_height = 473
    n_classes = 21

    x = get_image_arr(inp, input_width, input_height)
    pr = model.predict(np.array([x]))[0]
    pr = pr.reshape((output_height, output_width, n_classes)).argmax(axis=2)
    
    seg_img = np.zeros((output_height, output_width, 3))
    colors = class_colors

    for c in range(n_classes):
        seg_img[:,:,0] += ((pr[:,: ] == c)*(colors[c][0])).astype('uint8')
        seg_img[:,:,1] += ((pr[:,: ] == c)*(colors[c][1])).astype('uint8')
        seg_img[:,:,2] += ((pr[:,: ] == c)*(colors[c][2])).astype('uint8')

    seg_img = cv2.resize(seg_img, (orininal_w, orininal_h))
    cv2.imwrite(output_name, seg_img)