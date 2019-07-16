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

print("Reading PDF File, Please Wait...")

# Currently HardCoding the name of the PDF file.
src_filename = "example.pdf"
with tempfile.TemporaryDirectory() as path:
    images_from_path = convert_from_path(src_filename, thread_count=4, output_folder=path, first_page=0)

print("Read Complete.")

# Author : Amar Kumar
# The code will convert all PDF pages into JPEG Image and Save it in the Local Disk.
# count = 1
# for image in images_from_path:
#     print(image)
#     filename_j = str(count) + '.jpg'
#     print(filename_j)
#     image.save(filename_j, 'JPEG')
#     count = count + 1

page13_image = images_from_path[12]
page13_image.save('13.jpg', 'JPEG')
print('#13 Page Saved')

page14_image = images_from_path[13]
page14_image.save('14.jpg', 'JPEG')
print('#14 Page Saved')

page16_image = images_from_path[15]
page16_image.save('16.jpg', 'JPEG')
print('#16 Page Saved')


def get_text_from_image(image_filename):
    # initializing empty file paths list
    path = os.path.join(os.path.dirname(__file__), image_filename)
    print(path)

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # returning all image paths
    return texts


texts_13 = get_text_from_image("13.jpg")
texts_14 = get_text_from_image("14.jpg")
texts_16 = get_text_from_image("16.jpg")

print("\nInformation on Page No. 13")
print("\nShare Capital ")
print(texts_13[21].description)
print(texts_13[24].description)
print(texts_13[122].description)

print("\nTrade Receivables ")
print(texts_13[21].description)
print(texts_13[24].description)
print(texts_13[51].description)

print("\nInformation on Page No. 14")
print("\nRevenue ")
print(texts_14[26].description)
print(texts_14[30].description)
print(texts_14[32].description)

print("\nProfit After tax ")
print(texts_14[26].description)
print(texts_14[30].description)
print(texts_14[77].description)

print("\nInformation on Page No. 16")
print("\nNet Cash generated from Operations ")
print(texts_16[24].description)
print(texts_16[26].description)
print(texts_16[99].description)

print("\nNet Cash generated from finance activities")
print(texts_16[24].description)
print(texts_16[26].description)
print(texts_16[157].description)
