import PIL
from PIL import Image
import cv2
from imageai.Detection import ObjectDetection
import time
import math

#1

# image = Image.open('variant-7.jpg')
# image = image.transpose(PIL.Image.FLIP_TOP_BOTTOM)
# image = image.transpose(Image.ROTATE_180)
# image.save('flip_rot_image.jpg')

#2,3
camera = cv2.VideoCapture(0)

detector = ObjectDetection()
detector.setModelTypeAsTinyYOLOv3()
detector.setModelPath('yolo-tiny.h5')
detector.loadModel()

finish = 0

while camera.isOpened():
    ret, frame = camera.read()
    start = time.time()
    if start - finish > 2:
        _, array_detection = detector.detectObjectsFromImage(input_image=frame, input_type='array', output_type='array')
        finish = time.time()
        print(array_detection)
    cv2.imshow('Test', frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
    x = 1366 / 2 - array_detection[0]
    y = 768 / 2 - array_detection[1]
    print(math.sqrt(x^2 + y^2))
cv2.destroyAllWindows()




