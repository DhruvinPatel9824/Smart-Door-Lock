import face_recognition
import cv2
import numpy as np
import datetime
import twilio
from credentials import account, token, my_cell, my_twilio
from twilio.rest import Client



video_capture = cv2.VideoCapture(0)
# we load file image and encode the image for recognition the face
Dhruvin = face_recognition.load_image_file('dhruvin.jpeg')
Dhruvin_encoding = face_recognition.face_encodings(Dhruvin)[0]

Bhavya = face_recognition.load_image_file('bhavya.jpeg')
Bhavya_encoding = face_recognition.face_encodings(Bhavya)[0]

hem = face_recognition.load_image_file('hem.jpeg')
hem_encoding = face_recognition.face_encodings(hem)[0]

known_face_encodings = [
    Dhruvin_encoding ,
    Bhavya_encoding,
    hem_encoding,

]
known_face_names = [
    "Dhruvin",
    "Bhavya",
    "Hem",
]
person=[]
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
i=0

while video_capture.isOpened():
    ret, frame = video_capture.read()

    face_names = []

    # Convert image  BGR to RGB because opencv use BGR formate when  the face_recognition use Rgb formate
    rgb_small_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Only process every other frame of video
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        for face_encoding in face_encodings:

            # Match the face of video capture with encoded(known) face if does not mathe then set unknown
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
                face_names.append(name)


    process_this_frame = not process_this_frame

    # Put rectangle on the face
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting frames
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

def send_sms(msg,time):

    client = Client(account, token)
    msg=msg+"come at"+str(now)

    message = client.messages.create(to=my_cell, from_=my_twilio,
                                     body=msg)
    print(message)

# information of guist list
guist_list = [["zometoboy", "zom001", "20:20:00:00", "23:00:00:00"],
                  ["flipcart", "flip002", "8:00:00:00", "9:30:00:00"],
                  ["londary", "lon003", "7:00:00:00", "8:00:00:00"],
                  ["milkman", "milk004", "7:00:00:00", "7:30:00:00"]]
# function for adding new guist in list
def add_guist(guist_list):
    l=[]
    print("Enter the job of man")
    l.append(input())
    print("Enter the code of person")
    l.append(input())
    print("Enter Time range1")
    l.append((input()))
    print("Enter Time range2")
    l.append((input()))
    guist_list.append(l)
# if unknown face is dectated then it match with guist list if it match then send sms
def unknown_detection():
    print("Enter the Entry Code")
    search = input()
    now = datetime.datetime.now()
    index = -1
    for i in range(len(guist_list)):
        if guist_list[i][1] == search:
            a, b, c, d = map(int, guist_list[i][2].split(":"))
            st = now.replace(hour=a, minute=b, second=c, microsecond=d)
            a, b, c, d = map(int, guist_list[i][3].split(":"))
            ed = now.replace(hour=a, minute=b, second=c, microsecond=d)
            if (st <= now <= ed):
                index = i
    if index > -1:
        send_sms(guist_list[index][0],now)
    else:
        send_sms("Unknown Person",now)



now = datetime.datetime.now()
if face_names[0]=="Unknown":
    unknown_detection()
elif len(face_names)>0:
    send_sms(face_names[0],now)







