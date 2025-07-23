from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox


class Login_Window:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1150x800+0+0")

        # Background image
        self.bg = ImageTk.PhotoImage(file=r"C:\Users\HP\Desktop\Face recognization\My images\bg2.png")
        bg_label = Label(self.root, image=self.bg)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # User icon
        img1 = Image.open(r"C:\Users\HP\Desktop\Face recognization\My images\user.png").resize((100, 100), Image.Resampling.LANCZOS)
        self.photoimage1 = ImageTk.PhotoImage(img1)
        lblimg1 = Label(self.root, image=self.photoimage1, bg="#000000", borderwidth=0)
        lblimg1.place(x=730, y=175, width=100, height=100)

        # Title
        get_str = Label(self.root, text="Get Started", font=("Helvetica", 20, "bold"), fg="white", bg="#000000")
        get_str.place(x=705, y=280)

        # Username
        user_icon = Image.open(r"C:\Users\HP\Desktop\Face recognization\My images\user.png").resize((25, 25), Image.Resampling.LANCZOS)
        self.photoimage2 = ImageTk.PhotoImage(user_icon)
        lbl_user_icon = Label(self.root, image=self.photoimage2, bg="#000000", borderwidth=0)
        lbl_user_icon.place(x=650, y=323)

        username_label = Label(self.root, text="Username", font=("Helvetica", 12, "bold"), fg="white", bg="#000000")
        username_label.place(x=690, y=320)

        self.txtuser = ttk.Entry(self.root, font=("Helvetica", 12))
        self.txtuser.place(x=690, y=350, width=250)

        # Password
        lock_icon = Image.open(r"C:\Users\HP\Desktop\Face recognization\My images\lock.png").resize((25, 25), Image.Resampling.LANCZOS)
        self.photoimage3 = ImageTk.PhotoImage(lock_icon)
        lbl_lock_icon = Label(self.root, image=self.photoimage3, bg="#000000", borderwidth=0)
        lbl_lock_icon.place(x=650, y=395)

        password_label = Label(self.root, text="Password", font=("Helvetica", 12, "bold"), fg="white", bg="#000000")
        password_label.place(x=690, y=392)

        self.txtpass = ttk.Entry(self.root, font=("Helvetica", 12), show="*")
        self.txtpass.place(x=690, y=420, width=250)

        # Login Button
        loginbtn = Button(self.root, command=self.login, text="Login", font=("Helvetica", 13, "bold"),
                          bd=3, relief=RIDGE, fg="white", bg="red", activeforeground="white", activebackground="red")
        loginbtn.place(x=760, y=470, width=100, height=35)

        # Register Button
        registerbtn = Button(self.root, text="New User Register", font=("Helvetica", 10, "bold"), borderwidth=0,
                             fg="white", bg="#000000", activeforeground="white", activebackground="#000000")
        registerbtn.place(x=690, y=520, width=160)

        # Forgot Password Button
        forgetbtn = Button(self.root, text="Forgot Password?", font=("Helvetica", 10, "bold"), borderwidth=0,
                           fg="white", bg="#000000", activeforeground="white", activebackground="#000000")
        forgetbtn.place(x=690, y=545, width=160)

    def login(self):
        if self.txtuser.get() == "" or self.txtpass.get() == "":
            messagebox.showerror("Error", "All fields are required")
        elif self.txtuser.get() == "sweety" and self.txtpass.get() == "sweety19":
            messagebox.showinfo("Success", "Welcome to the Face Recognition Attendance System")
        else:
            messagebox.showerror("Invalid", "Invalid username or password")


if __name__ == "__main__":
    root = Tk()
    app = Login_Window(root)
    root.mainloop()
