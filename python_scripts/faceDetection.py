import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import cv2
import math
import datetime
import time
import sys


MODEL_PATH = 'D:\Coding\Python\Selfie Segmenter\model\selfie_multiclass_256x256.tflite'

DESIRED_HEIGHT = 480
DESIRED_WIDTH = 480

BG_COLOR = (0, 0, 0) 
MASK_COLOR = (255, 255, 255) 

BaseOptions = mp.tasks.BaseOptions
ImageSegmenter = mp.tasks.vision.ImageSegmenter
ImageSegmenterOptions = mp.tasks.vision.ImageSegmenterOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = ImageSegmenterOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.IMAGE,
    )

segmenter = ImageSegmenter.create_from_options(options)

def show_image(image):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    newFile = f'./imageFile/image-{timestr}.jpg'
    cv2.imwrite(newFile, image)
    print(newFile)

def resize_and_show(image):
  h, w = image.shape[:2]
  if h < w:
    img = cv2.resize(image, (DESIRED_WIDTH, math.floor(h/(w/DESIRED_WIDTH))))
  else:
    img = cv2.resize(image, (math.floor(w/(h/DESIRED_HEIGHT)), DESIRED_HEIGHT))
  show_image(img)



def find_face_and_show(filename):

    image = mp.Image.create_from_file(filename)  # opening image as a mediapipe.Image
    segmented_masks = segmenter.segment(image)      # getting output by feeding image to the model
    # print(segmented_masks)


    confidence_masks = segmented_masks.confidence_masks
    # category_mask = segmented_masks.category_mask

    hair = confidence_masks[1]
    face = confidence_masks[3]

    # print(hair.numpy_view().shape)
    # print(face.numpy_view().shape)



    image_data = image.numpy_view()
    bg_image = np.zeros(image_data.shape, dtype=np.uint8)
    bg_image[:] = BG_COLOR

    original_image = cv2.imread(filename)

    # condition = np.stack((category_mask.numpy_view(), ) * 3, axis= -1) > 0.2
    condition1 = np.stack((hair.numpy_view(), ) * 3, axis= -1) > 0.2 
    condition2 = np.stack((face.numpy_view(), ) * 3, axis = -1) > 0.2

    final_condition = np.logical_or(condition1, condition2)

    output_image = np.where(final_condition, original_image, bg_image)

    resize_and_show(output_image)








noOfArguments = len(sys.argv)

if noOfArguments != 2:
    sys.exit(400)


# imageFileName = './image.jpeg'
imageFileName = sys.argv[1]


find_face_and_show(imageFileName)





















