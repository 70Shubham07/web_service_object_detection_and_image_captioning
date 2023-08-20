import os
import numpy as np
from collections import Counter

from rest_apis import app

from flask_restful import Resource

from flask import render_template, request, redirect, make_response, jsonify


from rest_apis.task import runTaskToDetectObjectsInGivenImage

# from rest_apis.task2 import dummyTask

import redis
from rq import Queue, Connection

r = redis.Redis()
q = Queue(connection=r)




import pathlib
import datetime


class HelloWorld(Resource):
    def get(self):
        print( os.path.join( app.instance_path, app.config["PATH_TO_CKPT"] )  )
        return {'hello': 'world'}




@app.route( "/find-images", methods = ["GET", "POST"] )
def createBackGroundObjectDetectionTask():
    # take an image as input through request.files and turn it into numpy array.
    # Then run it through the object detection task
    # Then get the objects and the number of times they occur and prepare a query
    if request.method == "POST":
        if request.files:

            # I am not fully confident about which code to change to get rid of the file size thing,
            # so let's just let it be for now
            print("Hoping to find good news here: ", request.form.to_dict())
            requestDict = request.form.to_dict()
            modelToUse = requestDict["model"]
            print (  dict(request.files)[ "file" ]  ,  "\n", type(dict(request.files)[ "file" ]) ,  "\n", str(dict(request.files)[ "file" ])  )

            print( dir(request.files.keys) )

            imageFile = dict(request.files)[ "file" ]

            print( imageFile.filename )

            pathToInstance = app.instance_path.replace("/instance", "")
            print("This is the path now", pathToInstance)

            pathToImages = pathToInstance + "/" + app.config["IMAGE_PATH"]
            filename = imageFile.filename

            # ADD TIMESTAMP TO THE FILE NAME AND SAVE IT
            timeStamp = str( datetime.datetime.now() )
            timeStamp = timeStamp.replace('-', '_').replace(' ','_').replace(':','_').replace('.', '_')

            fileNameWithTimeStamp = timeStamp + "_" + filename

            imageFile.save(os.path.join(pathToImages, fileNameWithTimeStamp))

            print("Image has been saved")

            # Mow get the image from the path using the file name. Also, add timestamp to the file name.

            fullPathToImage = pathToImages + '/' + fileNameWithTimeStamp

            print("The full path to image: ", fullPathToImage)


            # Converting the path to whatever type pathlib.Path() returns is useful for 
            # opening image using Image.open() 
            pathToReadImageFrom = pathlib.Path( fullPathToImage )

            taskInputDict = {"pathToReadImageFrom": pathToReadImageFrom, "modelToUse" : modelToUse}

            print( "Path to read image from: ", taskInputDict )

            # This is specifically for when running in local env
            task = q.enqueue( runTaskToDetectObjectsInGivenImage, taskInputDict )

            taskId = task.get_id()    

            print( "Task has been queued!: ", task.enqueued_at, task.get_id(), task.get_status() )

            return jsonify( {"taskId" : taskId, "imgPath" : "static/img/"+fileNameWithTimeStamp } )



    return render_template("public/upload_image_ajax_detection.html")


# From the API below, will have to return a template as a json response 
# to the template from which this API is called.
@app.route("/getTheUrlsOfImagesFound", methods = ["GET", "POST"])
def getTheListOfImagesFound():

    # Use below when running with docker

    # with Connection(redis.from_url(app.config["REDIS_URL"])):
    #     q = Queue()
    #     task = q.fetch_job(task_id)



    if request.method == "POST":
        requestDict = request.form.to_dict()

        print( "This is request.get_json: ", request.get_json(), request.json, request.form.to_dict() )

        print( requestDict[ "taskId" ] )

        task = q.fetch_job( requestDict["taskId"] )

        print( "The task: ", task )


        if task.result:

            print( "This is task result: ", task.result)

            responseObject = {
                "status": "success",
                "data": {
                    "task_id": task.get_id(),
                    "task_status": task.get_status(),
                        "task_result": task.result,
                },
            }

        else:
            responseObject = {"status": "not yet"}        



        return jsonify( responseObject )





@app.route( "/getImageDivs", methods = ["GET", "POST"] )
def getImageDivs():

    if request.method == "POST":

        imageUrls = request.form.getlist( "imageUrls[]" )
        print( "List of urls: ", imageUrls )

        return jsonify( { 'divsOfImages': render_template('public/response.html', theUrls = imageUrls ) }  )










