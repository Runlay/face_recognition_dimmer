import numpy as np
import cv2
import time
import os, sys
import face_recognition
import screen_brightness_control as sbc


known = "C:\\Users\\maxfi\\Desktop\\Face Recognition\\known_faces\\You.jpg"


def check(unknown):
    picture_of_me = face_recognition.load_image_file(known)
    my_face_encoding = face_recognition.face_encodings(picture_of_me)[0]

    # stranger
    unknown_picture = face_recognition.load_image_file(
        "C:\\Users\\maxfi\\Desktop\\Face Recognition\\Pics\\" + unknown)
    try:
        unknown_face_encoding = face_recognition.face_encodings(unknown_picture)[0]
        results = face_recognition.compare_faces([my_face_encoding], unknown_face_encoding)
        if results[0] == True:
            print("It's Max")
            value = 100

            try:
                sbc.set_brightness(value)
            except sbc.ScreenBrightnessError as error:
                print(error)

            #sys.exit()
        else:
            print("Nope, not " + unknown)
            print("Setting Brightness")
            value = 0

            try:
                sbc.set_brightness(value)
            except sbc.ScreenBrightnessError as error:
                print(error)

    except IndexError as e:
        print("Nobody detected")
        print("Setting Brightness")
        value = 0

        try:
            sbc.set_brightness(value)
        except sbc.ScreenBrightnessError as error:
            print(error)
        pass

def camera():
    cap = cv2.VideoCapture(0)
    count = 0
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


        success, image = cap.read()
        success = True
        while True:
            cap.set(cv2.CAP_PROP_POS_MSEC, (count * 10000))  # added this line
            success, image = cap.read()
            print('A new Picture was taken!')
            cv2.imwrite("C:\\Users\\maxfi\\Desktop\\Face Recognition\\Pics\\" + "frame%d.jpg" % count, image)  # save frame as JPEG file
            datei = os.listdir("C:\\Users\\maxfi\\Desktop\\Face Recognition\\Pics\\")
            for file in datei:
                check(file)
            time.sleep(20)
            cv2.imshow('frame', gray)
            os.remove("C:\\Users\\maxfi\\Desktop\\Face Recognition\\Pics\\" + "frame%d.jpg" % count)
            count = count + 1

    cap.release()
    cv2.destroyAllWindows()
camera()
