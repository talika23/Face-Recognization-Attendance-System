
import time
import cv2
import pandas as pd
import numpy as np
from threading import Thread
from datetime import datetime, timedelta
from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
import matplotlib.pyplot as plt
from PIL import Image, ImageTk, ImageOps
import mysql.connector
import os
import webbrowser
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import seaborn as sns
import qrcode
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pickle
import face_recognition1 as fr  # Additional face recognition library for better accuracy

# Configure styles
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8')  # For newer Matplotlib versions
# Ensure haarcascades are available
print(plt.style.available)
HAARCASCADES_PATH = cv2.data.haarcascades

class EnhancedFaceRecognition:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Enhanced Face Recognition System")
        self.root.configure(bg="#f0f2f5")  # Light gray background for modern look
        
        # Set window icon
        try:
            self.root.iconbitmap('icon.ico')  # Provide your own icon file
        except:
            pass

        # Custom style for the application
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure styles
        self.configure_styles()
        
        # Initialize variables
        self.initialize_variables()
        
        # UI Setup
        self.setup_ui()

        # Load existing data
        self.load_initial_data()

    def configure_styles(self):
        """Configure all the custom styles for the application"""
        self.style.configure('TButton', font=('Segoe UI', 12), padding=8, 
                           background='#4a6baf', foreground='white')
        self.style.map('TButton', 
                      background=[('active', '#3a5a9f'), ('disabled', '#d3d3d3')])
        
        self.style.configure('Primary.TButton', font=('Segoe UI', 12, 'bold'), 
                           background='#4a6baf', foreground='white')
        
        self.style.configure('Secondary.TButton', font=('Segoe UI', 11), 
                           background='#6c757d', foreground='white')
        
        self.style.configure('Success.TButton', font=('Segoe UI', 11), 
                           background='#28a745', foreground='white')
        
        self.style.configure('Danger.TButton', font=('Segoe UI', 11), 
                           background='#dc3545', foreground='white')
        
        self.style.configure('TLabel', font=('Segoe UI', 11), background="#f0f2f5", 
                           foreground='#333333')
        
        self.style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), 
                           background="#f0f2f5", foreground='#2c3e50')
        
        self.style.configure('TFrame', background="#f0f2f5")
        
        self.style.configure('TLabelframe', background="#ffffff", foreground='#2c3e50', 
                           font=('Segoe UI', 12, 'bold'), borderwidth=2)
        
        self.style.configure('TLabelframe.Label', background="#ffffff", 
                           foreground='#2c3e50')
        
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=30, 
                           background='#ffffff', foreground='#333333', 
                           fieldbackground='#ffffff', bordercolor='#dee2e6', 
                           borderwidth=1)
        
        self.style.map('Treeview', background=[('selected', '#4a6baf')])
        
        self.style.configure('Treeview.Heading', font=('Segoe UI', 11, 'bold'), 
                           background='#4a6baf', foreground='white')
        
        self.style.map('Treeview.Heading', background=[('active', '#3a5a9f')])
        
        self.style.configure('TCombobox', font=('Segoe UI', 11), 
                           fieldbackground='#ffffff', background='#f8f9fa')
        
        self.style.configure('TCheckbutton', background="#f0f2f5", 
                           font=('Segoe UI', 11))
        
        self.style.configure('Horizontal.TScale', background="#f0f2f5", 
                           troughcolor="#d3d8e0")
        
        self.style.configure('TNotebook', background="#f0f2f5", borderwidth=0)
        self.style.configure('TNotebook.Tab', background="#e9ecef", 
                           foreground='#495057', padding=[10, 5], 
                           font=('Segoe UI', 10, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', '#ffffff')])

    def initialize_variables(self):
        """Initialize all the variables used in the application"""
        self.attendance_df = pd.DataFrame(columns=["ID", "Name", "Department", "Date", "Time", "Status", "Confidence"])
        self.recognition_active = False
        self.confidence_threshold = 85  # Higher default threshold for better accuracy
        self.camera_index = 0  # Default camera
        self.last_marked_time = {}  # To prevent rapid re-marking for the same person
        self.known_face_encodings = []
        self.known_face_ids = []
        self.face_detection_method = 'haar'  # 'haar' or 'dlib' or 'cnn'
        self.email_settings = {
            'sender': 'your_email@example.com',
            'password': 'your_password',
            'smtp_server': 'smtp.example.com',
            'smtp_port': 587
        }
        self.system_settings = {
            'auto_save_interval': 5,  # minutes
            'notify_missing': True,
            'dark_mode': False
        }
        self.face_recognizer = None
        self.capture = None
        self.current_frame = None
        self.photo_camera = None
        self.filtered_report_df = None
        self.last_save_time = datetime.now()
        self.auto_save_thread = None
        self.auto_save_running = True

    def setup_ui(self):
        """Setup the main user interface"""
        # Main container frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)

        # Title frame with modern design
        self.setup_title_frame()
        
        # Content frame
        self.content_frame = ttk.Frame(self.main_frame, style='TFrame')
        self.content_frame.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        # Left frame - Camera view and controls
        self.setup_camera_frame()
        
        # Right frame - Controls and analytics
        self.setup_analytics_frame()

        # Status bar
        self.setup_status_bar()
        
        # Start auto-save thread
        self.start_auto_save()

    def setup_title_frame(self):
        """Setup the title frame with logo and title"""
        self.title_frame = Frame(self.main_frame, bg="#2c3e50", height=90, bd=0, relief="solid")
        self.title_frame.pack(fill=X)
        
        # Logo (placeholder - replace with your own logo)
        try:
            logo_img = Image.open('logo.png').resize((60, 60), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = Label(self.title_frame, image=self.logo, bg="#2c3e50")
            logo_label.pack(side=LEFT, padx=(20, 10), pady=10)
        except:
            pass
        
        # Title label
        self.title_lbl = Label(self.title_frame, 
                              text="ENHANCED FACE RECOGNITION ATTENDANCE SYSTEM",
                              font=("Segoe UI", 24, "bold"), 
                              bg="#2c3e50", fg="white")
        self.title_lbl.pack(side=LEFT, pady=25)
        
        # Add a settings button
        settings_btn = ttk.Button(self.title_frame, text="⚙", width=3, 
                                command=self.open_settings,
                                style='Secondary.TButton')
        settings_btn.pack(side=RIGHT, padx=20, pady=10)

    def setup_camera_frame(self):
        """Setup the camera frame with live feed and controls"""
        self.left_frame = ttk.LabelFrame(self.content_frame, text="Live Camera Feed", 
                                        style='TLabelframe')
        self.left_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))
        
        # Camera view with border
        camera_container = Frame(self.left_frame, bg='#4a6baf', bd=0)
        camera_container.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Placeholder for camera image
        self.camera_placeholder = Image.new('RGB', (650, 500), color='#343a40')
        self.photo_camera = ImageTk.PhotoImage(self.camera_placeholder)
        self.camera_label = Label(camera_container, image=self.photo_camera, 
                                bg="black", bd=0)
        self.camera_label.pack(fill=BOTH, expand=True, padx=2, pady=2)
        
        # Camera controls frame
        controls_frame = ttk.Frame(self.left_frame, style='TFrame')
        controls_frame.pack(fill=X, padx=10, pady=(0, 10))
        
        # Recognition button with icon
        self.recognition_btn = ttk.Button(controls_frame, 
                                        text="▶ Start Recognition",
                                        command=self.toggle_recognition, 
                                        style='Primary.TButton')
        self.recognition_btn.pack(side=LEFT, padx=(0, 10))
        
        # Capture photo button
        self.capture_btn = ttk.Button(controls_frame, text="📷 Capture Photo",
                                    command=self.capture_photo,
                                    style='Secondary.TButton')
        self.capture_btn.pack(side=LEFT, padx=10)
        
        # Face detection method
        self.detection_method = StringVar(value='haar')
        methods = [('Haar Cascade', 'haar'), 
                  ('Dlib (More Accurate)', 'dlib'), 
                  ('CNN (Most Accurate)', 'cnn')]
        
        for text, mode in methods:
            rb = ttk.Radiobutton(controls_frame, text=text, variable=self.detection_method, 
                                value=mode, style='TCheckbutton')
            rb.pack(side=LEFT, padx=10)

    def setup_analytics_frame(self):
        """Setup the analytics frame with tabs and controls"""
        self.right_frame = ttk.LabelFrame(self.content_frame, 
                                         text="System Controls & Analytics", 
                                         style='TLabelframe')
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=(10, 0))
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.right_frame, style='TNotebook')
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Add tabs
        self.add_control_tab()
        self.add_attendance_tab()
        self.add_statistics_tab()
        self.add_charts_tab()
        self.add_admin_tab()
        
        # Bind tab change event
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def add_control_tab(self):
        """Add the control tab to the notebook"""
        control_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(control_tab, text="Controls")
        
        # Confidence threshold control
        threshold_frame = ttk.LabelFrame(control_tab, text="Recognition Settings", 
                                       style='TLabelframe')
        threshold_frame.pack(fill=X, pady=5, padx=5)
        
        ttk.Label(threshold_frame, text="Confidence Threshold:", 
                background='#ffffff').pack(side=LEFT, padx=5, pady=5)
        
        self.threshold_slider = Scale(threshold_frame, from_=70, to=99, 
                                    orient=HORIZONTAL, command=self.update_threshold,
                                    bg="white", troughcolor="#d3d8e0", 
                                    activebackground="#4a6baf", highlightthickness=0,
                                    length=200, resolution=1)
        self.threshold_slider.set(self.confidence_threshold)
        self.threshold_slider.pack(side=LEFT, padx=5, pady=5)
        
        self.threshold_label = ttk.Label(threshold_frame, 
                                      text=f"{self.confidence_threshold}%", 
                                      background='#ffffff', 
                                      font=('Segoe UI', 10, 'bold'))
        self.threshold_label.pack(side=LEFT, padx=5, pady=5)
        
        # Camera selection
        camera_frame = ttk.LabelFrame(control_tab, text="Camera Settings", 
                                    style='TLabelframe')
        camera_frame.pack(fill=X, pady=5, padx=5)
        
        ttk.Label(camera_frame, text="Camera Source:", 
                background='#ffffff').pack(side=LEFT, padx=5, pady=5)
        
        self.camera_var = StringVar()
        self.camera_dropdown = ttk.Combobox(camera_frame, textvariable=self.camera_var,
                                          values=["Default Camera (0)", 
                                                "Secondary Camera (1)", 
                                                "Tertiary Camera (2)"], 
                                          width=20)
        self.camera_dropdown.current(0)
        self.camera_dropdown.pack(side=LEFT, padx=5, pady=5)
        self.camera_dropdown.bind("<<ComboboxSelected>>", self.on_camera_select)
        
        # Security features
        security_frame = ttk.LabelFrame(control_tab, text="Security Features", 
                                      style='TLabelframe')
        security_frame.pack(fill=X, pady=5, padx=5)
        
        self.liveness_var = IntVar(value=1)
        self.liveness_cb = ttk.Checkbutton(security_frame, 
                                          text="Liveness Detection",
                                          variable=self.liveness_var, 
                                          style='TCheckbutton')
        self.liveness_cb.pack(side=LEFT, padx=5, pady=5)
        
        self.mask_var = IntVar(value=0)
        self.mask_cb = ttk.Checkbutton(security_frame, 
                                     text="Mask Detection (Beta)",
                                     variable=self.mask_var, 
                                     style='TCheckbutton')
        self.mask_cb.pack(side=LEFT, padx=5, pady=5)
        
        # Report buttons
        report_frame = ttk.LabelFrame(control_tab, text="Reports & Export", 
                                    style='TLabelframe')
        report_frame.pack(fill=X, pady=5, padx=5)
        
        btn_frame = ttk.Frame(report_frame, style='TFrame')
        btn_frame.pack(fill=X, pady=5)
        
        self.report_btn = ttk.Button(btn_frame, text="📊 Generate Report",
                                   command=self.generate_report, 
                                   style='Primary.TButton')
        self.report_btn.pack(side=LEFT, padx=5, expand=True, fill=X)
        
        self.export_btn = ttk.Button(btn_frame, text="📁 Export Data",
                                   command=self.export_to_excel, 
                                   style='Success.TButton')
        self.export_btn.pack(side=LEFT, padx=5, expand=True, fill=X)
        
        self.email_btn = ttk.Button(btn_frame, text="✉ Email Report",
                                  command=self.email_report, 
                                  style='Secondary.TButton')
        self.email_btn.pack(side=LEFT, padx=5, expand=True, fill=X)
        
        # Help button
        help_frame = ttk.Frame(control_tab, style='TFrame')
        help_frame.pack(fill=X, pady=5, padx=5)
        
        self.help_btn = ttk.Button(help_frame, text="❔ Help & Documentation",
                                 command=self.show_help, 
                                 style='Secondary.TButton')
        self.help_btn.pack(side=LEFT, padx=5, expand=True, fill=X)

    def add_attendance_tab(self):
        """Add the attendance tab to the notebook"""
        attendance_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(attendance_tab, text="Attendance")
        
        # Create a table for attendance
        self.attendance_tree = ttk.Treeview(attendance_tab, 
                                          columns=("ID", "Name", "Department", "Date", "Time", "Status", "Confidence"), 
                                          show="headings", style='Treeview')
        
        # Configure columns
        columns = [
            ("ID", 80, "center"),
            ("Name", 150, "w"),
            ("Department", 120, "w"),
            ("Date", 100, "center"),
            ("Time", 80, "center"),
            ("Status", 80, "center"),
            ("Confidence", 90, "center")
        ]
        
        for col, width, anchor in columns:
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=width, anchor=anchor)
        
        # Add scrollbars
        scroll_y = ttk.Scrollbar(attendance_tab, orient=VERTICAL, 
                                command=self.attendance_tree.yview)
        scroll_x = ttk.Scrollbar(attendance_tab, orient=HORIZONTAL, 
                                command=self.attendance_tree.xview)
        self.attendance_tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)
        
        # Grid layout
        self.attendance_tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        attendance_tab.grid_rowconfigure(0, weight=1)
        attendance_tab.grid_columnconfigure(0, weight=1)
        
        # Add context menu
        self.setup_attendance_context_menu()



      

    def setup_attendance_context_menu(self):
        """Setup context menu for attendance treeview"""
        self.attendance_menu = Menu(self.root, tearoff=0)
        self.attendance_menu.add_command(label="View Details", 
                                       command=self.view_attendance_details)
        self.attendance_menu.add_command(label="Generate QR Code", 
                                       command=self.generate_qr_for_entry)
        self.attendance_menu.add_separator()
        self.attendance_menu.add_command(label="Delete Entry", 
                                       command=self.delete_attendance_entry)
        
        self.attendance_tree.bind("<Button-3>", self.show_attendance_context_menu)

    def show_attendance_context_menu(self, event):
        """Show context menu for attendance treeview"""
        item = self.attendance_tree.identify_row(event.y)
        if item:
            self.attendance_tree.selection_set(item)
            self.attendance_menu.post(event.x_root, event.y_root)

    def add_statistics_tab(self):
        """Add the statistics tab to the notebook"""
        stats_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(stats_tab, text="Statistics")
        
        # Create a text widget for statistics
        self.stats_text = Text(stats_tab, wrap=WORD, font=("Segoe UI", 10), 
                             height=10, bg='#ffffff', fg='#333333', 
                             relief="flat", bd=1, padx=10, pady=10)
        self.stats_text.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # Add refresh button
        refresh_btn = ttk.Button(stats_tab, text="🔄 Refresh Statistics",
                               command=self.update_statistics,
                               style='Secondary.TButton')
        refresh_btn.pack(side=BOTTOM, pady=5, fill=X, padx=5)

    def add_charts_tab(self):
        """Add the charts tab to the notebook"""
        charts_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(charts_tab, text="Charts")
        
        # Container for charts
        self.chart_canvas_frame = ttk.Frame(charts_tab, style='TFrame')
        self.chart_canvas_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
        
        # Add refresh button
        refresh_btn = ttk.Button(charts_tab, text="🔄 Refresh Charts",
                               command=self.plot_attendance_charts,
                               style='Secondary.TButton')
        refresh_btn.pack(side=BOTTOM, pady=5, fill=X, padx=5)

    def add_admin_tab(self):
        """Add the admin tab to the notebook"""
        admin_tab = ttk.Frame(self.notebook, style='TFrame')
        self.notebook.add(admin_tab, text="Admin")
        
        # Database management frame
        db_frame = ttk.LabelFrame(admin_tab, text="Database Management", 
                                 style='TLabelframe')
        db_frame.pack(fill=X, pady=5, padx=5)
        
        ttk.Button(db_frame, text="🔍 View All Students", 
                  command=self.view_all_students,
                  style='Secondary.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        
        ttk.Button(db_frame, text="➕ Add New Student", 
                  command=self.add_new_student,
                  style='Success.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        
        ttk.Button(db_frame, text="✏️ Edit Student", 
                  command=self.edit_student,
                  style='Secondary.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        
        ttk.Button(db_frame, text="🗑️ Delete Student", 
                  command=self.delete_student,
                  style='Danger.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        
        # System tools frame
        tools_frame = ttk.LabelFrame(admin_tab, text="System Tools", 
                                   style='TLabelframe')
        tools_frame.pack(fill=X, pady=5, padx=5)
        
        ttk.Button(tools_frame, text="🔄 Rebuild Face Encodings", 
                  command=self.rebuild_face_encodings,
                  style='Secondary.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        
        ttk.Button(tools_frame, text="📤 Backup Database", 
                  command=self.backup_database,
                  style='Secondary.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        
        ttk.Button(tools_frame, text="📥 Restore Database", 
                  command=self.restore_database,
                  style='Secondary.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)
        
        ttk.Button(tools_frame, text="⚙️ System Settings", 
                  command=self.open_settings,
                  style='Secondary.TButton').pack(side=LEFT, padx=5, pady=5, fill=X, expand=True)

    def setup_status_bar(self):
        """Setup the status bar at the bottom"""
        self.status_bar = ttk.Frame(self.main_frame, height=30, style='TFrame')
        self.status_bar.pack(fill=X, side=BOTTOM, pady=(0, 5))
        
        # Status label
        self.status_label = ttk.Label(self.status_bar, text="System Ready", 
                                    relief=SUNKEN, anchor=W, 
                                    font=('Segoe UI', 10), 
                                    background='#e9ecef', 
                                    foreground='#495057')
        self.status_label.pack(fill=X, ipady=3)
        
        # System info
        self.system_info = ttk.Label(self.status_bar, 
                                   text=f"Users: 0 | Attendance: 0 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                   relief=SUNKEN, anchor=E, 
                                   font=('Segoe UI', 10), 
                                   background='#e9ecef', 
                                   foreground='#495057')
        self.system_info.pack(fill=X, ipady=3)

    def load_initial_data(self):
        """Load initial data including attendance and face encodings"""
        self.load_attendance_data()
        self.load_face_encodings()
        self.update_statistics()
        self.update_system_info()

    def load_attendance_data(self):
        """Load attendance data from file"""
        try:
            if os.path.exists("attendance_log.csv"):
                self.attendance_df = pd.read_csv("attendance_log.csv")
                self.update_attendance_tree()
                self.status_label.config(text="Attendance data loaded successfully")
            else:
                self.status_label.config(text="No attendance data found - new file will be created")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load attendance data: {str(e)}")
            self.status_label.config(text="Error loading attendance data")

    def load_face_encodings(self):
        """Load pre-computed face encodings if available"""
        try:
            if os.path.exists("face_encodings.dat"):
                with open("face_encodings.dat", "rb") as f:
                    data = pickle.load(f)
                    self.known_face_encodings = data['encodings']
                    self.known_face_ids = data['ids']
                self.status_label.config(text=f"Loaded {len(self.known_face_ids)} face encodings")
            else:
                self.status_label.config(text="No face encodings found - will use classifier.xml")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load face encodings: {str(e)}")
            self.status_label.config(text="Error loading face encodings")

    def update_attendance_tree(self):
        """Update the attendance treeview with current data"""
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
            
        if not self.attendance_df.empty:
            for _, row in self.attendance_df.iterrows():
                self.attendance_tree.insert("", END, values=(
                    row['ID'], row['Name'], row['Department'], 
                    row['Date'], row['Time'], row['Status'], 
                    f"{row.get('Confidence', 'N/A')}%"
                ))

    def update_statistics(self):
        """Update the statistics display"""
        self.stats_text.delete(1.0, END)
        
        if not self.attendance_df.empty:
            # Basic statistics
            total = len(self.attendance_df)
            unique = self.attendance_df['ID'].nunique()
            today = datetime.now().strftime("%Y-%m-%d")
            present_today = self.attendance_df[self.attendance_df['Date'] == today]['ID'].nunique()
            
            # Department statistics
            dept_stats = self.attendance_df['Department'].value_counts().to_string()
            
            # Time-based statistics
            earliest = self.attendance_df['Time'].min()
            latest = self.attendance_df['Time'].max()
            
            # Confidence statistics
            if 'Confidence' in self.attendance_df.columns:
                avg_conf = self.attendance_df['Confidence'].mean()
                min_conf = self.attendance_df['Confidence'].min()
                max_conf = self.attendance_df['Confidence'].max()
                conf_stats = f"\nAverage Confidence: {avg_conf:.1f}%\nMin: {min_conf}% | Max: {max_conf}%"
            else:
                conf_stats = "\nConfidence data not available"
            
            stats = f"""Attendance Statistics
{'-'*40}
Total records: {total:,}
Unique individuals: {unique:,}
Present today: {present_today:,}

First record: {earliest}
Last record: {latest}
{conf_stats}

By Department:
{dept_stats}
"""
            self.stats_text.insert(END, stats)
        else:
            self.stats_text.insert(END, "No attendance data available yet.")
            
        self.stats_text.config(state=DISABLED)

    def update_system_info(self):
        """Update the system information in the status bar"""
        unique_users = 0
        total_attendance = 0
        
        if not self.attendance_df.empty:
            unique_users = self.attendance_df['ID'].nunique()
            total_attendance = len(self.attendance_df)
            
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.system_info.config(text=f"Users: {unique_users:,} | Attendance: {total_attendance:,} | {timestamp}")
        self.root.after(1000, self.update_system_info)  # Update every second

    def update_threshold(self, val):
        """Update the confidence threshold"""
        self.confidence_threshold = int(float(val))
        self.threshold_label.config(text=f"{self.confidence_threshold}%")
        self.status_label.config(text=f"Confidence threshold set to {self.confidence_threshold}%")

    def on_camera_select(self, event):
        """Handle camera selection change"""
        selection = self.camera_var.get()
        if "Default Camera" in selection:
            self.camera_index = 0
        elif "Secondary Camera" in selection:
            self.camera_index = 1
        elif "Tertiary Camera" in selection:
            self.camera_index = 2
            
        self.status_label.config(text=f"Camera source changed to {selection}.")
        
        if self.recognition_active:
            self.toggle_recognition()  # Restart with new camera

    def check_liveness(self, frame):
        """Basic liveness detection using eye blink analysis"""
        if not self.liveness_var.get():
            return True  # Liveness detection is disabled

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        eye_cascade = cv2.CascadeClassifier(HAARCASCADES_PATH + 'haarcascade_eye.xml')
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

        # More advanced check: look for blinking patterns
        if len(eyes) >= 2:
            # Additional checks could be added here
            return True
        return False

    def detect_faces(self, frame):
        """Detect faces using the selected method"""
        if self.face_detection_method == 'haar':
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(HAARCASCADES_PATH + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)
            return [(x, y, x+w, y+h) for (x, y, w, h) in faces]
        elif self.face_detection_method == 'dlib':
            # Convert to RGB for dlib
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = fr.face_locations(rgb, model="hog")
            return face_locations
        elif self.face_detection_method == 'cnn':
            # More accurate but slower CNN model
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = fr.face_locations(rgb, model="cnn")
            return face_locations
        return []

    def recognize_face(self, face_image):
        """Recognize face using the selected method"""
        if self.face_detection_method in ['dlib', 'cnn'] and self.known_face_encodings:
            # Use face_recognition library if encodings are available
            rgb = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)
            face_encoding = fr.face_encodings(rgb)
            
            if face_encoding:
                matches = fr.compare_faces(self.known_face_encodings, face_encoding[0], tolerance=0.5)
                face_distances = fr.face_distance(self.known_face_encodings, face_encoding[0])
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    confidence = (1 - face_distances[best_match_index]) * 100
                    return self.known_face_ids[best_match_index], confidence
        else:
            # Fall back to LBPH recognizer
            gray = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)
            try:
                id, confidence = self.face_recognizer.predict(gray)
                return id, confidence
            except:
                pass
                
        return None, 0

    def draw_face_info(self, frame, face_location, student_info=None, confidence=0, is_spoof=False):
        """Draw face bounding box and information on the frame"""
        if self.face_detection_method == 'haar':
            x, y, w, h = face_location
            top, right, bottom, left = y, x+w, y+h, x
        else:
            top, right, bottom, left = face_location
            
        # Draw rectangle around face
        color = (0, 255, 0)  # Green for recognized
        if is_spoof:
            color = (0, 0, 255)  # Red for spoof
        elif student_info is None:
            color = (0, 165, 255)  # Orange for unknown
            
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        
        # Draw info box
        if student_info:
            student_id, name, department = student_info
            
            # Create background for text
            cv2.rectangle(frame, (left, bottom - 90), (right, bottom), color, cv2.FILLED)
            
            # Draw text
            cv2.putText(frame, f"ID: {student_id}", (left + 6, bottom - 75), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Name: {name}", (left + 6, bottom - 55), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Dept: {department}", (left + 6, bottom - 35), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            cv2.putText(frame, f"Conf: {confidence:.1f}%", (left + 6, bottom - 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        else:
            cv2.putText(frame, "Unknown", (left + 6, bottom - 6), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
        return frame

    def mark_attendance(self, student_id, name, department, confidence):
        """Mark attendance for a recognized student"""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        time_str = now.strftime("%H:%M:%S")
        
        # Prevent marking attendance too frequently for the same person
        if student_id in self.last_marked_time:
            last_time = self.last_marked_time[student_id]
            if (now - last_time) < timedelta(minutes=1):
                return False  # Already marked very recently
        
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
                "Status": "Present",
                "Confidence": confidence
            }
            
            self.attendance_df = pd.concat([self.attendance_df, pd.DataFrame([new_entry])], ignore_index=True)
            self.update_attendance_tree()
            self.update_statistics()
            
            self.status_label.config(text=f"Attendance marked for {name} ({student_id}) at {time_str}")
            self.last_marked_time[student_id] = now
            self.save_attendance_data()
            
            # Show notification
            self.show_notification(f"Attendance marked for {name}")
            return True
        else:
            self.status_label.config(text=f"{name} ({student_id}) already marked present today.")
            return False

    def show_notification(self, message):
        """Show a notification popup"""
        notification = Toplevel(self.root)
        notification.title("Notification")
        notification.geometry("300x100+{}+{}".format(
            self.root.winfo_x() + self.root.winfo_width() - 320,
            self.root.winfo_y() + self.root.winfo_height() - 120
        ))
        notification.attributes('-topmost', True)
        notification.after(3000, notification.destroy)  # Auto-close after 3 seconds
        
        ttk.Label(notification, text=message, font=('Segoe UI', 11)).pack(pady=20)
        ttk.Button(notification, text="OK", command=notification.destroy).pack(pady=5)

    def save_attendance_data(self):
        """Save attendance data to file"""
        try:
            self.attendance_df.to_csv("attendance_log.csv", index=False)
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save attendance data: {str(e)}")

    def start_auto_save(self):
        """Start the auto-save thread"""
        self.auto_save_running = True
        self.auto_save_thread = Thread(target=self.auto_save_loop, daemon=True)
        self.auto_save_thread.start()

    def auto_save_loop(self):
        """Auto-save loop that runs in a separate thread"""
        while self.auto_save_running:
            time.sleep(self.system_settings['auto_save_interval'] * 60)
            if self.recognition_active:
                self.save_attendance_data()
                self.status_label.config(text=f"Auto-saved attendance data at {datetime.now().strftime('%H:%M:%S')}")

    def toggle_recognition(self):
        """Toggle face recognition on/off"""
        if not self.recognition_active:
            # Initialize face recognizer
            if not os.path.exists("classifier.xml"):
                messagebox.showerror("Error", "Classifier file (classifier.xml) not found. Please train the model first.")
                self.status_label.config(text="Error: Classifier file missing.")
                return
                
            self.face_recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.face_recognizer.read("classifier.xml")
            
            # Set face detection method
            self.face_detection_method = self.detection_method.get()
            
            self.recognition_active = True
            self.recognition_btn.config(text="⏹ Stop Recognition")
            self.status_label.config(text="Face recognition started...")
            
            # Start recognition thread
            Thread(target=self.face_recognition_thread, daemon=True).start()
        else:
            self.recognition_active = False
            self.recognition_btn.config(text="▶ Start Recognition")
            self.status_label.config(text="Face recognition stopped")
            
            if self.capture is not None:
                self.capture.release()
                self.capture = None

    def face_recognition_thread(self):
        """Thread for face recognition"""
        try:
            self.capture = cv2.VideoCapture(self.camera_index)
            if not self.capture.isOpened():
                messagebox.showerror("Camera Error", 
                                   f"Could not open camera with index {self.camera_index}.")
                self.recognition_active = False
                self.recognition_btn.config(text="▶ Start Recognition")
                self.status_label.config(text="Camera access failed.")
                return
                
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            
            while self.recognition_active:
                ret, frame = self.capture.read()
                if not ret:
                    self.status_label.config(text="Error: Could not read frame from camera.")
                    time.sleep(1)
                    continue
                    
                # Detect faces
                face_locations = self.detect_faces(frame)
                
                for face_location in face_locations:
                    # Extract face ROI
                    if self.face_detection_method == 'haar':
                        x, y, w, h = face_location
                        face_roi = frame[y:y+h, x:x+w]
                    else:
                        top, right, bottom, left = face_location
                        face_roi = frame[top:bottom, left:right]
                    
                    # Check liveness if enabled
                    is_spoof = False
                    if self.liveness_var.get() and not self.check_liveness(face_roi):
                        is_spoof = True
                        self.draw_face_info(frame, face_location, is_spoof=True)
                        continue
                        
                    # Recognize face
                    student_id, confidence = self.recognize_face(face_roi)
                    
                    if student_id and confidence >= self.confidence_threshold:
                        # Get student info from database
                        student_info = self.get_student_info(student_id)
                        if student_info:
                            # Draw face info
                            self.draw_face_info(frame, face_location, student_info, confidence)
                            
                            # Mark attendance
                            self.mark_attendance(student_id, *student_info, confidence)
                    else:
                        # Unknown face or low confidence
                        self.draw_face_info(frame, face_location)
                
                # Display frame
                self.update_camera_view(frame)
                
                # Small delay to prevent freezing
                time.sleep(0.03)
                
        except Exception as e:
            messagebox.showerror("Recognition Error", f"An error occurred: {str(e)}")
            self.recognition_active = False
            self.recognition_btn.config(text="▶ Start Recognition")
            self.status_label.config(text=f"Recognition failed: {str(e)}")
            
        finally:
            if self.capture is not None:
                self.capture.release()
                self.capture = None

    def get_student_info(self, student_id):
        """Get student info from database"""
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="B@b@2208",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            cursor.execute("SELECT Student_id, Name, Department FROM student WHERE Student_id=%s", (student_id,))
            result = cursor.fetchone()
            
            if result:
                return result
            return None
                
        except mysql.connector.Error as err:
            self.status_label.config(text=f"Database error: {err}")
            return None
            
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def update_camera_view(self, frame):
        """Update the camera view in the UI"""
        # Convert to PIL Image
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(img)
        
        # Maintain aspect ratio
        img.thumbnail((650, 500), Image.LANCZOS)
        
        # Convert to PhotoImage
        self.current_frame = img
        self.photo_camera = ImageTk.PhotoImage(img)
        
        # Update label
        self.camera_label.config(image=self.photo_camera)
        self.camera_label.image = self.photo_camera

    def capture_photo(self):
        """Capture the current frame and save it"""
        if self.current_frame is None:
            messagebox.showwarning("No Image", "No image available to capture.")
            return
            
        filename = f"capture_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        self.current_frame.save(filename)
        self.status_label.config(text=f"Image saved as {filename}")
        self.show_notification(f"Image saved as {filename}")

    def generate_report(self):
        """Generate attendance report for selected date range"""
        report_window = Toplevel(self.root)
        report_window.title("Attendance Report")
        report_window.geometry("1000x700")
        report_window.resizable(True, True)
        report_window.transient(self.root)
        report_window.grab_set()
        
        # Style the report window
        report_window.configure(bg="#f5f5f5")
        
        # Title
        ttk.Label(report_window, text="Attendance Report Generator",
                 font=("Segoe UI", 18, "bold"), background="#f5f5f5", 
                 foreground='#2c3e50').pack(pady=15)
        
        # Date range selection
        date_frame = ttk.Frame(report_window, style='TFrame')
        date_frame.pack(fill=X, padx=20, pady=10)
        
        ttk.Label(date_frame, text="From Date:", background="#f5f5f5").pack(side=LEFT, padx=5)
        self.from_date = DateEntry(date_frame, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, 
                                 date_pattern='yyyy-mm-dd')
        self.from_date.pack(side=LEFT, padx=5)
        
        ttk.Label(date_frame, text="To Date:", background="#f5f5f5").pack(side=LEFT, padx=5)
        self.to_date = DateEntry(date_frame, width=12, background='darkblue',
                               foreground='white', borderwidth=2, 
                               date_pattern='yyyy-mm-dd')
        self.to_date.pack(side=LEFT, padx=5)
        
        # Filter options
        filter_frame = ttk.Frame(report_window, style='TFrame')
        filter_frame.pack(fill=X, padx=20, pady=5)
        
        ttk.Label(filter_frame, text="Filter by:", background="#f5f5f5").pack(side=LEFT, padx=5)
        
        self.filter_department = StringVar()
        dept_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_department,
                                    values=self.get_departments(), width=15)
        dept_dropdown.pack(side=LEFT, padx=5)
        dept_dropdown.set("All Departments")
        
        self.filter_status = StringVar()
        status_dropdown = ttk.Combobox(filter_frame, textvariable=self.filter_status,
                                      values=["All Statuses", "Present", "Absent"], width=12)
        status_dropdown.pack(side=LEFT, padx=5)
        status_dropdown.set("All Statuses")
        
        # Buttons
        btn_frame = ttk.Frame(report_window, style='TFrame')
        btn_frame.pack(fill=X, padx=20, pady=10)
        
        ttk.Button(btn_frame, text="Generate Report",
                 command=lambda: self._generate_report_data(report_display_frame),
                 style='Primary.TButton').pack(side=LEFT, padx=5)
        
        ttk.Button(btn_frame, text="Print Report",
                 command=self.print_report,
                 style='Secondary.TButton').pack(side=LEFT, padx=5)
        
        # Report display area
        report_display_frame = ttk.Frame(report_window, style='TFrame')
        report_display_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        # Treeview for report
        self.report_tree = ttk.Treeview(report_display_frame, 
                                      columns=("ID", "Name", "Department", "Date", "Time", "Status", "Confidence"), 
                                      show="headings", style='Treeview')
        
        # Configure columns
        columns = [
            ("ID", 80, "center"),
            ("Name", 150, "w"),
            ("Department", 120, "w"),
            ("Date", 100, "center"),
            ("Time", 80, "center"),
            ("Status", 80, "center"),
            ("Confidence", 90,"center")
        ]
        
        for col, width, anchor in columns:
            self.report_tree.heading(col, text=col)
            self.report_tree.column(col, width=width, anchor=anchor)
        
        # Scrollbars
        scroll_y = ttk.Scrollbar(report_display_frame, orient=VERTICAL, 
                               command=self.report_tree.yview)
        scroll_x = ttk.Scrollbar(report_display_frame, orient=HORIZONTAL, 
                               command=self.report_tree.xview)
        self.report_tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)
        
        # Grid layout
        self.report_tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        report_display_frame.grid_rowconfigure(0, weight=1)
        report_display_frame.grid_columnconfigure(0, weight=1)
        
        # Summary label
        self.report_summary = ttk.Label(report_window, text="", 
                                      font=('Segoe UI', 10), 
                                      background="#f5f5f5")
        self.report_summary.pack(side=BOTTOM, fill=X, padx=20, pady=10)

    def _generate_report_data(self, report_display_frame):
        """Generate the report data based on filters"""
        # Clear existing entries
        for item in self.report_tree.get_children():
            self.report_tree.delete(item)
            
        try:
            from_dt = self.from_date.get_date()
            to_dt = self.to_date.get_date()
        except ValueError:
            messagebox.showerror("Date Error", "Invalid date format. Please use YYYY-MM-DD.")
            return
            
        # Apply date filter
        filtered_df = self.attendance_df[
            (self.attendance_df['Date'] >= from_dt.strftime("%Y-%m-%d")) & 
            (self.attendance_df['Date'] <= to_dt.strftime("%Y-%m-%d"))
        ]
        
        # Apply department filter
        if self.filter_department.get() != "All Departments":
            filtered_df = filtered_df[filtered_df['Department'] == self.filter_department.get()]
            
        # Apply status filter
        if self.filter_status.get() != "All Statuses":
            filtered_df = filtered_df[filtered_df['Status'] == self.filter_status.get()]
            
        if filtered_df.empty:
            messagebox.showinfo("Report", "No attendance records found for the selected filters.")
            self.report_summary.config(text="No records found for the selected filters.")
            return
            
        # Populate treeview
        for _, row in filtered_df.iterrows():
            self.report_tree.insert("", END, values=(
                row['ID'], row['Name'], row['Department'], 
                row['Date'], row['Time'], row['Status'], 
                f"{row.get('Confidence', 'N/A')}%"
            ))
            
        # Update summary
        unique_users = filtered_df['ID'].nunique()
        total_records = len(filtered_df)
        date_range = f"{from_dt.strftime('%Y-%m-%d')} to {to_dt.strftime('%Y-%m-%d')}"
        
        summary_text = f"Report Summary: {total_records} records for {unique_users} unique users from {date_range}"
        if self.filter_department.get() != "All Departments":
            summary_text += f" | Department: {self.filter_department.get()}"
        if self.filter_status.get() != "All Statuses":
            summary_text += f" | Status: {self.filter_status.get()}"
            
        self.report_summary.config(text=summary_text)
        self.filtered_report_df = filtered_df  # Store for export/print

    def get_departments(self):
        """Get list of unique departments from attendance data"""
        if not self.attendance_df.empty:
            depts = ["All Departments"] + sorted(self.attendance_df['Department'].unique().tolist())
            return depts
        return ["All Departments"]

    def print_report(self):
        """Print the current report"""
        if not hasattr(self, 'filtered_report_df') or self.filtered_report_df.empty:
            messagebox.showwarning("No Data", "No report data to print.")
            return
            
        # Create a simple printable version
        printable = self.filtered_report_df.to_string(index=False)
        
        # Create a print window
        print_window = Toplevel(self.root)
        print_window.title("Print Preview")
        print_window.geometry("800x600")
        
        text = Text(print_window, wrap=WORD, font=('Courier New', 10))
        text.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        text.insert(END, "Attendance Report\n")
        text.insert(END, "="*50 + "\n\n")
        text.insert(END, printable)
        
        # Add print button
        ttk.Button(print_window, text="Print", 
                 command=lambda: self._print_text(text),
                 style='Primary.TButton').pack(pady=10)

    def _print_text(self, text_widget):
        """Print the text widget content"""
        # This is a placeholder - actual printing would need more implementation
        messagebox.showinfo("Print", "Printing would be implemented here.")

    def export_to_excel(self):
        """Export attendance data to Excel"""
        if self.attendance_df.empty:
            messagebox.showinfo("Export Data", "No attendance data to export.")
            return
            
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                               filetypes=[("Excel files", "*.xlsx"), 
                                                         ("CSV files", "*.csv"), 
                                                         ("All files", "*.*")],
                                               title="Save Attendance Data")
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    self.attendance_df.to_csv(file_path, index=False)
                else:
                    self.attendance_df.to_excel(file_path, index=False)
                    
                messagebox.showinfo("Export Successful", 
                                  f"Attendance data exported to:\n{file_path}")
                self.status_label.config(text=f"Data exported to {os.path.basename(file_path)}")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export data: {str(e)}")

    def email_report(self):
        """Email the attendance report"""
        if not hasattr(self, 'filtered_report_df') or self.filtered_report_df.empty:
            messagebox.showwarning("No Data", "No report data to email. Generate a report first.")
            return
            
        email_window = Toplevel(self.root)
        email_window.title("Email Report")
        email_window.geometry("500x400")
        
        ttk.Label(email_window, text="Email Recipient:", 
                font=('Segoe UI', 11)).pack(pady=(10, 0))
        
        self.recipient_email = ttk.Entry(email_window, font=('Segoe UI', 11))
        self.recipient_email.pack(fill=X, padx=20, pady=5)
        
        ttk.Label(email_window, text="Subject:", 
                font=('Segoe UI', 11)).pack(pady=(10, 0))
        
        self.email_subject = ttk.Entry(email_window, font=('Segoe UI', 11))
        self.email_subject.pack(fill=X, padx=20, pady=5)
        self.email_subject.insert(0, "Attendance Report")
        
        ttk.Label(email_window, text="Message:", 
                font=('Segoe UI', 11)).pack(pady=(10, 0))
        
        self.email_message = Text(email_window, wrap=WORD, font=('Segoe UI', 11), 
                                height=8)
        self.email_message.pack(fill=BOTH, expand=True, padx=20, pady=5)
        self.email_message.insert(END, "Please find attached the attendance report.\n\nRegards,\nAttendance System")
        
        btn_frame = ttk.Frame(email_window, style='TFrame')
        btn_frame.pack(fill=X, padx=20, pady=10)
        
        ttk.Button(btn_frame, text="Send Email", 
                 command=self._send_email,
                 style='Primary.TButton').pack(side=LEFT, expand=True)
        
        ttk.Button(btn_frame, text="Cancel", 
                 command=email_window.destroy,
                 style='Secondary.TButton').pack(side=LEFT, expand=True, padx=10)

    def _send_email(self):
        """Send the email with attachment"""
        recipient = self.recipient_email.get()
        subject = self.email_subject.get()
        message = self.email_message.get("1.0", END)
        
        if not recipient or '@' not in recipient:
            messagebox.showerror("Invalid Email", "Please enter a valid email address.")
            return
            
        try:
            # Create a temporary file for the report
            temp_file = "temp_report.xlsx"
            self.filtered_report_df.to_excel(temp_file, index=False)
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.email_settings['sender']
            msg['To'] = recipient
            msg['Subject'] = subject
            
            # Add message body
            msg.attach(MIMEText(message, 'plain'))
            
            # Attach file
            with open(temp_file, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', 
                               f"attachment; filename=attendance_report.xlsx")
                msg.attach(part)
            
            # Connect to server and send
            server = smtplib.SMTP(self.email_settings['smtp_server'], 
                                 self.email_settings['smtp_port'])
            server.starttls()
            server.login(self.email_settings['sender'], 
                        self.email_settings['password'])
            server.send_message(msg)
            server.quit()
            
            # Clean up
            os.remove(temp_file)
            
            messagebox.showinfo("Success", "Email sent successfully!")
            self.recipient_email.winfo_toplevel().destroy()
            
        except Exception as e:
            messagebox.showerror("Email Error", f"Failed to send email: {str(e)}")

    def plot_attendance_charts(self):
        """Plot attendance charts"""
        # Clear previous charts
        for widget in self.chart_canvas_frame.winfo_children():
            widget.destroy()
            
        if self.attendance_df.empty:
            ttk.Label(self.chart_canvas_frame, text="No data available to generate charts.", 
                     style='TLabel').pack(pady=20)
            return
            
        # Create figure with 2 subplots
        fig = Figure(figsize=(10, 8), dpi=100, facecolor='#f0f2f5')
        
        # Chart 1: Attendance by Department (Pie)
        ax1 = fig.add_subplot(211)
        dept_counts = self.attendance_df['Department'].value_counts()
        if not dept_counts.empty:
            colors = plt.cm.Paired(np.linspace(0, 1, len(dept_counts)))
            ax1.pie(dept_counts, labels=dept_counts.index, autopct='%1.1f%%',
                   startangle=90, colors=colors, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
            ax1.set_title('Attendance by Department', fontsize=12, pad=20)
            ax1.axis('equal')
        else:
            ax1.text(0.5, 0.5, "No Department Data", ha='center', va='center')
            ax1.set_title('Attendance by Department', fontsize=12)
            ax1.axis('off')
        
        # Chart 2: Daily Attendance Trend (Bar)
        ax2 = fig.add_subplot(212)
        self.attendance_df['Date'] = pd.to_datetime(self.attendance_df['Date'])
        daily_counts = self.attendance_df.groupby(self.attendance_df['Date'].dt.date).nunique()['ID'].tail(14)
        
        if not daily_counts.empty:
            dates = [str(d) for d in daily_counts.index]
            bars = ax2.bar(dates, daily_counts.values, color='#4a6baf')
            
            # Add value labels on bars
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                         f'{int(height)}', ha='center', va='bottom')
                
            ax2.set_title('Daily Unique Attendees (Last 14 Days)', fontsize=12, pad=20)
            ax2.set_xlabel('Date')
            ax2.set_ylabel('Number of Attendees')
            ax2.tick_params(axis='x', rotation=45)
            ax2.grid(axis='y', linestyle='--', alpha=0.7)
            
            # Adjust layout to prevent label cutoff
            fig.tight_layout(pad=3.0)
        else:
            ax2.text(0.5, 0.5, "No Daily Attendance Data", ha='center', va='center')
            ax2.set_title('Daily Unique Attendees', fontsize=12)
            ax2.axis('off')
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.chart_canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=BOTH, expand=True)

    def view_all_students(self):
        """View all students in the database"""
        students_window = Toplevel(self.root)
        students_window.title("All Students")
        students_window.geometry("800x600")
        
        # Create treeview
        tree = ttk.Treeview(students_window, columns=("ID", "Name", "Department", "Email"), 
                           show="headings", style='Treeview')
        
        # Configure columns
        columns = [
            ("ID", 80, CENTER),
            ("Name", 200, LEFT),
            ("Department", 150, LEFT),
            ("Email", 250, LEFT)
        ]
        
        for col, width, anchor in columns:
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor=anchor)
        
        # Add scrollbars
        scroll_y = ttk.Scrollbar(students_window, orient=VERTICAL, command=tree.yview)
        scroll_x = ttk.Scrollbar(students_window, orient=HORIZONTAL, command=tree.xview)
        tree.configure(yscroll=scroll_y.set, xscroll=scroll_x.set)
        
        # Grid layout
        tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        # Configure grid weights
        students_window.grid_rowconfigure(0, weight=1)
        students_window.grid_columnconfigure(0, weight=1)
        
        # Load data
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="B@b@2208",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            cursor.execute("SELECT Student_id, Name, Department, Email FROM student")
            results = cursor.fetchall()
            
            for row in results:
                tree.insert("", END, values=row)
                
            ttk.Label(students_window, text=f"Total Students: {len(results)}", 
                     style='TLabel').grid(row=2, column=0, sticky=W, padx=10, pady=5)
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching students: {err}")
            
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def add_new_student(self):
        """Add a new student to the database"""
        add_window = Toplevel(self.root)
        add_window.title("Add New Student")
        add_window.geometry("500x400")
        
        # Form fields
        fields = [
            ("Student ID:", "id"),
            ("Name:", "name"),
            ("Department:", "dept"),
            ("Email:", "email"),
            ("Phone:", "phone")
        ]
        
        entries = {}
        
        for i, (label, key) in enumerate(fields):
            ttk.Label(add_window, text=label).grid(row=i, column=0, padx=10, pady=5, sticky=W)
            entry = ttk.Entry(add_window)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky=EW)
            entries[key] = entry
        
        # Add photo button
        ttk.Button(add_window, text="Add Photo", 
                 command=lambda: self.capture_student_photo(entries['id'].get()),
                 style='Secondary.TButton').grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # Submit button
        ttk.Button(add_window, text="Save Student", 
                 command=lambda: self._save_new_student(entries, add_window),
                 style='Primary.TButton').grid(row=len(fields)+1, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        add_window.grid_columnconfigure(1, weight=1)

    def _save_new_student(self, entries, window):
        """Save the new student to database"""
        student_id = entries['id'].get()
        name = entries['name'].get()
        dept = entries['dept'].get()
        email = entries['email'].get()
        phone = entries['phone'].get()
        
        if not student_id or not name:
            messagebox.showerror("Error", "Student ID and Name are required!")
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="B@b@2208",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            # Check if student already exists
            cursor.execute("SELECT * FROM student WHERE Student_id=%s", (student_id,))
            if cursor.fetchone():
                messagebox.showerror("Error", "Student ID already exists!")
                return
                
            # Insert new student
            cursor.execute(
                "INSERT INTO student (Student_id, Name, Department, Email, Phone) VALUES (%s, %s, %s, %s, %s)",
                (student_id, name, dept, email, phone)
            )
            conn.commit()
            
            messagebox.showinfo("Success", "Student added successfully!")
            window.destroy()
            
            # Rebuild face encodings if photo exists
            photo_path = f"data/user.{student_id}.1.jpg"
            if os.path.exists(photo_path):
                self.rebuild_face_encodings()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error saving student: {err}")
            
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def capture_student_photo(self, student_id):
        """Capture photo for a new student"""
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID first!")
            return
            
        # Create directory if not exists
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Open camera for photo capture
        cap = cv2.VideoCapture(0)
        
        def capture_and_save():
            ret, frame = cap.read()
            if ret:
                # Save the image
                img_path = f"data/user.{student_id}.1.jpg"
                cv2.imwrite(img_path, frame)
                messagebox.showinfo("Success", f"Photo saved as {img_path}")
                cap.release()
                cv2.destroyAllWindows()
                photo_window.destroy()
                
                # Rebuild face encodings
                self.rebuild_face_encodings()
        
        photo_window = Toplevel(self.root)
        photo_window.title("Capture Photo")
        
        # Video frame
        video_frame = ttk.Frame(photo_window)
        video_frame.pack(padx=10, pady=10)
        
        # Capture button
        ttk.Button(photo_window, text="Capture Photo", 
                 command=capture_and_save,
                 style='Primary.TButton').pack(pady=10)
        
        # Show video feed
        def show_frame():
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                img = ImageTk.PhotoImage(image=img)
                
                if hasattr(show_frame, 'panel'):
                    show_frame.panel.configure(image=img)
                    show_frame.panel.image = img
                else:
                    show_frame.panel = ttk.Label(video_frame, image=img)
                    show_frame.panel.image = img
                    show_frame.panel.pack()
                
            photo_window.after(10, show_frame)
        
        show_frame()

    def edit_student(self):
        """Edit an existing student"""
        edit_window = Toplevel(self.root)
        edit_window.title("Edit Student")
        edit_window.geometry("500x400")
        
        # Student ID entry
        ttk.Label(edit_window, text="Student ID:").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        id_entry = ttk.Entry(edit_window)
        id_entry.grid(row=0, column=1, padx=10, pady=5, sticky=EW)
        
        # Search button
        ttk.Button(edit_window, text="Search", 
                 command=lambda: self._search_student(id_entry.get(), edit_window),
                 style='Secondary.TButton').grid(row=0, column=2, padx=10, pady=5)
        
        # Form fields (will be populated after search)
        fields = [
            ("Name:", "name"),
            ("Department:", "dept"),
            ("Email:", "email"),
            ("Phone:", "phone")
        ]
        
        self.edit_entries = {}
        
        for i, (label, key) in enumerate(fields):
            ttk.Label(edit_window, text=label).grid(row=i+1, column=0, padx=10, pady=5, sticky=W)
            entry = ttk.Entry(edit_window)
            entry.grid(row=i+1, column=1, padx=10, pady=5, sticky=EW, columnspan=2)
            self.edit_entries[key] = entry
        
        # Update photo button
        ttk.Button(edit_window, text="Update Photo", 
                 command=lambda: self.capture_student_photo(id_entry.get()),
                 style='Secondary.TButton').grid(row=len(fields)+1, column=0, columnspan=3, pady=10)
        
        # Save button
        ttk.Button(edit_window, text="Save Changes", 
                 command=lambda: self._save_edited_student(id_entry.get(), edit_window),
                 style='Primary.TButton').grid(row=len(fields)+2, column=0, columnspan=3, pady=10)
        
        # Configure grid weights
        edit_window.grid_columnconfigure(1, weight=1)

    def _search_student(self, student_id, window):
        """Search for student to edit"""
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID!")
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="B@b@2208",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            cursor.execute("SELECT Name, Department, Email, Phone FROM student WHERE Student_id=%s", (student_id,))
            result = cursor.fetchone()
            
            if result:
                # Populate fields
                self.edit_entries['name'].delete(0, END)
                self.edit_entries['name'].insert(0, result[0])
                
                self.edit_entries['dept'].delete(0, END)
                self.edit_entries['dept'].insert(0, result[1])
                
                self.edit_entries['email'].delete(0, END)
                self.edit_entries['email'].insert(0, result[2])
                
                self.edit_entries['phone'].delete(0, END)
                self.edit_entries['phone'].insert(0, result[3])
            else:
                messagebox.showerror("Error", "Student not found!")
                
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error searching student: {err}")
            
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def _save_edited_student(self, student_id, window):
        """Save edited student information"""
        name = self.edit_entries['name'].get()
        dept = self.edit_entries['dept'].get()
        email = self.edit_entries['email'].get()
        phone = self.edit_entries['phone'].get()
        
        if not student_id or not name:
            messagebox.showerror("Error", "Student ID and Name are required!")
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="B@b@2208",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            # Update student
            cursor.execute(
                "UPDATE student SET Name=%s, Department=%s, Email=%s, Phone=%s WHERE Student_id=%s",
                (name, dept, email, phone, student_id)
            )
            conn.commit()
            
            messagebox.showinfo("Success", "Student updated successfully!")
            window.destroy()
            
            # Rebuild face encodings if they exist
            if student_id in self.known_face_ids:
                self.rebuild_face_encodings()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error updating student: {err}")
            
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def delete_student(self):
        """Delete a student from the database"""
        delete_window = Toplevel(self.root)
        delete_window.title("Delete Student")
        delete_window.geometry("400x200")
        
        # Student ID entry
        ttk.Label(delete_window, text="Student ID:").pack(pady=(20, 5))
        
        self.delete_id_entry = ttk.Entry(delete_window)
        self.delete_id_entry.pack(pady=5, padx=20, fill=X)
        
        # Buttons
        btn_frame = ttk.Frame(delete_window, style='TFrame')
        btn_frame.pack(fill=X, padx=20, pady=20)
        
        ttk.Button(btn_frame, text="Delete", 
                 command=self._confirm_delete_student,
                 style='Danger.TButton').pack(side=LEFT, expand=True)
        
        ttk.Button(btn_frame, text="Cancel", 
                 command=delete_window.destroy,
                 style='Secondary.TButton').pack(side=LEFT, expand=True, padx=10)

    def _confirm_delete_student(self):
        """Confirm and delete student"""
        student_id = self.delete_id_entry.get()
        if not student_id:
            messagebox.showerror("Error", "Please enter Student ID!")
            return
            
        if not messagebox.askyesno("Confirm", f"Delete student {student_id}? This cannot be undone!"):
            return
            
        try:
            conn = mysql.connector.connect(
                host="localhost",
                username="root",
                password="B@b@2208",
                database="face_recognizer"
            )
            cursor = conn.cursor()
            
            # Delete student
            cursor.execute("DELETE FROM student WHERE Student_id=%s", (student_id,))
            conn.commit()
            
            # Delete photos if they exist
            photo_path = f"data/user.{student_id}.1.jpg"
            if os.path.exists(photo_path):
                os.remove(photo_path)
                
            messagebox.showinfo("Success", "Student deleted successfully!")
            self.delete_id_entry.winfo_toplevel().destroy()
            
            # Rebuild face encodings if they existed
            if student_id in self.known_face_ids:
                self.rebuild_face_encodings()
            
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error deleting student: {err}")
            
        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    def rebuild_face_encodings(self):
        """Rebuild the face encodings from the dataset"""
        try:
            # Get all image paths
            image_paths = [os.path.join("data", f) for f in os.listdir("data") if f.endswith(".jpg")]
            
            if not image_paths:
                messagebox.showinfo("Info", "No face images found in the data directory.")
                return
                
            self.known_face_encodings = []
            self.known_face_ids = []
            
            for image_path in image_paths:
                # Extract ID from filename (format: user.<id>.<number>.jpg)
                student_id = os.path.split(image_path)[-1].split(".")[1]
                
                # Load image
                image = fr.load_image_file(image_path)
                face_locations = fr.face_locations(image)
                
                if face_locations:  # If at least one face found
                    face_encoding = fr.face_encodings(image, face_locations)[0]
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_ids.append(student_id)
            
            # Save encodings to file
            data = {"encodings": self.known_face_encodings, "ids": self.known_face_ids}
            with open("face_encodings.dat", "wb") as f:
                pickle.dump(data, f)
                
            messagebox.showinfo("Success", f"Rebuilt {len(self.known_face_ids)} face encodings!")
            self.status_label.config(text=f"Face encodings rebuilt for {len(self.known_face_ids)} images")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to rebuild face encodings: {str(e)}")

    def backup_database(self):
        """Backup the database to a file"""
        backup_file = filedialog.asksaveasfilename(defaultextension=".sql",
                                                 filetypes=[("SQL files", "*.sql"), 
                                                           ("All files", "*.*")],
                                                 title="Save Database Backup")
        if backup_file:
            try:
                # This is a simplified backup - in production you'd use mysqldump
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="B@b@2208",
                    database="face_recognizer"
                )
                cursor = conn.cursor()
                
                # Get all tables
                cursor.execute("SHOW TABLES")
                tables = [table[0] for table in cursor.fetchall()]
                
                with open(backup_file, 'w') as f:
                    for table in tables:
                        # Write table structure
                        cursor.execute(f"SHOW CREATE TABLE {table}")
                        create_table = cursor.fetchone()[1]
                        f.write(f"{create_table};\n\n")
                        
                        # Write table data
                        cursor.execute(f"SELECT * FROM {table}")
                        rows = cursor.fetchall()
                        
                        if rows:
                            columns = [desc[0] for desc in cursor.description]
                            f.write(f"INSERT INTO {table} ({', '.join(columns)}) VALUES\n")
                            
                            for i, row in enumerate(rows):
                                values = []
                                for value in row:
                                    if value is None:
                                        values.append("NULL")
                                    elif isinstance(value, (int, float)):
                                        values.append(str(value))
                                    else:
                                        values.append(f"'{str(value).replace("'", "''")}'")
                                
                                f.write(f"({', '.join(values)})")
                                f.write(";\n" if i == len(rows)-1 else ",\n")
                            
                            f.write("\n")
                
                messagebox.showinfo("Success", f"Database backup saved to {backup_file}")
                
            except mysql.connector.Error as err:
                messagebox.showerror("Backup Error", f"Failed to backup database: {err}")
                
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()

    def restore_database(self):
        """Restore database from backup"""
        backup_file = filedialog.askopenfilename(filetypes=[("SQL files", "*.sql"), 
                                                          ("All files", "*.*")],
                                               title="Select Database Backup")
        if backup_file:
            if not messagebox.askyesno("Confirm", "This will overwrite current database. Continue?"):
                return
                
            try:
                # This is a simplified restore - in production you'd use mysql command
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="B@b@2208"
                )
                cursor = conn.cursor()
                
                # Read SQL file
                with open(backup_file, 'r') as f:
                    sql_commands = f.read().split(';')
                
                # Execute commands
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
                
                conn.commit()
                messagebox.showinfo("Success", "Database restored successfully!")
                
                # Rebuild face encodings
                self.rebuild_face_encodings()
                
            except Exception as e:
                messagebox.showerror("Restore Error", f"Failed to restore database: {str(e)}")
                
            finally:
                if 'conn' in locals() and conn.is_connected():
                    cursor.close()
                    conn.close()

    def open_settings(self):
        """Open system settings dialog"""
        settings_window = Toplevel(self.root)
        settings_window.title("System Settings")
        settings_window.geometry("500x400")
        
        # Email settings frame
        email_frame = ttk.LabelFrame(settings_window, text="Email Settings", 
                                   style='TLabelframe')
        email_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(email_frame, text="SMTP Server:").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        smtp_server = ttk.Entry(email_frame)
        smtp_server.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        smtp_server.insert(0, self.email_settings['smtp_server'])
        
        ttk.Label(email_frame, text="Port:").grid(row=1, column=0, padx=5, pady=5, sticky=W)
        smtp_port = ttk.Entry(email_frame)
        smtp_port.grid(row=1, column=1, padx=5, pady=5, sticky=EW)
        smtp_port.insert(0, str(self.email_settings['smtp_port']))
        
        ttk.Label(email_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=W)
        email = ttk.Entry(email_frame)
        email.grid(row=2, column=1, padx=5, pady=5, sticky=EW)
        email.insert(0, self.email_settings['sender'])
        
        ttk.Label(email_frame, text="Password:").grid(row=3, column=0, padx=5, pady=5, sticky=W)
        password = ttk.Entry(email_frame, show="*")
        password.grid(row=3, column=1, padx=5, pady=5, sticky=EW)
        password.insert(0, self.email_settings['password'])
        
        # System settings frame
        sys_frame = ttk.LabelFrame(settings_window, text="System Settings", 
                                 style='TLabelframe')
        sys_frame.pack(fill=X, padx=10, pady=10)
        
        ttk.Label(sys_frame, text="Auto-save Interval (mins):").grid(row=0, column=0, padx=5, pady=5, sticky=W)
        auto_save = ttk.Entry(sys_frame)
        auto_save.grid(row=0, column=1, padx=5, pady=5, sticky=EW)
        auto_save.insert(0, str(self.system_settings['auto_save_interval']))
        
        notify_missing = IntVar(value=self.system_settings['notify_missing'])
        ttk.Checkbutton(sys_frame, text="Notify about missing students", 
                      variable=notify_missing, style='TCheckbutton').grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        
        dark_mode = IntVar(value=self.system_settings['dark_mode'])
        ttk.Checkbutton(sys_frame, text="Dark Mode", 
                      variable=dark_mode, style='TCheckbutton').grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky=W)
        
        # Save button
        ttk.Button(settings_window, text="Save Settings", 
                 command=lambda: self._save_settings(
                     smtp_server.get(),
                     smtp_port.get(),
                     email.get(),
                     password.get(),
                     auto_save.get(),
                     notify_missing.get(),
                     dark_mode.get(),
                     settings_window
                 ),
                 style='Primary.TButton').pack(pady=10)
        
        # Configure grid weights
        email_frame.grid_columnconfigure(1, weight=1)
        sys_frame.grid_columnconfigure(1, weight=1)

    def _save_settings(self, smtp_server, smtp_port, email, password, auto_save, notify_missing, dark_mode, window):
        """Save system settings"""
        try:
            self.email_settings = {
                'smtp_server': smtp_server,
                'smtp_port': int(smtp_port),
                'sender': email,
                'password': password
            }
            
            self.system_settings = {
                'auto_save_interval': int(auto_save),
                'notify_missing': bool(notify_missing),
                'dark_mode': bool(dark_mode)
            }
            
            # Apply dark mode if changed
            if dark_mode:
                self._apply_dark_mode()
            else:
                self._apply_light_mode()
            
            messagebox.showinfo("Success", "Settings saved successfully!")
            window.destroy()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid values for all fields!")
            return

    def _apply_dark_mode(self):
        """Apply dark mode theme"""
        self.root.configure(bg="#2d2d2d")
        self.style.configure('TFrame', background="#2d2d2d")
        self.style.configure('TLabel', background="#2d2d2d", foreground="white")
        self.style.configure('Title.TLabel', background="#2d2d2d", foreground="white")
        self.style.configure('TLabelframe', background="#3d3d3d", foreground="white")
        self.style.configure('TLabelframe.Label', background="#3d3d3d", foreground="white")
        self.style.configure('Treeview', background="#3d3d3d", foreground="white", fieldbackground="#3d3d3d")
        self.style.configure('TNotebook', background="#2d2d2d")
        self.style.configure('TNotebook.Tab', background="#3d3d3d", foreground="white")

    def _apply_light_mode(self):
        """Apply light mode theme"""
        self.root.configure(bg="#f0f2f5")
        self.style.configure('TFrame', background="#f0f2f5")
        self.style.configure('TLabel', background="#f0f2f5", foreground="#333333")
        self.style.configure('Title.TLabel', background="#f0f2f5", foreground="#2c3e50")
        self.style.configure('TLabelframe', background="#ffffff", foreground="#2c3e50")
        self.style.configure('TLabelframe.Label', background="#ffffff", foreground="#2c3e50")
        self.style.configure('Treeview', background="#ffffff", foreground="#333333", fieldbackground="#ffffff")
        self.style.configure('TNotebook', background="#f0f2f5")
        self.style.configure('TNotebook.Tab', background="#e9ecef", foreground="#495057")

    def view_attendance_details(self):
        """View details of a selected attendance entry"""
        selected = self.attendance_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an attendance record first.")
            return
            
        item = self.attendance_tree.item(selected[0])
        values = item['values']
        
        details_window = Toplevel(self.root)
        details_window.title("Attendance Details")
        details_window.geometry("400x300")
        
        # Display details
        ttk.Label(details_window, text="Attendance Details", 
                 style='Title.TLabel').pack(pady=10)
        
        details_frame = ttk.Frame(details_window, style='TFrame')
        details_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)
        
        fields = [
            ("Student ID:", values[0]),
            ("Name:", values[1]),
            ("Department:", values[2]),
            ("Date:", values[3]),
            ("Time:", values[4]),
            ("Status:", values[5]),
            ("Confidence:", values[6])
        ]
        
        for i, (label, value) in enumerate(fields):
            ttk.Label(details_frame, text=label, style='TLabel').grid(row=i, column=0, sticky=W, pady=2)
            ttk.Label(details_frame, text=value, style='TLabel').grid(row=i, column=1, sticky=W, pady=2)
        
        # Close button
        ttk.Button(details_window, text="Close", 
                 command=details_window.destroy,
                 style='Primary.TButton').pack(pady=10)

    def generate_qr_for_entry(self):
        """Generate QR code for a selected attendance entry"""
        selected = self.attendance_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an attendance record first.")
            return
            
        item = self.attendance_tree.item(selected[0])
        values = item['values']
        
        # Create QR code data
        qr_data = f"""Attendance Record:
ID: {values[0]}
Name: {values[1]}
Department: {values[2]}
Date: {values[3]}
Time: {values[4]}
Status: {values[5]}
Confidence: {values[6]}"""
        
        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to Tkinter image
        bio = BytesIO()
        img.save(bio, format="PNG")
        qr_img = Image.open(bio)
        qr_photo = ImageTk.PhotoImage(qr_img)
        
        # Display in new window
        qr_window = Toplevel(self.root)
        qr_window.title("QR Code")
        
        ttk.Label(qr_window, image=qr_photo).pack(padx=10, pady=10)
        ttk.Label(qr_window, text="Attendance Record QR Code", 
                 style='Title.TLabel').pack(pady=5)
        
        # Save reference to prevent garbage collection
        qr_window.qr_photo = qr_photo
        
        # Save button
        ttk.Button(qr_window, text="Save QR Code", 
                 command=lambda: self._save_qr_code(img, qr_window),
                 style='Primary.TButton').pack(pady=10)

    def _save_qr_code(self, qr_img, window):
        """Save the QR code to a file"""
        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                               filetypes=[("PNG files", "*.png"), 
                                                         ("All files", "*.*")],
                                               title="Save QR Code")
        if file_path:
            qr_img.save(file_path)
            messagebox.showinfo("Success", f"QR code saved to {file_path}")
            window.destroy()

    def delete_attendance_entry(self):
        """Delete a selected attendance entry"""
        selected = self.attendance_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select an attendance record first.")
            return
            
        item = self.attendance_tree.item(selected[0])
        values = item['values']
        
        if not messagebox.askyesno("Confirm", f"Delete attendance record for {values[1]} ({values[0]}) on {values[3]}?"):
            return
            
        # Remove from DataFrame
        index = self.attendance_df[
            (self.attendance_df['ID'] == values[0]) & 
            (self.attendance_df['Date'] == values[3]) & 
            (self.attendance_df['Time'] == values[4])
        ].index
        
        if len(index) > 0:
            self.attendance_df.drop(index[0], inplace=True)
            self.save_attendance_data()
            self.update_attendance_tree()
            self.update_statistics()
            messagebox.showinfo("Success", "Attendance record deleted.")
        else:
            messagebox.showerror("Error", "Record not found in data.")

    def on_tab_change(self, event):
        """Handle tab change event"""
        selected_tab = self.notebook.tab(self.notebook.select(), "text")
        if selected_tab == "Charts":
            self.plot_attendance_charts()
        elif selected_tab == "Statistics":
            self.update_statistics()
        elif selected_tab == "Attendance":
            self.update_attendance_tree()

    def show_help(self):
        """Show help documentation"""
        help_window = Toplevel(self.root)
        help_window.title("Help & Documentation")
        help_window.geometry("800x600")
        
        # Create notebook for help tabs
        help_notebook = ttk.Notebook(help_window, style='TNotebook')
        help_notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # General Help tab
        general_tab = ttk.Frame(help_notebook, style='TFrame')
        help_notebook.add(general_tab, text="General Help")
        
        general_text = """Enhanced Face Recognition Attendance System

1. Getting Started:
   - Ensure your camera is properly connected
   - Make sure classifier.xml exists in the application directory
   - Database should be properly configured

2. Basic Usage:
   - Click 'Start Recognition' to begin face detection
   - Adjust confidence threshold as needed
   - View attendance records in the Attendance tab

3. Features:
   - Multiple face detection methods (Haar, Dlib, CNN)
   - Liveness detection to prevent spoofing
   - Comprehensive reporting and analytics
   - Database management tools

For more detailed documentation, please refer to the user manual."""
        
        general_label = ttk.Label(general_tab, text=general_text, 
                                style='TLabel', justify=LEFT)
        general_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Troubleshooting tab
        trouble_tab = ttk.Frame(help_notebook, style='TFrame')
        help_notebook.add(trouble_tab, text="Troubleshooting")
        
        trouble_text = """Common Issues and Solutions:

1. Camera Not Working:
   - Check camera connection
   - Try a different camera index
   - Ensure no other application is using the camera

2. Recognition Accuracy:
   - Adjust confidence threshold
   - Use better lighting conditions
   - Try different face detection method
   - Rebuild face encodings

3. Database Errors:
   - Verify database connection settings
   - Check MySQL service is running
   - Ensure correct credentials

4. Performance Issues:
   - Use Haar method for faster detection
   - Reduce camera resolution
   - Close other applications"""
        
        trouble_label = ttk.Label(trouble_tab, text=trouble_text, 
                                style='TLabel', justify=LEFT)
        trouble_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # About tab
        about_tab = ttk.Frame(help_notebook, style='TFrame')
        help_notebook.add(about_tab, text="About")
        
        about_text = """Enhanced Face Recognition Attendance System
Version 2.0

Developed by: Your Name
Contact: your.email@example.com

Technologies Used:
- Python 3.x
- OpenCV
- Dlib
- MySQL
- Tkinter

License: MIT

© 2023 All Rights Reserved"""
        
        about_label = ttk.Label(about_tab, text=about_text, 
                              style='TLabel', justify=CENTER)
        about_label.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Close button
        ttk.Button(help_window, text="Close", 
                 command=help_window.destroy,
                 style='Primary.TButton').pack(pady=10)

    def on_close(self):
        """Handle window close event"""
        self.auto_save_running = False
        if self.recognition_active:
            self.recognition_active = False
            if self.capture is not None:
                self.capture.release()
        
        self.save_attendance_data()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    app = EnhancedFaceRecognition(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()