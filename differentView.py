import cv2
import numpy as np
import math
import sys
import os
import time

IMAGE_H = 479
IMAGE_W = 639
NUM_OF_BOXES = 15
SPACE_BETWEEN = IMAGE_H / NUM_OF_BOXES

def main():

    #try:
    cap = cv2.VideoCapture(0)
    
    # For use in the linear transformation to birdseye view
    """
    rec = np.array([[250, 28], [399, 28], [459, 479], [181, 479]], dtype="float32")
    dst = np.array([[0, 0], [278, 0], [278, 600], [0, 600]], dtype="float32")
    """
    rec = np.array([[0,IMAGE_H],[IMAGE_W,IMAGE_H],[0,0],[IMAGE_W,0]], dtype="float32")
    dst = np.array([[150,IMAGE_H], [450,IMAGE_H], [0, 0], [IMAGE_W,0]], dtype="float32")
    
    array = np.linspace(IMAGE_H,0, NUM_OF_BOXES)
    #x = []
    
    while(True):
        # Read the image from the webcam
        ret, frame = cap.read()
        
        #cv2.imshow("lol poop", frame)
        
        # time.sleep(5)
        
        # Convert image from RGB to HSV
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # let's take apart the HSV and look at them
        h, s, v = image[:,:,0], image[:,:,1], image[:,:,2]
        
        # Create binary image with S of the HSV image with a thersold of 150
        retval,mask_img = cv2.threshold(s, 70, 250,cv2.THRESH_BINARY)
        
        # Get the birdseye view
        M = cv2.getPerspectiveTransform(rec, dst)
        #Minv = cv2.getPerspectiveTransform(dst,rec)
        warped = cv2.warpPerspective(mask_img, M, (IMAGE_W,IMAGE_H))    
        origin_image = cv2.warpPerspective(frame, M, (IMAGE_W,IMAGE_H))
        
        
        x = []
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
            
            #cv2.rectangle(warped, (iFirst, int(array[i] - SPACE_BETWEEN)), (iLast, int(array[i])),(120,120,120),2)
            #cv2.circle(warped, (int(x[i]), int(array[i] - (SPACE_BETWEEN / 2))),2, (120,120,120))
            
        print("length of x: " + str(len(x)) + " y: " + str(len(array)-len(x)))
            
        z = np.polyfit(x, (array[:len(x):] - (SPACE_BETWEEN / 2)),2)
            
        plotx = np.linspace(0, IMAGE_W, 100)
        fity = z[0]*plotx**2 + z[1]*plotx + z[2]
        
        pts = np.vstack((plotx, fity)).astype(np.int32).T
            
        ### find turn angle ###
        # width = sqrt((x2 - x1)**2 + (y2 - y1)**2)
        width = math.sqrt((pts[9][0] - pts[5][0])**2 + (pts[9][1] - pts[5][1])**2)
            
        midpointx = pts[9][0] - pts[5][0]
        midpointy = pts[9][1] - pts[5][1]
        
        height = math.sqrt((midpointx - pts[7][0])**2 + (midpointy - pts[7][0])**2)
        degrees = (180 - ((height/2) + (width**2) / (8 * height)))
        if degrees < 76:
            degrees = 76
        elif degrees > 115:
            degrees = 115
            print(degrees)
                
                ### show polynomial and video feeds ###
        cv2.polylines(warped, [pts], False, (120, 120, 120), 2)
                        
        cv2.imshow("Video", frame)
        cv2.imshow("binary image", warped)
        cv2.imshow("Original Image warped", origin_image)
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
                
    cap.release()
    cv2.destroyAllWindows()
                
#except:
#print("poop error: " + str(sys.exc_info()[0]))
#raise
#       os.system("python3 differentView.py")


if __name__ == "__main__":
    main()
