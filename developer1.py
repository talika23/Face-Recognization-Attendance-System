from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import qrcode
import webbrowser
import itertools
from datetime import datetime

class StylishDeveloperUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Developer Portfolio")
        self.root.geometry("1100x800+100+20")
        self.root.config(bg="#121212")

        # === Set Background ===
        bg_img = Image.open("My images/dev4.png").resize((1100, 800), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_img)
        bg_label = Label(self.root, image=self.bg_photo)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Generate QR Codes if missing
        self.generate_qr("mailto:talikarathod91@email.com", "email_qr.png")
        self.generate_qr("https://linkedin.com/in/talika-rathod-957795280", "linkedin_qr.png")
        self.generate_qr("https://github.com/talika23", "github_qr.png")

        # Main Frame
        card = Frame(self.root, bg="#1f1f2e")
        card.place(x=40, y=40, width=1000, height=720)

        # Profile Image
        img = Image.open("My images/alika1.jpg").resize((180, 180), Image.LANCZOS)
        self.profile_photo = ImageTk.PhotoImage(img)
        Label(card, image=self.profile_photo, bg="#1f1f2e", bd=2, relief=RIDGE).place(x=30, y=30)

        # Name, Role & About
        Label(card, text="Talika Rathod", font=("Segoe UI", 24, "bold"), bg="#1f1f2e", fg="white").place(x=230, y=40)
        Label(card, text="Python Developer", font=("Segoe UI", 16), bg="#1f1f2e", fg="#b5b5b5").place(x=230, y=80)

        about = ("I am a passionate Python developer with experience in intelligent systems,\n"
                 "machine learning, and smart UI design. I build real-time apps blending logic and design.")
        Label(card, text=about, font=("Segoe UI", 11), bg="#1f1f2e", fg="white", justify=LEFT).place(x=230, y=120)

        # Animated Quote
        self.quotes = itertools.cycle([
            "\U0001F680 Turning coffee into code!",
            "\U0001F4A1 Building smart, scalable systems.",
            "\U0001F331 Learning every day.",
            "\U0001F469‍\U0001F4BB Python | ML | AI | Tkinter"
        ])
        self.quote_label = Label(card, text="", font=("Segoe UI", 12, "italic"), bg="#1f1f2e", fg="#00f2ff")
        self.quote_label.place(x=230, y=190)
        self.rotate_quote()

        # Date and Time Display
        self.datetime_label = Label(card, font=("Segoe UI", 11), bg="#1f1f2e", fg="white")
        self.datetime_label.place(x=720, y=20)
        self.update_datetime()

        # Tech Stack
        Label(card, text="Tech Stack", font=("Segoe UI", 16, "bold"), bg="#6262f0", fg="white").place(x=410, y=250)
        skills = ["Python", "OpenCV", "MySQL", "Tkinter", "HTML", "CSS"]
        colors = ["#8F3737", "#277ed4", "#fab1a0", "#9bdbfe", "#cba836", "#55efc4"]
        x = 180
        for i, skill in enumerate(skills):
            Label(card, text=skill, font=("Segoe UI", 11, "bold"), bg=colors[i], fg="#121212",
                  padx=15, pady=10, relief=RAISED, bd=1).place(x=x, y=290, width=110, height=45)
            x += 130

        # Projects Section
        Label(card, text="Projects", font=("Segoe UI", 16, "bold"), bg="#1f1f2e", fg="white").place(x=30, y=340)
        projects = [
            ("Face Recognition", "My images/facehome.png", "Automated attendance with face recognition.\nRole: Backend + UI"),
            ("Agro Analytics", "My images/home.jpg", "Smart agri portal with crop & weather info.\nRole: Full-Stack"),
            ("Endometrial Cancer Detection", "My images/endometrial.png", "A multimodal deep learning model that analyzes genomic and image data for accurate endometrial cancer detection.")
        ]
        x_proj = 30
        for name, path, desc in projects:
            proj_frame = Frame(card, bg="#292943", bd=1)
            proj_frame.place(x=x_proj, y=380, width=280, height=160)
            try:
                img = Image.open(path).resize((280, 80), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                lbl = Label(proj_frame, image=photo, bg="#292943")
                lbl.image = photo
                lbl.pack()
            except:
                Label(proj_frame, text="Image Missing", bg="#292943", fg="white").pack()
            Label(proj_frame, text=name, font=("Segoe UI", 10, "bold"), bg="#292943", fg="white").pack()
            Label(proj_frame, text=desc, font=("Segoe UI", 9), bg="#292943", fg="#b5b5b5", wraplength=260, justify=LEFT).pack()
            x_proj += 320

        # Contact Section
        Label(card, text="Contact Me", font=("Segoe UI", 16, "bold"), bg="#1f1f2e", fg="white").place(x=30, y=560)
        button_data = [
            ("\U0001F4E7 Email", "#e74c3c", lambda: self.open_link("mailto:talikarathod91@email.com")),
            ("\U0001F517 LinkedIn", "#3498db", lambda: self.open_link("https://linkedin.com/in/talika-rathod-957795280")),
            ("\U0001F409 GitHub", "#2c3e50", lambda: self.open_link("https://github.com/talika23")),
            ("\U0001F4C4 Resume", "#f1c40f", self.open_resume),
            ("\U0001F4F1 Show QR", "#2ecc71", self.show_qr_popup)
        ]
        x_start = 30
        for text, color, action in button_data:
            Button(card, text=text, font=("Segoe UI", 12, "bold"), bg=color,
                   fg="white" if color != "#f1c40f" else "#121212",
                   activebackground="#f7f7f7", cursor="hand2", relief=RAISED, bd=1,
                   command=action).place(x=x_start, y=600, width=180, height=50)
            x_start += 190

    def rotate_quote(self):
        quote = next(self.quotes)
        self.quote_label.config(text=quote)
        self.root.after(3000, self.rotate_quote)

    def update_datetime(self):
        now = datetime.now()
        time_string = now.strftime("%I:%M:%S %p")
        date_string = now.strftime("%A, %d %B %Y")
        self.datetime_label.config(text=f"{date_string}  |  {time_string}")
        self.root.after(1000, self.update_datetime)

    def open_link(self, url):
        webbrowser.open(url)

    def open_resume(self):
        if os.path.exists("resume.pdf"):
            os.startfile("resume.pdf")
        else:
            messagebox.showerror("Error", "resume.pdf not found.")

    def generate_qr(self, data, filename):
        if not os.path.exists(filename):
            img = qrcode.make(data)
            img.save(filename)

    def show_qr_popup(self):
        top = Toplevel()
        top.title("Scan to Connect")
        top.geometry("320x500")
        top.config(bg="#121212")
        self.qr_refs = {}
        files = {
            "LinkedIn": "linkedin_qr.png",
            "Email": "email_qr.png",
            "GitHub": "github_qr.png"
        }
        for name, file in files.items():
            try:
                img = Image.open(file).resize((130, 130), Image.LANCZOS)
                qr_img = ImageTk.PhotoImage(img)
                self.qr_refs[name] = qr_img
                Label(top, text=name, font=("Segoe UI", 12, "bold"), bg="#121212", fg="white").pack(pady=5)
                Label(top, image=qr_img, bg="#121212").pack()
            except FileNotFoundError:
                Label(top, text=f"{name} QR not found", font=("Segoe UI", 10), fg="red", bg="#121212").pack(pady=10)

# Run App
if __name__ == "__main__":
    root = Tk()
    app = StylishDeveloperUI(root)
    root.mainloop()