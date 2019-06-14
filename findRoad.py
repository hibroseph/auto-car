import numpy as np
import cv2
import matplotlib
matplotlib.rcParams["backend"] = "TkAgg"
from matplotlib import pyplot as plt

# Load the webcam
cap = cv2.VideoCapture(0)

# For use in the linear transformation to birdseye view
rec = np.array([[250, 28], [399, 28], [459, 479], [181, 479]], dtype="float32")
dst = np.array([[0, 0], [278, 0], [278, 600], [0, 600]], dtype="float32")


while (True):

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
    warped = cv2.warpPerspective(mask_img, M, (278,600))    

    # Save the image to a file for viewing
    # np.savetxt("image.txt", warped, fmt='%g')
    
    ## To find the middle pixel where the road is 
    b = np.sum(warped[590:,], axis=0)

    # This will loop through the 10 difference sections where we are searching with our windows
    # our windows have the height of 60px

    array = [600, 540, 480, 420, 360, 300, 240, 180, 120, 60]
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

        #Add a rectangle onto the image of where the path was found
        cv2.rectangle(warped, (iFirst, array[i] - 60), (iLast,array[i]),(120,120,120),2)


    # Display the new image with the rectangles added to it
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
