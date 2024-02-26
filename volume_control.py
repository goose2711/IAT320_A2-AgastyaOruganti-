#IAT320 - Body Interface (Spring 2024)
#Professor: Philippe Pasquier
#Teaching Assistant: Henry Lin 
#By: Agastya Oruganti (301386531)


# Importing the necessary libraries after pip installing them
import cv2 # OpenCV for object detection and motion capture
import numpy as np # Numpy for mathamatical operations and arrays
import os # To create and operate with directories

# Start the hand tracking by using video capture function in the cv2 module and store in a variable as an object
cap = cv2.VideoCapture(0)

# Set up volume control parameters and store inside variables
max_volume = 100
min_volume = 0
volume_interval = 10  # Calibrating the horizontal movement with the intensity of change 
current_volume = 50  # Setting base volume as 50 %

# Define the command to change the volume (Mac-specific) (Citation: https://dev.to/0xkoji/control-mac-sound-volume-by-python-h4g)
volume_command = "osascript -e 'set volume output volume {}'"

# Start while loop
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally for a mirrored view
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # Convert the frame to grayscale
    gray = cv2.GaussianBlur(gray, (5, 5), 0)  # Apply a blur to the frame to improve hand tracking
    _, threshold = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY) # Use thresholding to create a binary image
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Find contours in the binary image

    #Here i used a for loop to iterate through all the found contours stored in the contours object earlier.
    #The idea is that, when a contour is distinguished, find the greatest contour area and create a bounding box for that contour and use that to manipulate math operations. 
    # (Citation: https://stackoverflow.com/questions/57296398/how-can-i-get-better-results-of-bounding-box-using-find-contours-of-opencv)
    for contour in contours:

        # Filter contours based on area 
        if cv2.contourArea(contour) > 1000:
            x, y, w, h = cv2.boundingRect(contour) # create the bounding box for the contour
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # Map the hand position/bounding box to the volume range
            volume = np.interp(x + w // 2, [0, frame.shape[1]], [min_volume, max_volume])
            # Smoothen the volume changes
            current_volume = np.interp(volume, [current_volume - volume_interval, current_volume + volume_interval],
                                       [current_volume - 1, current_volume + 1])

            # Execute the volume command for the system using the os library . 
            os.system(volume_command.format(int(current_volume)))

    cv2.imshow("Volume Control", frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#Once the loop breaks, release the cv2 capture object and kill all existing windows of the program 
cap.release()
cv2.destroyAllWindows()

###############################################################################
# Citations for all the resources used 
# https://stackoverflow.com/questions/57296398/how-can-i-get-better-results-of-bounding-box-using-find-contours-of-opencv
# https://dev.to/0xkoji/control-mac-sound-volume-by-python-h4g
# https://docs.opencv.org/4.x/d0/db2/tutorial_macos_install.html
# https://numpy.org/install/
# https://docs.python.org/3/library/os.html
# https://github.com/mdylan2/gesture_jester
# https://macpaw.com/how-to/install-pip-mac
# https://stackoverflow.com/questions/1687357/updating-python-on-mac
