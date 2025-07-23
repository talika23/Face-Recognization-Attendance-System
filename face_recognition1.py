from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
from time import strftime
from datetime import datetime
import os
import numpy as np
import cv2
 

class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        self.title_lbl = Label(self.root, text="FACE RECOGNITION", 
                               font=("times new roman", 35, "bold"), 
                               bg="white", fg="darkgreen")
        self.title_lbl.place(x=0, y=0, width=1530, height=45)
       
        # 1st image
        img_top = Image.open("My images/face detector.png")
        img_top = img_top.resize((650, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        self.f_lbl1 = Label(self.root, image=self.photoimg_top)
        self.f_lbl1.place(x=0, y=55, width=650, height=700)

        # 2nd image
        img_bottom = Image.open("My images/accuracy1.png")
        img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        self.f_lbl2 = Label(self.root, image=self.photoimg_bottom)
        self.f_lbl2.place(x=650, y=55, width=950, height=700)
        
        # Button for Face Recognition
        self.b1_1 = Button(self.f_lbl2, text="Face Recognition", cursor="hand2",
                           font=("times new roman", 18, "bold"), bg="blue", fg="white",
                           command=self.face_recog)
        self.b1_1.place(x=365, y=620, width=200, height=40)

    def mark_attendance(self, i, r, n, d): 
        with open("talika.csv", "r+", newline="\n") as f:
            myDataList = f.readlines()
            name_list = []
            for line in myDataList:
                entry = line.split(",")
                name_list.append(entry[0])
            if (i not in name_list) and (r not in name_list) and (n not in name_list) and (d not in name_list):
                now = datetime.now()
                d1 = now.strftime("%d/%m/%Y")
                dtString = now.strftime("%H:%M:%S")
                f.writelines(f"\n{i},{r},{n},{d},{dtString},{d1},Preset")

    def recognize(self, img, clf, faceCascade):
         return self.draw_boundary(img, faceCascade, 1.1, 10, clf)

    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        for (x, y, w, h) in features:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))
            print(f"Predicted ID: {id}, Confidence: {confidence}")


            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="B@b@2208", database="face_recognizer")
                my_cursor = conn.cursor()

                my_cursor.execute("SELECT Name FROM student WHERE Student_id=%s", (id,))
                n = my_cursor.fetchone()
                n = n[0] if n else "Unknown"

                my_cursor.execute("SELECT Roll FROM student WHERE Student_id=%s", (id,))
                r = my_cursor.fetchone()
                r = r[0] if r else "Unknown"

                my_cursor.execute("SELECT Dep FROM student WHERE Student_id=%s", (id,))
                d = my_cursor.fetchone()
                d = d[0] if d else "Unknown"

                my_cursor.execute("SELECT Student_id FROM student WHERE Student_id=%s", (id,))
                i = my_cursor.fetchone()
                i = "+".join(i) if i else "Unknown"

                


                if confidence > 50:
                   
                    cv2.putText(img, f"ID: {i}", (x, y - 75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Roll: {r}", (x, y - 55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {n}", (x, y - 30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Department: {d}", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    self.mark_attendance(i, r, n, d)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 3)
                    cv2.putText(img, "Unknown Face", (x, y - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)

                conn.close()
            except mysql.connector.Error as err:
                print(f"Error accessing database: {err}")
            except Exception as e:
                print(f"An error occurred: {e}") #catch any other errors
        return img

    def face_recog(self):
        faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
        try:
            clf = cv2.face.LBPHFaceRecognizer_create()
            clf.read("classifier.xml")
            print("Classifier loaded successfully!")
        except Exception as e:
            print(f"Error loading classifier: {e}")
            return

        video_cap = cv2.VideoCapture(0)

        while True:
            ret, img = video_cap.read()
            if not ret:
                break
            img = self.recognize(img, clf, faceCascade)
            cv2.imshow("Welcome To Face Recognition", img)

            if cv2.waitKey(1) == 13:
                break

        video_cap.release()
        cv2.destroyAllWindows()

# Main Execution
if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition(root)
    root.mainloop()

