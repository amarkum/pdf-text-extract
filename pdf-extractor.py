# Author @Amar Kumar

import io
import os
import tempfile

from pdf2image import convert_from_path

try:
    import datetime
except ImportError:
    print("Installing Data & Time Python Library.")
    os.system("sudo -H pip install datetime")
    import datetime
try:
    from google.cloud import vision
except ImportError:
    print("Installing Google API Python Library.")
    os.system("sudo -H pip install --ignore-installed --upgrade google-cloud-vision")
    from google.cloud import vision
from google.cloud import vision

try:
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"
except:
    print("Please check if \"key.json\" file exists.")

# Instantiates a Google Vision client
try:
    client = vision.ImageAnnotatorClient()
except:
    print("Can't Instantiate a Google Vision Client.")
    print("Please check your Internet Connection or check if Google API \"key.json\" is available.")
    exit(0)

from google.cloud import vision


# sends a request to google vision API with an image to get the text array.
def get_text_from_image(image_filename):
    # initializing empty file paths list
    path = os.path.join(os.path.dirname(__file__), image_filename)
    print("\nSend Image Scan Request. ")

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print("OK.")

    # returning all image paths
    return texts


# The below method will compare the attribute from regular image with the hd image.
# The method reconciles the attribute of two.
# If the length of HD image is greater , it shall keep it. Vice-versa.
def get_non_truncated_val(text, text_list):
    for x in text_list[1:]:
        if text in x.description or x.description in text:
            if len(x.description) > len(text):
                return x.description
    return text


src_filename = "example.pdf"

# Algorithm : 2 Image of the PDF will be created
# Regular Image + HD Image
# Google Vision API might truncate the value in either of regular or HD Image.
# We pass the regular image and reconcile the value with HD Image and keep the data with maximum character.
# This removed the un-necessary truncation of value.


# Read The PDF in Regular mode, and extract the required Image
print("\nScanning PDF | Mode = Regular")
with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path(src_filename, thread_count=8, output_folder=path, first_page=0)

# flush all the required images
page13_image = images_from_path[12]
page13_image.save('13.jpg', 'JPEG')

page14_image = images_from_path[13]
page14_image.save('14.jpg', 'JPEG')

page16_image = images_from_path[15]
page16_image.save('16.jpg', 'JPEG')

print("Image(s) Saved")

# Read The PDF in HD mode, and extract the required Image
print("\nScanning PDF | Mode = 500 DPI")
with tempfile.TemporaryDirectory() as path:
    hd_images_from_path = convert_from_path(src_filename, dpi=500, thread_count=8, output_folder=path, first_page=0)

# flush all the required images
page13_image = hd_images_from_path[12]
page13_image.save('hd_13.jpg', 'JPEG')

page14_image = hd_images_from_path[13]
page14_image.save('hd_14.jpg', 'JPEG')

page16_image = hd_images_from_path[15]
page16_image.save('hd_16.jpg', 'JPEG')
print("HD Image(s) Saved")

print("\nPassing Image(s) to Google Vision API for Scan Request.")

# Make call to vision API and get the text meta for regular images
texts_13 = get_text_from_image("13.jpg")
texts_14 = get_text_from_image("14.jpg")
texts_16 = get_text_from_image("16.jpg")

# Make call to vision API and get the text meta for HD images
hd_texts_13 = get_text_from_image("hd_13.jpg")
hd_texts_14 = get_text_from_image("hd_14.jpg")
hd_texts_16 = get_text_from_image("hd_16.jpg")

print("\nPage No. 13")
print("\nShare Capital ")
print(texts_13[21].description, texts_13[24].description, get_non_truncated_val(texts_13[122].description, texts_13))

print("\nTrade Receivables ")
print(texts_13[21].description, texts_13[24].description, get_non_truncated_val(texts_13[51].description, texts_13))

print("\nPage No. 14")
print("\nRevenue ")
print(texts_14[26].description, texts_14[30].description, get_non_truncated_val(texts_14[32].description, texts_14))

print("\nProfit After tax ")
print(texts_14[26].description, texts_14[30].description, get_non_truncated_val(texts_14[77].description, texts_14))

print("\nPage No. 16")
print("\nNet Cash generated from Operations ")
print(texts_16[24].description, texts_16[26].description, get_non_truncated_val(texts_16[99].description, hd_texts_16))

print("\nNet Cash generated from finance activities")
print(texts_16[24].description, texts_16[26].description, get_non_truncated_val(texts_16[157].description, hd_texts_16))
