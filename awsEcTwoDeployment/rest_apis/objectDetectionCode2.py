import sys

import numpy as np
import os
import six.moves.urllib as urllib
import tarfile
import tensorflow as tf
import zipfile

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image

# check in a separate file whether the import would work successfully.
from rest_apis.utils import label_map_util

from rest_apis import app


import pathlib



print("Imports done and image paths ready")

def detectObjectsInGivenImage( pathToReadImageFrom ):

    print(app.instance_path)

    pathToInstance = app.instance_path.replace("/instance", "")
    print("This is the path now", pathToInstance)

    pathToImages = pathToInstance + "/" + app.config["IMAGE_PATH"]

    # PATH_TO_TEST_IMAGES_DIR = pathlib.Path('/home/shubham/Desktop/localStaginMiscProgramming/for_object_detection/models-master/research/object_detection/test_images')
    PATH_TO_TEST_IMAGES_DIR = pathlib.Path(pathToImages)
    TEST_IMAGE_PATHS = sorted(list(PATH_TO_TEST_IMAGES_DIR.glob("*.jpg")))


    # PATH_TO_CKPT =  os.path.join(  pathToInstance, app.config["PATH_TO_CKPT"])
    PATH_TO_CKPT =  pathToInstance + "/" + app.config["PATH_TO_CKPT"]
    PATH_TO_LABELS = os.path.join( pathToInstance, app.config["PATH_TO_LABELS"])

    print("type of path to labels: ", type(PATH_TO_LABELS))

    NUM_CLASSES = app.config["NUM_CLASSES"]

    print( "path to ckpt: ", PATH_TO_CKPT )

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()

        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

    print("detection_graph loaded from model file")
    # Loading label map
    # Label maps map indices to category names, so that when our convolution network predicts `5`, we know that this corresponds to `airplane`.  Here we use internal utility functions, but anything that returns a dictionary mapping integers to appropriate string labels would be fine
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)

    categories = label_map_util.convert_label_map_to_categories(
        label_map, max_num_classes=NUM_CLASSES, use_display_name=True)

    category_index = label_map_util.create_category_index(categories)

    print("Loaded mapping data from label maps and created category_index")

    # Helper code
    # def load_image_into_numpy_array(image):
    #     (im_width, im_height) = image.size
    #     return np.array(image.getdata()).reshape(
    #         (im_height, im_width, 3)).astype(np.uint8)


    # Detection
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # for image_path in TEST_IMAGE_PATHS:
                # print( "type of image inside the session", type(image_np) )
                # image_np = np.array(image_np)


            image_np = np.array(Image.open(pathToReadImageFrom))

            image_np_expanded = np.expand_dims(image_np, axis=0)
            # Extract image tensor
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Extract detection boxes
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Extract detection scores
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            # Extract detection classes
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            # Extract number of detectionsd
            num_detections = detection_graph.get_tensor_by_name(
                'num_detections:0')
            # Actual detection.
            (boxes, scores, classes, num_detections) = sess.run(
                [boxes, scores, classes, num_detections],
                feed_dict={image_tensor: image_np_expanded})

            print( boxes, '\n', scores, '\n', classes, '\n', num_detections )
            print("Detection completed. ")

            # https://stackoverflow.com/questions/47627395/printing-class-name-and-score-in-tensorflow-object-detection-api
            # https://stackoverflow.com/questions/44088706/cannot-convert-a-ndarray-into-a-tensor-or-operation-error-when-trying-to-fetc
            threshold = 0.5
            objects = []
            for index, value in enumerate(classes[0]):
                object_dict = {}
                if scores[0, index] > threshold:
                    object_dict[(category_index.get(value)).get('name').encode('utf8')] = \
                              scores[0, index]
                    objects.append(object_dict)


            print ("These are predicted objects: ", objects)

            print("((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))")

    return objects































