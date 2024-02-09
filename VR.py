import cv2
import numpy as np

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to 960x540 to maintain a 16:9 aspect ratio
    resized_frame = cv2.resize(frame, (960, 540))

    # Concatenate the two resized frames to create the VR effect
    vr_frame = np.concatenate((resized_frame, resized_frame), axis=1)

    # Since the concatenated frame is 1920x540, we need to add black borders
    # on the top and bottom to fill the 1920x1080 screen
    top_border_width = (1080 - 540) // 2
    bottom_border_width = 1080 - 540 - top_border_width
    vr_frame_with_borders = cv2.copyMakeBorder(
        vr_frame,
        top_border_width,
        bottom_border_width,
        0,
        0,
        cv2.BORDER_CONSTANT,
        value=[0, 0, 0],
    )

    # Display the VR frame with borders
    cv2.imshow("VR Webcam", vr_frame_with_borders)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# Release the VideoCapture and close windows
cap.release()
cv2.destroyAllWindows()
