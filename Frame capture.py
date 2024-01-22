# This is for to take photo whenever we press spacebar.
import cv2
import os
from datetime import datetime

a=input(str("Enter the User Id: "))

def take_and_save_photo(Picture):
    # Open the video capture object for the webcam
    video_capture = cv2.VideoCapture(0)

    # Create the save folder if it doesn't exist
    if not os.path.exists(Picture):
        os.makedirs(Picture)

    while True:
        # Capture each frame from the webcam
        ret, frame = video_capture.read()

        # Display the frame
        cv2.imshow('Webcam', frame)
       
            
        # Wait for the user to press the spacebar to capture a photo
        key = cv2.waitKey(1)
        if key == 32:  # ASCII code for spacebar
            # Get the current timestamp for the photo filename
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            photo_filename = f"{a}.jpg"

            # Save the photo to the specified folder
           
            
            photo_path = os.path.join("E:\College\Projects\WiDS", photo_filename)
            cv2.imwrite(photo_path, frame)

            print(f"Photo saved: {photo_path}")

        # Break the loop if the user presses 'q'
        elif key == ord('q'):
            break

    # Release the video capture object and close the window
    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    save_folder = "Pictures"  # Replace with your desired folder name
    take_and_save_photo("E:\College\Projects\WiDS")