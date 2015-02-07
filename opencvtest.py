import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# Die in a fire autoexposure
cap.set(15, 1)

lastx = -1
lasty = -1

while True:
    # Capture frame-by-frame
    _, frame = cap.read()

    # Our operations on the frame come here
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # yellow color range
    lower_yellow = np.array([20, 120, 120])
    upper_yellow = np.array([30, 255, 255])
    # Threshold the HSV image to get only yellow colors
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Remove small objects & holes from foreground
    tracker = cv2.erode(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                                        (10, 10)))
    tracker = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE,
                                                         (5, 5)))

    # Go back to color mode so we can see the line in color
    output = cv2.cvtColor(tracker, cv2.COLOR_GRAY2BGR)

    contours, hierarchy = cv2.findContours(tracker.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_NONE)
    for i, contour in enumerate(contours):
        carea = cv2.contourArea(contour)
        if carea < 1000:
            cv2.drawContours(tracker, contours, i, (0, 0, 0), -1)
        else:
            cv2.drawContours(output, contours, i, (0, 255, 0), 3)

    # Now we will draw a black frame around the edges because the black contours above
    # don't go all the way to the edge of the image
    height, width = tracker.shape
    cv2.rectangle(tracker, (0, 0), (width, height), (0, 0, 0), 2)

    cv2.imshow('tracker', tracker)
    # Calculate moments
    moments = cv2.moments(tracker)
    dm01 = moments['m01']
    dm10 = moments['m10']
    darea = moments['m00']

    if darea > 20000:
        allpoints = cv2.findNonZero(tracker)
        bounding_rect = cv2.minAreaRect(allpoints)
        box = cv2.cv.BoxPoints(bounding_rect)
        box = np.int0(box)
        cv2.drawContours(output, [box], 0, (0, 0, 255), 2)

        posx = int(dm10 / darea)
        posy = int(dm01 / darea)
        cv2.circle(output, (posx, posy), 5, (25, 200, 50), 10)

    # Display the resulting frame
    cv2.imshow('hsv', hsv)
    cv2.imshow('output', output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()