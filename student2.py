from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2


class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        #========Variables==========
        self.var_dep = StringVar()
        self.var_course = StringVar()
        self.var_year = StringVar()
        self.var_semester = StringVar()
        self.var_std_id = StringVar()
        self.var_std_name = StringVar()
        self.var_div = StringVar()
        self.var_roll = StringVar()
        self.var_gender = StringVar()
        self.var_dob = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_address = StringVar()
        self.var_teacher = StringVar()
        self.var_radio1 = StringVar()  # Initialize radio button variable

        # First Image
        img = Image.open(r"C:\Users\HP\Desktop\My images\student2.PNG")
        img = img.resize((500, 130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        self.f_lbl1 = Label(self.root, image=self.photoimg)
        self.f_lbl1.place(x=0, y=0, width=500, height=130)

        # Second Image
        img1 = Image.open(r"C:\Users\HP\Desktop\My images\student3.PNG")
        img1 = img1.resize((500, 130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        self.f_lbl2 = Label(self.root, image=self.photoimg1)
        self.f_lbl2.place(x=500, y=0, width=500, height=130)

        # Third Image
        img2 = Image.open(r"C:\Users\HP\Desktop\My images\student4.PNG")
        img2 = img2.resize((550, 130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        self.f_lbl3 = Label(self.root, image=self.photoimg2)
        self.f_lbl3.place(x=1000, y=0, width=550, height=130)

        # bg image
        img3 = Image.open(r"C:\Users\HP\Desktop\My images\background.PNG")
        img3 = img3.resize((1536, 709), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        self.bg_image = Label(self.root, image=self.photoimg3)
        self.bg_image.place(x=0, y=130, width=1530, height=710)

        self.title_lbl = Label(self.bg_image, text="STUDENT MANAGEMENT SYSTEM", font=("times new roman", 35, "bold"), bg="white", fg="darkgreen")
        self.title_lbl.place(x=0, y=0, width=1530, height=45)

        main_frame = Frame(self.bg_image, bd=2, bg="white")
        main_frame.place(x=10, y=55, width=1500, height=600)

        # Left label frame
        left_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text="Student Details", font=("times new roman", 12, "bold"))
        left_frame.place(x=10, y=10, width=760, height=580)

        img_left = Image.open(r"C:\Users\HP\Desktop\My images\student7.PNG")
        img_left = img_left.resize((750, 130), Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img_left)

        self.f_lbl3 = Label(left_frame, image=self.photoimg_left)
        self.f_lbl3.place(x=5, y=0, width=750, height=130)

        # Current course
        current_course_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Current course information", font=("times new roman", 12, "bold"))
        current_course_frame.place(x=5, y=135, width=720, height=115)

        # Department
        dep_label = Label(current_course_frame, text="Department", font=("times new roman", 13, "bold"), bg="white")
        dep_label.grid(row=0, column=0, padx=10)

        dep_combo = ttk.Combobox(current_course_frame, textvariable=self.var_dep, font=("times new roman", 13, "bold"), state="readonly", width=20)
        dep_combo["values"] = ("Select Department", "Computer", "IT", "Civil", "Mechanical", "MCA")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        # Course
        course_label = Label(current_course_frame, text="Course", font=("times new roman", 13, "bold"), bg="white")
        course_label.grid(row=0, column=2, padx=10, sticky=W)

        course_combo = ttk.Combobox(current_course_frame, textvariable=self.var_course, font=("times new roman", 13, "bold"), state="readonly", width=20)
        course_combo["values"] = ("Select Course", "FE", "SE", "TE", "BE")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=2, pady=10, sticky=W)

        # Year
        year_label = Label(current_course_frame, text="Year", font=("times new roman", 13, "bold"), bg="white")
        year_label.grid(row=1, column=0, padx=10, sticky=W)

        year_combo = ttk.Combobox(current_course_frame, textvariable=self.var_year, font=("times new roman", 13, "bold"), state="readonly", width=20)
        year_combo["values"] = ("Select Year", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25")
        year_combo.current(0)
        year_combo.grid(row=1, column=1, padx=2, pady=10, sticky=W)

        # Semester
        semester_label = Label(current_course_frame, text="Semester", font=("times new roman", 13, "bold"), bg="white")
        semester_label.grid(row=1, column=2, padx=10, sticky=W)

        semester_combo = ttk.Combobox(current_course_frame, textvariable=self.var_semester, font=("times new roman", 13, "bold"), state="readonly", width=20)
        semester_combo["values"] = ("Select Semester", "Semester-1", "Semester-2", "Semester-3", "Semester-4", "Semester-5", "Semester-6")
        semester_combo.current(0)
        semester_combo.grid(row=1, column=3, padx=2, pady=10, sticky=W)

        # Class Student information
        Class_Student_frame = LabelFrame(left_frame, bd=2, bg="white", relief=RIDGE, text="Class Student information", font=("times new roman", 12, "bold"))
        Class_Student_frame.place(x=5, y=250, width=720, height=300)

        # Student ID
        studentId_label = Label(Class_Student_frame, text="StudentID:", font=("times new roman", 13, "bold"), bg="white")
        studentId_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        studentID_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_std_id, width=20, font=("times new roman", 13, "bold"))
        studentID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W)

        # Student name
        studentName_label = Label(Class_Student_frame, text="Student Name:", font=("times new roman", 13, "bold"), bg="white")
        studentName_label.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        studentName_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_std_name, width=20, font=("times new roman", 13, "bold"))
        studentName_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)

        # Class division
        class_div_label = Label(Class_Student_frame, text="Class Division:", font=("times new roman", 13, "bold"), bg="white")
        class_div_label.grid(row=1, column=0, padx=10, pady=5, sticky=W)

        div_combo = ttk.Combobox(Class_Student_frame, textvariable=self.var_div, font=("times new roman", 13, "bold"), state="readonly", width=18)
        div_combo["values"] = ("A", "B", "C")
        div_combo.current(0)
        div_combo.grid(row=1, column=1, padx=10, pady=5, sticky=W)

        # Roll No
        roll_no_label = Label(Class_Student_frame, text="Roll No:", font=("times new roman", 13, "bold"), bg="white")
        roll_no_label.grid(row=1, column=2, padx=10, pady=5, sticky=W)

        roll_no_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_roll, width=20, font=("times new roman", 13, "bold"))
        roll_no_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W)

        # Gender
        gender_label = Label(Class_Student_frame, text="Gender:", font=("times new roman", 13, "bold"), bg="white")
        gender_label.grid(row=2, column=0, padx=10, pady=5, sticky=W)

        gender_combo = ttk.Combobox(Class_Student_frame, textvariable=self.var_gender, font=("times new roman", 13, "bold"), state="readonly", width=18)
        gender_combo["values"] = ("Male", "Female", "Other")
        gender_combo.current(0)
        gender_combo.grid(row=2, column=1, padx=10, pady=5, sticky=W)

        # DOB
        dob_label = Label(Class_Student_frame, text="Date Of Birth:", font=("times new roman", 13, "bold"), bg="white")
        dob_label.grid(row=2, column=2, padx=10, pady=5, sticky=W)

        dob_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_dob, width=20, font=("times new roman", 13, "bold"))
        dob_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W)

        # Email
        email_label = Label(Class_Student_frame, text="Email:", font=("times new roman", 13, "bold"), bg="white")
        email_label.grid(row=3, column=0, padx=10, pady=5, sticky=W)

        email_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_email, width=20, font=("times new roman", 13, "bold"))
        email_entry.grid(row=3, column=1, padx=10, pady=5, sticky=W)

        # Phone No
        phone_label = Label(Class_Student_frame, text="Phone No:", font=("times new roman", 13, "bold"), bg="white")
        phone_label.grid(row=3, column=2, padx=10, pady=5, sticky=W)

        phone_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_phone, width=20, font=("times new roman", 13, "bold"))
        phone_entry.grid(row=3, column=3, padx=10, pady=5, sticky=W)

        # Address
        address_label = Label(Class_Student_frame, text="Address:", font=("times new roman", 13, "bold"), bg="white")
        address_label.grid(row=4, column=0, padx=10, pady=5, sticky=W)

        address_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_address, width=20, font=("times new roman", 13, "bold"))
        address_entry.grid(row=4, column=1, padx=10, pady=5, sticky=W)

        # Teacher Name
        teacher_label = Label(Class_Student_frame, text="Teacher Name:", font=("times new roman", 13, "bold"), bg="white")
        teacher_label.grid(row=4, column=2, padx=10, pady=5, sticky=W)

        teacher_entry = ttk.Entry(Class_Student_frame, textvariable=self.var_teacher, width=20, font=("times new roman", 13, "bold"))
        teacher_entry.grid(row=4, column=3, padx=10, pady=5, sticky=W)

        # Radio Buttons
        radionbtn1 = ttk.Radiobutton(Class_Student_frame, variable=self.var_radio1, text="Take Photo Sample", value="Yes")
        radionbtn1.grid(row=6, column=0)

        radionbtn2 = ttk.Radiobutton(Class_Student_frame, variable=self.var_radio1, text="No Photo Sample", value="No")
        radionbtn2.grid(row=6, column=1)

        # Buttons Frame
        btn_frame = Frame(Class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame.place(x=0, y=200, width=715, height=35)

        save_btn = Button(btn_frame, text="Save", width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white", command=self.add_data)
        save_btn.grid(row=0, column=0)

        update_btn = Button(btn_frame, text="Update", width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white", command=self.update_data)
        update_btn.grid(row=0, column=1)

        delete_btn = Button(btn_frame, text="Delete", width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white", command=self.delete_data)
        delete_btn.grid(row=0, column=2)

        reset_btn = Button(btn_frame, text="Reset", width=17, font=("times new roman", 13, "bold"), bg="blue", fg="white", command=self.reset_data)
        reset_btn.grid(row=0, column=3)

        btn_frame1 = Frame(Class_Student_frame, bd=2, relief=RIDGE, bg="white")
        btn_frame1.place(x=0, y=235, width=715, height=35)

        take_photo_btn = Button(btn_frame1,command=self.generate_dataset, text="Take Photo Sample", width=35, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        take_photo_btn.grid(row=0, column=0)

        update_photo_btn = Button(btn_frame1, text="Update Photo Sample", width=35, font=("times new roman", 13, "bold"), bg="blue", fg="white")
        update_photo_btn.grid(row=0, column=1)

        # Right label frame
        Right_frame = LabelFrame(main_frame, bd=2, bg="white", relief=RIDGE, text=" Student Details", font=("times new roman", 12, "bold"))
        Right_frame.place(x=780, y=10, width=700, height=580)

        img_right = Image.open(r"C:\Users\HP\Desktop\My images\student15.PNG")
        img_right = img_right.resize((750, 130), Image.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        self.f_lbl3 = Label(Right_frame, image=self.photoimg_right)
        self.f_lbl3.place(x=5, y=0, width=750, height=130)

        # Search System
        Search_frame = LabelFrame(Right_frame, bd=2, bg="white", relief=RIDGE, text="Search System", font=("times new roman", 12, "bold"))
        Search_frame.place(x=5, y=135, width=690, height=70)

        Search_label = Label(Search_frame, text="Search By:", font=("times new roman", 15, "bold"), bg="red", fg="white")
        Search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        Search_combo = ttk.Combobox(Search_frame, font=("times new roman", 13, "bold"), state="readonly", width=15)
        Search_combo["values"] = ("Select", "Roll_No", "Phone_No", "Address", "Name", "Email", "Course")
        Search_combo.current(0)
        Search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        search_entry = ttk.Entry(Search_frame, width=15, font=("times new roman", 13, "bold"))
        search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        search_btn = Button(Search_frame, text="Search", width=12, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        search_btn.grid(row=0, column=3, padx=4)

        showAll_btn = Button(Search_frame, text="Show All", width=12, font=("times new roman", 12, "bold"), bg="blue", fg="white")
        showAll_btn.grid(row=0, column=4, padx=4)

        # ==================table frame===============
        table_frame = Frame(Right_frame, bd=2, bg="white", relief=RIDGE)
        table_frame.place(x=5, y=210, width=690, height=350)

        scroll_x = ttk.Scrollbar(table_frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=VERTICAL)

        self.student_table = ttk.Treeview(table_frame, column=("dep", "course", "year", "sem", "id", "name", "div", "roll", "gender", "dob", "email", "phone", "address", "teacher", "photo"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)

        self.student_table.heading("dep", text="Department")
        self.student_table.heading("course", text="Course")
        self.student_table.heading("year", text="Year")
        self.student_table.heading("sem", text="Semester")
        self.student_table.heading("id", text="StudentId")
        self.student_table.heading("name", text="Name")
        self.student_table.heading("div", text="Division")
        self.student_table.heading("roll", text="Roll No")
        self.student_table.heading("gender", text="Gender")
        self.student_table.heading("dob", text="DOB")
        self.student_table.heading("email", text="Email")
        self.student_table.heading("phone", text="Phone")
        self.student_table.heading("address", text="Address")
        self.student_table.heading("teacher", text="Teacher")
        self.student_table.heading("photo", text="PhotoSampleStatus")
        self.student_table["show"] = "headings"

        self.student_table.column("dep", width=100)
        self.student_table.column("course", width=100)
        self.student_table.column("year", width=100)
        self.student_table.column("sem", width=100)
        self.student_table.column("id", width=100)
        self.student_table.column("name", width=100)
        self.student_table.column("roll", width=100)
        self.student_table.column("gender", width=100)
        self.student_table.column("div", width=100)
        self.student_table.column("dob", width=100)
        self.student_table.column("email", width=100)
        self.student_table.column("phone", width=100)
        self.student_table.column("address", width=100)
        self.student_table.column("teacher", width=100)
        self.student_table.column("photo", width=100)

        self.student_table.pack(fill=BOTH, expand=1)
        self.student_table.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()

    # =============Function declaration===========
    def add_data(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get() == "" or self.var_std_id.get() == "":
            messagebox.showerror("Error", "All Fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="B@b@2208", database="face_recognizer")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO student VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.var_year.get(),
                    self.var_semester.get(),
                    self.var_std_id.get(),
                    self.var_std_name.get(),
                    self.var_div.get(),
                    self.var_roll.get(),
                    self.var_gender.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_teacher.get(),
                    self.var_radio1.get()
                ))
                conn.commit()
                self.fetch_data()
                messagebox.showinfo("Success", "Student details have been added successfully", parent=self.root)
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
            finally:
                conn.close()

    # =============fetch data===========
    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="B@b@2208", database="face_recognizer")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM student")
            data = my_cursor.fetchall()

            if len(data) != 0:
                self.student_table.delete(*self.student_table.get_children())
                for i in data:
                    self.student_table.insert("", END, values=i)
            conn.commit()
        except Exception as es:
            messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
        finally:
            conn.close()

    #===============get cursor======
    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]

        self.var_dep.set(data[0])
        self.var_course.set(data[1])
        self.var_year.set(data[2])
        self.var_semester.set(data[3])
        self.var_std_id.set(data[4])
        self.var_std_name.set(data[5])
        self.var_div.set(data[6])
        self.var_roll.set(data[7])
        self.var_gender.set(data[8])
        self.var_dob.set(data[9])
        self.var_email.set(data[10])
        self.var_phone.set(data[11])
        self.var_address.set(data[12])
        self.var_teacher.set(data[13])
        self.var_radio1.set(data[14])

    # Update function
    def update_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required", parent=self.root)
        else:
            try:
                Update = messagebox.askyesno("Update", "Do you want to update this student details", parent=self.root)
                if Update > 0:
                    conn = mysql.connector.connect(host="localhost", username="root", password="B@b@2208", database="face_recognizer")
                    my_cursor = conn.cursor()
                    my_cursor.execute("UPDATE student SET Dep=%s, course=%s, Year=%s, Semester=%s, Name=%s, Division=%s, Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s, PhotoSample=%s WHERE Student_id=%s",(
                      
                        self.var_dep.get(),
                        self.var_course.get(),
                        self.var_year.get(),
                        self.var_semester.get(),
                        self.var_std_name.get(),
                        self.var_div.get(),
                        self.var_roll.get(),
                        self.var_gender.get(),
                        self.var_dob.get(),
                        self.var_email.get(),
                        self.var_phone.get(),
                        self.var_address.get(),
                        self.var_teacher.get(),
                        self.var_radio1.get(),
                        self.var_std_id.get()
                    ))
                    conn.commit()
                    self.fetch_data()
                    messagebox.showinfo("Success", "Student details have been updated successfully", parent=self.root)
                else:
                    if not Update:
                        return
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
            finally:
                conn.close()

    # Delete function
    def delete_data(self):
        if self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required", parent=self.root)
        else:
            try:
                delete = messagebox.askyesno("Student Delete Page", "Do you want to delete this student", parent=self.root)
                if delete > 0:
                    conn = mysql.connector.connect(host="localhost", username="root", password="B@b@2208", database="face_recognizer")
                    my_cursor = conn.cursor()
                    # sql = "DELETE FROM student WHERE id=%s"
                    sql = "DELETE FROM student WHERE student_id=%s"
                    val = (self.var_std_id.get(),)
                    my_cursor.execute(sql, val)
                    conn.commit()
                    self.fetch_data()
                    messagebox.showinfo("Delete", "Successfully deleted student details", parent=self.root)
                else:
                    if not delete:
                        return
            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)
            finally:
                conn.close()

    # Reset function
    def reset_data(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.var_year.set("Select Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_std_name.set("")
        self.var_div.set("Select Division")
        self.var_roll.set("")
        self.var_gender.set("Male")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_teacher.set("")
        self.var_radio1.set("Yes")


   



    def generate_dataset(self):
        if self.var_dep.get() == "Select Department" or self.var_std_name.get().strip()==" "or self.var_std_id.get() == "":
            messagebox.showerror("Error", "Student ID must be required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="B@b@2208",
                    database="face_recognizer"
                )
                my_cursor = conn.cursor()
                my_cursor.execute("select * FROM Student WHERE student_id=%s",(self.var_std_id.get(),))
                myresult = my_cursor.fetchall()
                
                id = 0  # Initialize id

                for x in myresult:
                    id += 1
                    my_cursor.execute(
                        "UPDATE student SET Dep=%s, course=%s, Year=%s, Semester=%s, Name=%s, Division=%s, Roll=%s, Gender=%s, Dob=%s, Email=%s, Phone=%s, Address=%s, Teacher=%s, PhotoSample=%s WHERE Student_id=%s",
                        (
                            self.var_dep.get(),
                            self.var_course.get(),
                            self.var_year.get(),
                            self.var_semester.get(),
                            self.var_std_name.get(),
                            self.var_div.get(),
                            self.var_roll.get(),
                            self.var_gender.get(),
                            self.var_dob.get(),
                            self.var_email.get(),
                            self.var_phone.get(),
                            self.var_address.get(),
                            self.var_teacher.get(),
                            self.var_radio1.get(),
                            self.var_std_id.get()
                        )
                    )
                
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                #======== Load predefined data on frontalface from open-cv====
                face_classifier = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

                def face_cropped(img):
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

                    for (x, y, w, h) in faces:
                        face_cropped = img[y:y + h, x:x + w]
                        return face_cropped
                    
                    return None   # यदि कोई चेहरा नहीं मिला, तो None रिटर्न करें

                cap = cv2.VideoCapture(0)
                img_id = 0

                while True:
                    ret, my_frame = cap.read()
                    if not ret:
                        print("Failed to capture frame")
                        break

                    face = face_cropped(my_frame)  
                    if face is not None:
                        img_id += 1
                        face = cv2.resize(face,(450, 450))
                        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                        # file_name_path = f"data/user.{self.var_std_id.get()}.{img_id}.jpg"
                        # file_name_path= ' data/{StudentID}.{ImageNumber}.jpg'
                        file_name_path ="data/user."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path,face)

                        cv2.putText(face, str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX, 2, (0, 255, 0), 2)
                        cv2.imshow("Cropped Face", face)

                    # if cv2.waitKey(1) == 13 or id(img_id) == 100:  # Stop capturing after 100 images or when Enter key is pressed
                    if cv2.waitKey(1) == 13 or img_id == 100:
 
                        break

                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result", "Dataset generation completed successfully!!!")

            except Exception as es:
                messagebox.showerror("Error", f"Due to: {str(es)}", parent=self.root)

# Main Execution
if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()

        
