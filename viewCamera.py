import cv2
import numpy as np

IMAGE_H = 479
IMAGE_W = 639
NUM_OF_BOXES = 10
SPACE_BETWEEN = IMAGE_H / NUM_OF_BOXES

cap = cv2.VideoCapture(0)

# For use in the linear transformation to birdseye view
"""
rec = np.array([[250, 28], [399, 28], [459, 479], [181, 479]], dtype="float32")
dst = np.array([[0, 0], [278, 0], [278, 600], [0, 600]], dtype="float32")
"""
rec = np.array([[0,IMAGE_H],[IMAGE_W,IMAGE_H],[0,0],[IMAGE_W,0]], dtype="float32")
dst = np.array([[200,IMAGE_H], [400,IMAGE_H], [0, 0], [IMAGE_W,0]], dtype="float32")

array = np.linspace(IMAGE_H,0, 10)
x = []

while(True):
     # Read the image from the webcam
    ret, frame = cap.read()

    # Convert image from RGB to HSV
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # let's take apart the HSV and look at them
    h, s, v = image[:,:,0], image[:,:,1], image[:,:,2]

    cv2.imshow("h", h)
    cv2.imshow("s", s)
    cv2.imshow("v", v)
    
    # Create binary image with S of the HSV image with a thersold of 150
    retval,mask_img = cv2.threshold(v, 230, 250,cv2.THRESH_BINARY)

    # Get the birdseye view
    M = cv2.getPerspectiveTransform(rec, dst)
    Minv = cv2.getPerspectiveTransform(dst,rec)
    warped = cv2.warpPerspective(mask_img, M, (IMAGE_W,IMAGE_H))    

    for i in range(array.size):
        # Find where the white line is
        holder = np.sum(warped[int(array[i] - SPACE_BETWEEN): int(array[i])], axis=0)
        #print("Hello World")
        iFirst = np.argmax(holder>250)

        revHolder = holder[::-1]

        iLast = len(revHolder) - np.argmax(revHolder>250) - 1

        if iFirst == 0 and iLast > IMAGE_W - 25:
            continue

        x.append((iLast-iFirst)/ 2 + iFirst)

        cv2.rectangle(warped, (iFirst, int(array[i] - SPACE_BETWEEN)), (iLast, int(array[i])),(120,120,120),2)
         
    cv2.imshow("Video", frame)
    cv2.imshow("binary image", warped)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
