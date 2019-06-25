import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# For use in the linear transformation to birdseye view
rec = np.array([[250, 28], [399, 28], [459, 479], [181, 479]], dtype="float32")
dst = np.array([[0, 0], [278, 0], [278, 600], [0, 600]], dtype="float32")

while(True):
     # Read the image from the webcam
    ret, frame = cap.read()

    # Convert image from RGB to HSV
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # let's take apart the HSV and look at them
    h, s, v = image[:,:,0], image[:,:,1], image[:,:,2]

    # Create binary image with S of the HSV image with a thersold of 150
    retval,mask_img = cv2.threshold(s, 70, 250,cv2.THRESH_BINARY)

    # Get the birdseye view
    M = cv2.getPerspectiveTransform(rec, dst)
    warped = cv2.warpPerspective(frame, M, (278,600))    

    cv2.imshow("Video", frame)
    cv2.imshow("binary image", warped)


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
