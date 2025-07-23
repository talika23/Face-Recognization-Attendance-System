import time
import cv2
import pandas as pd
import numpy as np
from threading import Thread
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import mysql.connector
import os


class EnhancedFaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Enhanced Face Recognition System")

        # Initialize variables
        self.attendance_df = pd.DataFrame(columns=["ID", "Name", "Department", "Date", "Time", "Status"])
        self.recognition_active = False
        self.confidence_threshold = 75
        
        # UI Setup
        self.setup_ui()
        
    def setup_ui(self):
        # Title label
        self.title_lbl = Label(self.root, text="ENHANCED FACE RECOGNITION", 
                             font=("times new roman", 35, "bold"), 
                             bg="white", fg="darkgreen")
        self.title_lbl.place(x=0, y=0, width=1530, height=45)
       
        # Left image frame
        img_top = Image.open("My images/face detector.png")
        img_top = img_top.resize((650, 700), Image.LANCZOS)
        self.photoimg_top = ImageTk.PhotoImage(img_top)
        self.f_lbl1 = Label(self.root, image=self.photoimg_top)
        self.f_lbl1.place(x=0, y=55, width=650, height=700)

        # Right control frame
        img_bottom = Image.open("My images/accuracy1.png")
        img_bottom = img_bottom.resize((950, 700), Image.LANCZOS)
        self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
        self.f_lbl2 = Label(self.root, image=self.photoimg_bottom)
        self.f_lbl2.place(x=650, y=55, width=950, height=700)
        
        # Add enhancement controls
        self.add_enhancements()
        
        # Face recognition button
        self.b1_1 = Button(self.f_lbl2, text="Start Recognition", cursor="hand2",
                         font=("times new roman", 18, "bold"), bg="blue", fg="white",
                         command=self.toggle_recognition)
        self.b1_1.place(x=365, y=500, width=200, height=40)
        
    def add_enhancements(self):
        # Confidence threshold control
        self.threshold_label = Label(self.f_lbl2, text="Confidence Threshold:", 
                                    font=("times new roman", 12), bg="white")
        self.threshold_label.place(x=50, y=550)
        
        self.threshold_slider = Scale(self.f_lbl2, from_=50, to=95, orient=HORIZONTAL,
                                    command=self.update_threshold, bg="white")
        self.threshold_slider.set(self.confidence_threshold)
        self.threshold_slider.place(x=200, y=550, width=200)
        
        # Liveness detection toggle
        self.liveness_var = IntVar(value=1)
        self.liveness_cb = Checkbutton(self.f_lbl2, text="Enable Liveness Detection", 
                                     variable=self.liveness_var, font=("times new roman", 12),
                                     bg="white")
        self.liveness_cb.place(x=50, y=580)
        
        # Attendance report button
        self.report_btn = Button(self.f_lbl2, text="Generate Report", command=self.generate_report,
                               font=("times new roman", 12), bg="green", fg="white")
        self.report_btn.place(x=50, y=620)
    
    def update_threshold(self, val):
        self.confidence_threshold = int(val)
        
    def check_liveness(self, frame):
        """Basic liveness detection using eye blink analysis"""
        if not self.liveness_var.get():
            return True
            
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect eyes
        eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
        
        return len(eyes) >= 2  # At least 2 eyes detected
        
    def draw_boundary(self, img, classifier, scaleFactor, minNeighbors, clf):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        features = classifier.detectMultiScale(gray_image, scaleFactor, minNeighbors)

        for (x, y, w, h) in features:
            if not self.check_liveness(img[y:y+h, x:x+w]):
                cv2.putText(img, "SPOOF ATTEMPT!", (x, y-80), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                continue
                
            id, predict = clf.predict(gray_image[y:y + h, x:x + w])
            confidence = int((100 * (1 - predict / 300)))
            
            if confidence > self.confidence_threshold:
                # Get student info from database
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="B@b@2208",
                    database="face_recognizer"
                )
                cursor = conn.cursor()
                
                cursor.execute("SELECT * FROM student WHERE Student_id=%s", (id,))
                result = cursor.fetchone()
                
                if result:
                    # Draw info on frame
                    cv2.putText(img, f"ID: {result[0]}", (x, y-75), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Name: {result[1]}", (x, y-55), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    cv2.putText(img, f"Dept: {result[2]}", (x, y-30), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                    
                    # Mark attendance
                    self.mark_attendance(result[0], result[1], result[2])
                else:
                    cv2.putText(img, "Unknown", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 3)
                
                conn.close()
                
        return img
        
    def mark_attendance(self, student_id, name, department):
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Check if already marked today
        today_attendance = self.attendance_df[
            (self.attendance_df['ID'] == student_id) & 
            (self.attendance_df['Date'] == date_str)
        ]
        
        if len(today_attendance) == 0:
            new_entry = {
                "ID": student_id,
                "Name": name,
                "Department": department,
                "Date": date_str,
                "Time": time_str,
                "Status": "Present"
            }
            self.attendance_df = pd.concat([self.attendance_df, pd.DataFrame([new_entry])], ignore_index=True)
            
    def toggle_recognition(self):
        if not self.recognition_active:
            self.recognition_active = True
            self.b1_1.config(text="Stop Recognition", bg="red")
            Thread(target=self.face_recognition_thread, daemon=True).start()
        else:
            self.recognition_active = False
            self.b1_1.config(text="Start Recognition", bg="blue")
            
    def face_recognition_thread(self):
        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        clf = cv2.face.LBPHFaceRecognizer_create()
        clf.read("classifier.xml")
        
        video_cap = cv2.VideoCapture(0)
        
        while self.recognition_active:
            ret, img = video_cap.read()
            if not ret:
                break
                
            img = self.draw_boundary(img, faceCascade, 1.1, 10, clf)
            cv2.imshow("Face Recognition", img)
            
            if cv2.waitKey(1) == 13:  # Enter key
                break
                
        video_cap.release()
        cv2.destroyAllWindows()
        
    def generate_report(self):
        """Generate attendance report for selected date range"""
        report_window = Toplevel(self.root)
        report_window.title("Attendance Report")
        report_window.geometry("800x600")
        
        # Date range selection
        Label(report_window, text="From:").pack()
        self.from_date = DateEntry(report_window)
        self.from_date.pack()
        
        Label(report_window, text="To:").pack()
        self.to_date = DateEntry(report_window)
        self.to_date.pack()
        
        Button(report_window, text="Generate", command=self._generate_report_data).pack()
        
        # Report display area
        self.report_text = Text(report_window, height=20, width=90)
        self.report_text.pack()
        
        Button(report_window, text="Export to Excel", command=self.export_to_excel).pack()
        
    def _generate_report_data(self):
        try:
            from_date = self.from_date.get_date()
            to_date = self.to_date.get_date() + timedelta(days=1)  # Include end date
            
            # Convert to string format for comparison
            from_str = from_date.strftime("%Y-%m-%d")
            to_str = to_date.strftime("%Y-%m-%d")
            
            # Filter data
            mask = (self.attendance_df['Date'] >= from_str) & (self.attendance_df['Date'] <= to_str)
            filtered_df = self.attendance_df.loc[mask]
            
            # Generate report
            report = filtered_df.groupby(['ID', 'Name', 'Date']).size().unstack(fill_value=0)
            self.report_text.delete(1.0, END)
            self.report_text.insert(END, report.to_string())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate report: {str(e)}")
            
    def export_to_excel(self):
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Excel files", "*.xlsx")]
            )
            if filename:
                self.attendance_df.to_excel(filename, index=False)
                messagebox.showinfo("Success", "Report exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")

if __name__ == "__main__":
    root = Tk()
    obj = EnhancedFaceRecognition(root)
    root.mainloop()