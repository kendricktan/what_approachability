import os, sys, cv2, glob, urllib2, httplib, urllib, base64, json
import numpy as np
from urlparse import urlparse

# Our paths
current_path = os.path.dirname(os.path.abspath(__file__))
cascade_file_path = current_path + '/database/haarcascade_frontalface_alt.xml'
eigenmodel_xml_file_path = current_path + '/database/eigenmodel.xml'
average_image_file_path = current_path + '/database/faces/*.jpg'

# Threshold to define how 'fuzzy' the comparison to eigenfaces should be
THRESHOLD = 9000.0

# Get face ROI
def get_faces_rect(image):
    cascade = cv2.CascadeClassifier(cascade_file_path)
    rects = cascade.detectMultiScale(image, 1.3, 5, cv2.cv.CV_HAAR_SCALE_IMAGE, (20, 20))
    if len(rects) == 0:
        return None
    return rects

# Downloads image via url
def downloadImage(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36')]
    handle = opener.open(url)
    if (handle.getcode() == 200):
        image = np.asarray(bytearray(handle.read()), dtype=np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_GRAYSCALE)
        return image
    return None

# Creates our eigenmodel
def create_eigenmodel():
    x, y = [], []
    SIZES = (256, 256)

    image_list = glob.glob(average_image_file_path)
    image_list.sort()

    # Read images
    i = 0
    for image_path in image_list:
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        rects = get_faces_rect(image)
        for (x1, y1, w, h) in rects:
            cropped = np.copy(image[y1:y1+h, x1:x1+w])
            cropped = cv2.resize(cropped, SIZES)
            x.append(np.asarray(cropped, dtype=np.uint8))
            y.append(i)
            i = i + 1

    # Convert labels to np array
    y = np.asarray(y, dtype=np.int32)

    # Eigenfaces model
    model = cv2.createEigenFaceRecognizer()

    # Train our model
    model.train(np.asarray(x), np.asarray(y))

    model.save(eigenmodel_xml_file_path)

# Compares our eigenmodel
def compare_eigenmodel(url='http://i.imgur.com/q6IYKCO.jpg'):
    model = cv2.createEigenFaceRecognizer(threshold=THRESHOLD)
    model.load(eigenmodel_xml_file_path)

    image = downloadImage(url)

    rects = get_faces_rect(image)

    for (x1, y1, w, h) in rects:
        cropped = np.copy(image[y1:y1+h, x1:x1+w])
        cropped = cv2.resize(cropped, (256, 256))
        [label, confidence] = model.predict(cropped)

        # Lower the confidence, more attractive it is
        print('Predicted label = %d, confidence = %.2f' % (label, confidence))

# Connects to microsoft's API to get emotion data
def microsoft_api_get_emotion(url='http://www.scientificamerican.com/sciam/cache/file/35391452-5457-431A-A75B859471FAB0B3.jpg'):
    # Image to analyse (body of the request)
    body = '{\'URL\': \''+ url + '\'}'

    # API request for Emotion Detection
    headers = {
       'Content-type': 'application/json',
    }

    params = urllib.urlencode({
       'subscription-key': 'bf13dfec6c98434e886a8818b949afd6',  # Enter EMOTION API key
       #'faceRectangles': '',
    })

    try:
       conn = httplib.HTTPSConnection('api.projectoxford.ai')
       conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body , headers)
       response = conn.getresponse()
       print("Send request")

       parsed_data = json.loads(response.read())[0]
       print(parsed_data)
       emotion_dict = parsed_data['scores']
       for emotion in emotion_dict:
           print(emotion, emotion_dict[emotion])

    except Exception as e:
       print("[Errno {0}] {1}".format(e.errno, e.strerror))

microsoft_api_emotion()
