import os
import cv2
from datetime import datetime
from datetime import timedelta

date = datetime(2010, 6, 10)
endDate = datetime(2021, 10, 23)

date += timedelta(days=1)

image_folder = 'images'
video_name = 'ohia_spread.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
numImages = len(images)

frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

fps = 20
video = cv2.VideoWriter(video_name, 0, fps, (width,height))

timeIncrement = (endDate - date) /numImages
for i in range(numImages):
    imageFileName = str(i) + ".png"
    path = os.path.join(image_folder, imageFileName)
    image = cv2.imread(path)
    window_name = 'Image'
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (50, 150)
    fontScale = 4
    color = (255, 255, 255)
    thickness = 2
    text = date.strftime("Year: %Y")
    image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    org = (50, 400)
    text = date.strftime("Month: %m")
    image = cv2.putText(image, text, org, font, fontScale, color, thickness, cv2.LINE_AA)
    video.write(image)
    date += timeIncrement

cv2.destroyAllWindows()
video.release()
