from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import os
from developer1 import StylishDeveloperUI
from tkinter import messagebox
from time import strftime
from datetime import datetime




# Detect blink or movement logic here (like ratio of eye aspect)

from student2 import Student
from train1 import Train
from face_recognition1 import Face_Recognition
from attendance import Attendance
from help import Help
from developer1 import StylishDeveloperUI



class Face_Recognization_System:

    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")
        
        


        # First Image
        img = Image.open(r"C:\Users\HP\Desktop\My images\face5.PNG").resize((500, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        Label(self.root, image=self.photoimg).place(x=0, y=0, width=500, height=130)

        # Second Image
        img1 = Image.open(r"C:\Users\HP\Desktop\My images\face6.PNG").resize((500, 130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg1).place(x=500, y=0, width=500, height=130)

        # Third Image
        img2 = Image.open(r"C:\Users\HP\Desktop\My images\face1.PNG").resize((550, 130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        Label(self.root, image=self.photoimg2).place(x=1000, y=0, width=550, height=130)

        # Background image
        img3 = Image.open(r"C:\Users\HP\Desktop\My images\background.PNG").resize((1530, 710), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)
        self.bg_image = Label(self.root, image=self.photoimg3)
        self.bg_image.place(x=0, y=130, width=1530, height=710)
        
        self.title_lbl = Label(self.bg_image, text="FACE RECOGNIZATION ATTENDANCE SYSTEM SOFTWARE",
                               font=("times new roman", 35, "bold"), bg="white", fg="red")
        self.title_lbl.place(x=0, y=0, width=1530, height=45)

  
       
        # Function Buttons
        self.create_button("student.jpg", "Student Details", 200, 100,self.student_details)
        self.create_button("face detector.PNG", "Face Detector", 500, 100,command=self.face_data)
        self.create_button("Attendance.PNG", "Attendance", 800, 100,self.attendance_data)
        self.create_button("help desk.PNG", "Help Desk", 1100, 100,self.help_data)
        self.create_button("train data.PNG", "Train Data", 200, 380,self.train_data)
        self.create_button("photos.PNG", "Photos", 500, 380,self.open_img)
        self.create_button("developer.PNG", "Developer", 800, 380,self.developer_data)
        self.create_button("Exit.PNG", "Exit", 1100, 380, self.iExit)

    def create_button(self, img_path, text, x, y, command=None):
        img = Image.open(fr"C:\Users\HP\Desktop\My images\{img_path}").resize((220, 220), Image.LANCZOS)

        
        photo = ImageTk.PhotoImage(img)
        btn = Button(self.bg_image, image=photo, cursor="hand2",command=command)
        btn.image = photo  # Keep reference
        btn.place(x=x, y=y, width=220, height=220)
        Button(self.bg_image, text=text, cursor="hand2",command=command,
               font=("times new roman", 15, "bold"), bg="darkblue", fg="white",
               ).place(x=x, y=y+200, width=220, height=40)
        
        
    
  #===============time==========
    def time(self):
        string = strftime('%H:%M:%S %p')
        self.lbl.config(text = string)
        self.lbl.after(1000, self.time)

        self.lbl = Label(self.title_lbl,font=('times new roman',14,'bold'),background= 'white',foreground='blue')
        self.lbl.place(x=0,y=0,width=110,height=50)
        self.time()



    def iExit(self):
        self.iExit=messagebox.askyesno("Face Recognition","Are you sure exit this project",parent=self.root)
        if self.iExit>0:
            self.root.destroy()
        else:
             return
    
    

    def open_img(self):
        os.startfile("data")



    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

    def train_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Train(self.new_window)
       
    def face_data(self):
        self.new_window = Toplevel(self.root)
        self.app = Face_Recognition(self.new_window)

    

   

    def attendance_data(self):
        self.new_window = Toplevel(self.root)
        self.app =Attendance(self.new_window)


    def developer_data(self):
        self.new_window = Toplevel(self.root)
        self.app =StylishDeveloperUI(self.new_window)


    def help_data(self):
        self.new_window = Toplevel(self.root)
        self.app =Help(self.new_window)





        







# Main Execution
if __name__ == "__main__":    
    root = Tk()
    obj = Face_Recognization_System(root)
    root.mainloop()
