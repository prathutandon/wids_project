import cv2
import face_recognition
import os
import csv
import time
from datetime import datetime
from win32com.client import Dispatch
    # Function to make the computer speak
def speak(str1):
    speak = Dispatch(("SAPI.SpVoice"))
    speak.Speak(str1)
    
def create_image_dictionary(folder_path):
    image_dict = {}

    # Ensure the provided path is a directory
    if os.path.isdir(folder_path):
        # Iterate through each file in the directory
        for file_name in os.listdir(folder_path):
            # Check if the file is a JPEG image
            if file_name.lower().endswith(".jpg"):
                # Get the image name without the file extension
                image_name = os.path.splitext(file_name)[0]

                # Construct the full path to the image
                image_path = os.path.join(folder_path, file_name)

                # Add the image name and path to the dictionary
                image_dict[image_name] = face_recognition.face_encodings(face_recognition.load_image_file(image_path))[0]
   
    return image_dict

if __name__ == "__main__":
    folder_path = r"C:\Users\91797\Desktop\Source Code\Pictures"  # Replace with the path to your folder
    image_dictionary = create_image_dictionary(folder_path)
    
# Function to recognize faces from the webcam
def recognize_faces_webcam():
    # Load face encodings for known faces (you need to prepare this in advance)
    # Replace "known_faces" with a dictionary where keys are names and values are face encodings
    known_faces = image_dictionary

    print(known_faces)
    # Open the webcam
    video_capture = cv2.VideoCapture(0)
    
    # Column names for the attendance CSV file
    COL_NAMES = ['NAME', 'TIME']

    while True:
        # Capture each frame from the webcam
        ret, frame = video_capture.read()

        # Find all face locations and face encodings in the frame
        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        # Loop through each face found in the frame
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            # Check if the face matches any known faces
            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)

            name = "Unknown"  # Default to "Unknown" if no match is found

            # If a match is found, use the name of the known face
            if True in matches:
                first_match_index = matches.index(True)
                name = list(known_faces.keys())[first_match_index]

            # Draw a rectangle around the face and display the name
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
            
            #Put Text on Image
            if name != "Unknown" and len(face_locations)==1:
                cv2.putText(frame, 'Press T to Record Attendance', (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)
        
            # Get the current timestamp
            ts = time.time()
            date = datetime.fromtimestamp(ts).strftime("%d-%m-%Y")
            timestamp = datetime.fromtimestamp(ts).strftime("%H:%M-%S")
            
            # Check if the attendance CSV file for the current date exists
            exist = os.path.isfile("Attendance/Attendance_" + date + ".csv")
            
            # Prepare attendance data
            attendance = [str(name), str(timestamp)]
            
            # Some Conditions
            if  name == "Unknown" and len(face_locations)>=2:
                cv2.putText(frame, 'Please Register Yourself', (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3) 
                
            if name == "Unknown" and len(face_locations)<2:
                cv2.putText(frame, 'Please Register Yourself', (5,25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3) 
                cv2.putText(frame, 'Unable to Recognise Face', (5,60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3) 
               
            if  len(face_locations)>=2 and name != "Unknown" :
                cv2.putText(frame, 'There are Multiple Faces in Single Frame', (5,50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 3) 
                
            
            
        # Display the resulting frame
        cv2.imshow('Video', frame)
        k = cv2.waitKey(1)
        
        # Break the loop if 'q' is pressed
        if k==ord('t') and name!= "Unknown" and len(face_locations)==1:
            speak("Attendance Taken..")
            time.sleep(5)
            if exist:
                with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(attendance)
                csvfile.close()
            else:
                with open("Attendance/Attendance_" + date + ".csv", "+a") as csvfile:
                    writer=csv.writer(csvfile)
                    writer.writerow(COL_NAMES)
                    writer.writerow(attendance)
            csvfile.close()
            
        if k==ord('t') and (name == "Unknown" or len(face_locations)>=2):
            speak("Unable to take Attendance ..")
            time.sleep(5)
            
        if k==ord('q'):
            break

    # Release the webcam and close all windows
    video_capture.release()
    cv2.destroyAllWindows()

# Call the function to start facial recognition from the webcam
recognize_faces_webcam()
    