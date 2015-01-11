import cv2

cap = cv2.VideoCapture(1)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    if frame is None:
        print 0
    else:
        print 1
    # Display the resulting frame
    #cv2.imshow('frame', frame)
    #if cv2.waitKey(1) & 0xFF == ord('q'):
    #    break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
