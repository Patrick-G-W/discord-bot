from google_images_download import google_images_download

response = google_images_download.googleimagesdownload()

arguments = {"keywords": "Polar bears", "limit": 1, "print_urls": True}
#paths = response.download(arguments)
#paths = response.build_url_parameters(arguments)
#print(paths)
