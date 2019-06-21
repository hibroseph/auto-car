import numpy as np
import cv2
import matplotlib
import time
from adafruit_servokit import ServoKit
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt

# Load the webcam
cap = cv2.VideoCapture(0)

# For use in the linear transformation to birdseye view
rec = np.array([[250, 28], [399, 28], [459, 479], [181, 479]], dtype="float32")
dst = np.array([[0, 0], [278, 0], [278, 600], [0, 600]], dtype="float32")

kit = ServoKit(channels=16)
kit.servo[1].angle = 90
kit.continuous_servo[0].throttle = float(0)

print("Prepared Servo.")

while (True):

    # Read the image from the webcam
    ret, frame = cap.read()

    # Convert image from RGB to HSV
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # let's take apart the HSV and look at them
    h, s, v = image[:,:,0], image[:,:,1], image[:,:,2]

    # Create binary image with S of the HSV image with a thersold of 150
    retval,mask_img = cv2.threshold(v,230 , 250,cv2.THRESH_BINARY)

    # Get the birdseye view
    M = cv2.getPerspectiveTransform(rec, dst)
    warped = cv2.warpPerspective(mask_img, M, (278,600))    

    # Save the image to a file for viewing
    # np.savetxt("image.txt", warped, fmt='%g')
    
    ## To find the middle pixel where the road is 
    b = np.sum(warped[590:,], axis=0)

    # This will loop through the 10 difference sections where we are searching with our windows
    # our windows have the height of 60px
    array = [600, 540, 480, 420, 360, 300, 240, 180, 120, 60]

    x = []


    # Loop 10 times to find the 10 difference box locations starting from the bottom, going to the top
    for i in range(10):

        # Add together all the columns and 60 rows to find where the white line is
        holder = np.sum(warped[array[i]-60:array[i]], axis=0)

        # Find the first index (meaning the left hand index)
        # Index in the follow comments talks about the x position of pixels
        iFirst = np.argmax(holder>250)
        
        # Reverse the list to find the right index
        revHolder = holder[::-1]

        # Find the last index (or the right index)
        iLast = len(revHolder) - np.argmax(revHolder>250) - 1
        
        # If the indexes are the edges of the images, don't display a rectangle
        if iFirst == 0 and iLast == 277:
            continue

        #Print statements for debugging
        #print(str(array[i]) + " iFirst: " + str(iFirst))
        #print(str(array[i]) + " iLast: " + str(iLast))

        x.append((iLast - iFirst) / 2 + iFirst)

        #Add a rectangle onto the image of where the path was found
        cv2.rectangle(warped, (iFirst, array[i] - 60), (iLast,array[i]),(120,120,120),3)

    # print(len(new_array[:len(x)]))
    #print(len(x[::-1]),len(new_array[0:len(x[::-1])]))
    # Create a polynomial that will fit the curve

    
    z = np.polyfit(x[::], array[len(array) - len(x):], 2 )
    
    p = np.poly1d(z)

    #plt.show()

    # print("polynomial: " + str(z))
    # cv2.putText(warped, "Polynomial: " + string(z)
    # Display the new image with the rectangles added to it
    # print("pt1: " + str(x[0]) + " " + str(int(p(x[0]))))
    # print("pt2: " + str(x[1]) + " " + str(int(p(x[1]))))

    #for i in range(len(x)):
    #    cv2.circle(warped, (int(x[i]), 600 - int(p(x[i]))), 5, (120,120,120), 2)

    # Using openCV polyfil
    plotx = np.linspace(0, 277, 1000)
    fity = z[0]*plotx**2  + z[1]*plotx + z[2]

    pts = np.vstack((plotx,fity)).astype(np.int32).T
    
    cv2.polylines(warped, [pts], False, (120, 120,120), 2)
    
    # print("y pt " + str(int(p(160))))
    # cv2.circle(warped, (154, 600 - int(p(154))), 5, (120,120,120),2)

    try:
        point = []
        point2 = []
        midpoint = []

        xSelector = 2
        x2Selector = 3

        point.append(int(x[xSelector])) 
        point.append(600 - int(p(x[xSelector])))

        point2.append(int(x[x2Selector]))
        point2.append(600 - int(p(x[x2Selector])))

        midpoint.append(point[0] - point2[0])
        midpoint.append(point[1] - point2[1])
    except:
        kit.servo[1].angle = float(90)
        kit.continuous_servo[0].throttle = float(0)
        
    degrees = 90
    
    if midpoint[1] & midpoint[0] != 0:
        if np.arccos(midpoint[0]/midpoint[1]) > 1:
            degrees = 180 - np.degrees(np.arccos(midpoint[0]/midpoint[1]))
            print(degrees)
    if degrees >= 108:
        degrees = 107
    elif degrees <= 72:
        degrees = 73

    kit.servo[1].angle = float(degrees)

    #time.sleep(0.2)
    
    kit.continuous_servo[0].throttle = float(.15)
    
    cv2.imshow("Warped Image with Box", warped)

    # Wait for a q to close the program and image
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Standard cv stuff
cap.release()
cv2.destroyAllWindows()

############################################################################################
# The following are scripts to help me remember some syntax stuff                          #
############################################################################################

# Load image to numpy
# a = np.loadtxt(image.txt)
### Sum the last 10 rows of all the cols together
# b = np.sum(a[590:,], axis=0)
### Find the first index of a number greater than a threshold
# iFirst = np.argmax(c>1000)
### Find the last index of a number greater than a threshold
# rc = c[::-1]
