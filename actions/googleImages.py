from google_images_download import google_images_download
from os import listdir, remove
from os.path import isfile, join
import json
import shutil

response = google_images_download.googleimagesdownload()


def imageSearch(keyword):
    searchKeyword = keyword[8:]
    arguments = {"keywords": searchKeyword, "limit": 1, "print_urls": True, "no_download": True, "extract_metadata": True}
    paths = dict(response.download(arguments))
    onlyfiles = [f for f in listdir("./logs") if isfile(join("./logs", f))][0]
    with open("./logs/{0}".format(onlyfiles)) as json_file:
        data = json.load(json_file)
        remove("./logs/{0}".format(onlyfiles))
        shutil.rmtree("./downloads")
        return data[0]['image_link']
