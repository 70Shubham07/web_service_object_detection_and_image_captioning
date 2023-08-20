from bs4 import BeautifulSoup
from PIL import Image
import urllib.request
import numpy as np


# query = 'cars+with+dents'
    
def getUrlsForSearchQuery( query ):
    url="https://www.google.co.in/search?q="+query+"&source=lnms&tbm=isch"


    headers = {}
    headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    req = urllib.request.Request(url, headers=headers)
    resp = urllib.request.urlopen(req)
    respData = str(resp.read())

    data = str(respData)


    imageUrls = []
    while True:

        idxHttps = data.find( "https://" )
        if idxHttps == -1:
            print("found no https")
            break

        idxImageFormat = data.find(".jpg")

        if idxImageFormat == -1:
            idxImageFormat = data.find(".png")
            if idxImageFormat == -1:
                print("found no image format")
                break

        print("Found https and image format both")
        print(idxHttps, idxImageFormat)

        concernedString = data[idxHttps: idxImageFormat+4]

        # The way would be: iteratively look for the next https till no more can be found between https and the image format.

        while True:

            # concerned string contains entire string from https to image format's last index
            # so skip the first 8 idcs to find next https
            dataToFindMoreHttps = concernedString[8:]

            # print(dataToFindMoreHttps)

            idxHttpsSubString = dataToFindMoreHttps.find("https://")

            if idxHttpsSubString == -1:
                print("nope")
                break

            print("yep")
            concernedString = dataToFindMoreHttps[ idxHttpsSubString :  ]

            # print( concernedString )        
            # dataToFindMoreHttps = concernedString[ idxHttpsSubString+8: ]

        # If there is any non url material in the string, then it doesn't qualify as a URL

        if " " in concernedString or "http" in concernedString[8:]: 
            print("came here")   
            data = data[ idxImageFormat+4 :  ]
            continue

        urlString = concernedString

        imageUrls.append( urlString )

        data = data[ idxImageFormat+4 :  ]

        # print( urlString )

    finalUrls = []
    counter = 0
    for imgUrl in imageUrls:
        if counter == 3:
            break
        if len(imgUrl) != 0:
            finalUrls.append(imgUrl)
            counter += 1

    return finalUrls



