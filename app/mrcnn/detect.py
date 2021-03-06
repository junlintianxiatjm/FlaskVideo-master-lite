# -*- coding: utf-8 -*-

"""
@author: tjm
@software: PyCharm
@file: detect.py
@time: 2021/9/16 9:48
"""

import os
import sys
import skimage.io

from app import app
from app.mrcnn.config import Config
from datetime import datetime
from pathlib import Path
import cv2

# Root directory of the project
ROOT_DIR = os.getcwd()

# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
# from mrcnn import utils
from app.mrcnn import model as modellib
from app.mrcnn import visualize

# Import COCO config
# sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))  # To find local version
# from samples.coco import coco


# Directory to save h5 and trained model

MODEL_DIR = os.path.join(ROOT_DIR, "app\mrcnn\h5")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(MODEL_DIR, "shapes20210726T1823/mask_rcnn_shapes_0014.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    # utils.download_trained_weights(COCO_MODEL_PATH)
    print("junlintianxia************ h5 model not exist ***********")

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")


class ShapesConfig(Config):
    """Configuration for training on the toy shapes dataset.
    Derives from the base Config class and overrides values specific
    to the toy shapes dataset.
    """
    # Give the configuration a recognizable name
    NAME = "shapes"

    # Train on 1 GPU and 8 images per GPU. We can put multiple images on each
    # GPU because the images are small. Batch size is 8 (GPUs * images/GPU).
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 12  # background + 12 shapes

    # Use small images for faster training. Set the limits of the small side
    # the large side, and that determines the image shape.
    IMAGE_MIN_DIM = 80
    IMAGE_MAX_DIM = 512

    # Use smaller anchors because our image and objects are small
    # RPN_ANCHOR_SCALES = (8 * 6, 16 * 6, 32 * 6, 64 * 6, 128 * 6)  # anchor side in pixels
    RPN_ANCHOR_SCALES = (8 * 2, 16 * 2, 32 * 2, 64 * 2, 128 * 2)

    # Reduce training ROIs per image because the images are small and have
    # few objects. Aim to allow ROI sampling to pick 33% positive ROIs.
    TRAIN_ROIS_PER_IMAGE = 10

    # Use a small epoch since the data is simple
    STEPS_PER_EPOCH = 10

    # use small validation steps since the epoch is small
    VALIDATION_STEPS = 5


# import train_tongue
# class InferenceConfig(coco.CocoConfig):
class InferenceConfig(ShapesConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


# ????????????
class detect_image():

    def __init__(self, imgPath=None):
        self.imgPath = imgPath
        self.config = InferenceConfig()
        # Create model object in inference mode.
        self.model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=self.config)

        # Load weights trained on MS-COCO
        self.model.load_weights(COCO_MODEL_PATH, by_name=True)

        # COCO Class names
        # Index of the class in the list is its ID. For example, to get ID of
        # the teddy bear class, use: class_names.index('teddy bear')
        self.class_names = ['BG', "AJ", "BX", "CJ", "CK", "CR", "FZ", "JG", "PL", "QF", "TJ", "ZC", "ZW"]
        # Load a random image from the images folder
        # file_names = next(os.walk(IMAGE_DIR))[2]
        # image = skimage.io.imread("./images/CJ6798.jpg")
        self.image = skimage.io.imread(imgPath)

    def call(self):
        a = datetime.now()
        # Run detection
        results = self.model.detect([self.image], verbose=1)
        b = datetime.now()
        # Visualize results
        print("time: ", (b - a).seconds)
        r = results[0]

        print("=======", r)

        visualize.display_instances(self.image, r['rois'], r['masks'], r['class_ids'],
                                    self.class_names, r['scores'])


# ????????????
class detect_video():

    def __init__(self, videoPath=None):
        self.videoPath = videoPath
        self.video_capture = cv2.VideoCapture(self.videoPath)

        self.config = InferenceConfig()
        # Create model object in inference mode.
        self.model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=self.config)

        # Load weights trained on MS-COCO
        self.model.load_weights(COCO_MODEL_PATH, by_name=True)

        # COCO Class names
        # Index of the class in the list is its ID. For example, to get ID of
        # the teddy bear class, use: class_names.index('teddy bear')
        self.class_names = ['BG', "AJ", "BX", "CJ", "CK", "CR", "FZ", "JG", "PL", "QF", "TJ", "ZC", "ZW"]

    def do_detect(self):
        a = datetime.now()
        # Run detection
        # TODO ????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        # TODO ??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????
        # ?????????????????????????????????????????????
        video_name = os.path.splitext(os.path.basename(self.videoPath))[0]
        # ?????????????????????????????????????????????????????????????????????results???????????????????????????????????????result???????????????????????? visualize.display_instances??????????????????
        folder_path = os.path.join('results', str(video_name))
        # save_path = os.path.join(ROOT_DIR, folder_path)
        # ??????????????????????????????????????????????????????????????????????????????
        # ??????????????????????????????????????????????????????????????????????????????????????????????????????
        if not Path(folder_path).exists():
            os.makedirs(folder_path)
            print('??????????????????', folder_path)
        else:
            files = os.listdir(folder_path)
            for file in files:
                c_path = os.path.join(folder_path, file)
                os.remove(c_path)
        while True:
            ret, frame = self.video_capture.read()
            if ret:
                # TODO ????????????????????????????????????
                results = self.model.detect([frame], verbose=1)
                b = datetime.now()
                # Visualize results
                print("time: ", (b - a).seconds)
                r = results[0]

                print("=======", r)
                cur_class_id = len(r['class_ids'])
                if cur_class_id:
                    # TODO ??????visualize.display_instances????????????????????????????????????????????????
                    # ?????????????????????file_path??? ????????????????????????????????????????????????????????????????????????
                    visualize.display_instances(frame, r['rois'], r['masks'], r['class_ids'],
                                                self.class_names, folder_path, r['scores'])
            else:
                break
        return folder_path


if __name__ == "__main__":
    # det = detect_image("./images/CJ6798.jpg")
    # det.call()

    root_path = app.config['UP_DIR']  # ????????????????????????
    det = detect_video(
        r"D:\python-workspace\FlaskVideo-master\app\static\video\21-09-13\2202109131608391c1babe4b2204fd0a9fca5e0c1db731d.mp4")
    det.do_detect()
