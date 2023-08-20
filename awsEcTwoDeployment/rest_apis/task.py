import sys
from collections import Counter

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
from rest_apis.imageUrlsGoogleSearch import getUrlsForSearchQuery
from rest_apis.build_vocab import Vocabulary

from rest_apis.subTask import getImageCaption

import pathlib



print("Imports done and image paths ready")



# The task function below will take the image path
# Find the objects in it
# Create a search query from it
# Use the image scraping code (in image_stuff/image_urls_google_search.py)
# to find the image URLs,
# Take random 5 image URLs from the list created

# Read image from those URLs and save to the image path

# Return the names of these images to the front end. -> Or maybe the whole path will also work



def runTaskToDetectObjectsInGivenImage( taskInputDict ):

    print(app.instance_path)

    pathToInstance = app.instance_path.replace("/instance", "")
    print("This is the path now", pathToInstance)

    imageUrls = []

    pathToReadImageFrom = taskInputDict["pathToReadImageFrom"]


    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if taskInputDict["modelToUse"] == "objects":


        PATH_TO_CKPT =  os.path.join(  pathToInstance, app.config["PATH_TO_CKPT"])
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



        # Detection
        with detection_graph.as_default():
            with tf.Session(graph=detection_graph) as sess:


                image_np = np.array(Image.open(pathToReadImageFrom))

                image_np_expanded = np.expand_dims(image_np, axis=0)

                if len(image_np_expanded.shape )>4:
                    print("t")
                    image_np_expanded = np.squeeze( image_np_expanded, axis = (0,) )

                elif len(image_np_expanded.shape)<4:
                    image_np_expanded = np.array(image_np_expanded, ndmin=4)
                    
                if image_np_expanded.shape[3]>3:
                    print("u")
                    image_np_expanded = image_np_expanded[:,:,:,:3]

                print("image_np_expanded.shape: ", image_np_expanded.shape)




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
                # https://stackoverflow.com/questions/40430186/tensorflow-valueerror-cannot-feed-value-of-shape-64-64-3-for-tensor-uplace
                # Cannot feed value of shape (1, 400, 400, 4) for Tensor 'image_tensor:0', which has shape '(?, ?, ?, 3)
                (boxes, scores, classes, num_detections) = sess.run(
                    [boxes, scores, classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})

                print( boxes, '\n', scores, '\n', classes, '\n', num_detections )
                print("Detection completed. ")

                # https://stackoverflow.com/questions/47627395/printing-class-name-and-score-in-tensorflow-object-detection-api
                # https://stackoverflow.com/questions/44088706/cannot-convert-a-ndarray-into-a-tensor-or-operation-error-when-trying-to-fetc
                threshold = 0.5
                listOfDetectedObjects = []
                for index, value in enumerate(classes[0]):
                    object_dict = {}
                    if scores[0, index] > threshold:
                        object_dict[(category_index.get(value)).get('name').encode('utf8')] = \
                                  scores[0, index]
                        listOfDetectedObjects.append(object_dict)


                print ("These are predicted objects: ", listOfDetectedObjects)

                print("((((((((((((((((((((((((((((((((())))))))))))))))))))))))))))))))))")


        # return objects
        detectedObjects = []
        for objectDict in listOfDetectedObjects:
            keys = list( objectDict.keys() )
            key = keys[0]
            detectedObjects.append( key.decode() )
            # objectDict[ key.decode() ] = objectDict[ key ]
            del objectDict[key]


        if len(detectedObjects) == 0:
            # imageUrls = [os.path.join(  pathToInstance, app.config["OBJECT_NOT_FOUND"])]
            imageUrls = ["static/img/notFound.png"]
            return imageUrls

        # This is an example of what counterDict would contain
        # {
        #   "dog": 2
        # }
        counterDict = Counter( detectedObjects )


        # Now, code to generate a query from the counterDict OR the detected objects and their quantities

        searchQueryOne = "Photographs+of+"

        idx=0
        for objectName, totalCount in counterDict.items():

            if idx>0:
                searchQueryOne += "+" + "and" + "+" + str( totalCount ) + "+" + "+".join(objectName.split())
            else:
                searchQueryOne += str( totalCount ) + "+" + "+".join(objectName.split())

            idx += 1


        imageUrls = getUrlsForSearchQuery( searchQueryOne )

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~`

    else:
        searchQueryTwo = getImageCaption( pathToReadImageFrom )

        # searchQueryTwo = "+".join(searchQueryTwo.split(" "))

        imageUrls = getUrlsForSearchQuery( searchQueryTwo ) 

    return imageUrls


