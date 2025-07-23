from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime
import webbrowser
import platform
import socket
import json
import os

class Help:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System - Help Desk")
        self.is_dark = True

        # Title Label
        self.title_lbl = Label(self.root, text="HELP DESK", font=("Segoe UI", 35, "bold"), bg="#f0f0f0", fg="#0a58ca")
        self.title_lbl.place(x=0, y=0, width=1530, height=60)

        # Background Image
        bg_image = Image.open("My images/help.png").resize((1530, 790), Image.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(bg_image)
        bg_lbl = Label(self.root, image=self.bg_photo)
        bg_lbl.place(x=0, y=60, width=1530, height=730)

        # Help Box Frame
        self.help_frame = Frame(bg_lbl, bg="#ffffff", bd=2, relief=GROOVE)
        self.help_frame.place(x=500, y=80, width=580, height=600)

        Label(self.help_frame, text="Need Assistance?", font=("Segoe UI", 20, "bold"), bg="white", fg="#222").pack(pady=10)

        # Contact Details
        Label(self.help_frame, text="Email: talikarathod91@gmail.com", font=("Segoe UI", 13), bg="white", fg="green").pack(anchor=W, padx=20)
        Label(self.help_frame, text="Phone: +91 9876543210", font=("Segoe UI", 13), bg="white", fg="green").pack(anchor=W, padx=20)

        # LinkedIn
        Label(self.help_frame, text="LinkedIn:", font=("Segoe UI", 13, "bold"), bg="white").pack(anchor=W, padx=20, pady=(10, 0))
        link = Label(self.help_frame, text="linkedin.com/in/talika-rathod-957795280", font=("Segoe UI", 12), bg="white", fg="blue", cursor="hand2")
        link.pack(anchor=W, padx=40)
        link.bind("<Button-1>", lambda e: webbrowser.open("https://linkedin.com/in/talika-rathod-957795280"))

        # System Info
        Label(self.help_frame, text="System Info:", font=("Segoe UI", 13, "bold"), bg="white").pack(anchor=W, padx=20, pady=(15, 0))
        sys_info = f"OS: {platform.system()} {platform.release()}\nHostname: {socket.gethostname()}"
        Label(self.help_frame, text=sys_info, font=("Segoe UI", 11), bg="white", justify=LEFT).pack(anchor=W, padx=40)

        # Time Display
        self.datetime_label = Label(self.help_frame, font=("Segoe UI", 11), bg="white", fg="black")
        self.datetime_label.pack(pady=(10, 0))
        self.update_time()

        # Buttons Section
        Button(self.help_frame, text="📧 Email Us", font=("Segoe UI", 12), bg="#28a745", fg="white", cursor="hand2",
               command=self.send_email).pack(pady=5, fill=X, padx=20)

        Button(self.help_frame, text="🔄 Refresh Time", font=("Segoe UI", 12), bg="#007bff", fg="white", cursor="hand2",
               command=self.update_time).pack(pady=5, fill=X, padx=20)

        Button(self.help_frame, text="📘 Open Docs", font=("Segoe UI", 12), bg="#6f42c1", fg="white", cursor="hand2",
               command=lambda: webbrowser.open("https://example.com/help-docs")).pack(pady=5, fill=X, padx=20)

        Button(self.help_frame, text="💬 Open Chatbot", font=("Segoe UI", 12), bg="#fd7e14", fg="white", cursor="hand2",
               command=self.open_chatbot).pack(pady=5, fill=X, padx=20)

        Button(self.help_frame, text="📤 Submit Feedback", font=("Segoe UI", 12), bg="#6610f2", fg="white", cursor="hand2",
               command=self.open_feedback_form).pack(pady=5, fill=X, padx=20)

        Button(self.help_frame, text="📄 View FAQs", font=("Segoe UI", 12), bg="#20c997", fg="white", cursor="hand2",
               command=self.show_faqs).pack(pady=5, fill=X, padx=20)

        Button(self.help_frame, text="🌗 Toggle Theme", font=("Segoe UI", 12), bg="#6c757d", fg="white", cursor="hand2",
               command=self.toggle_theme).pack(pady=5, fill=X, padx=20)

    def update_time(self):
        now = datetime.now()
        self.datetime_label.config(text=now.strftime("%A, %d %B %Y | %I:%M:%S %p"))
        self.root.after(1000, self.update_time)

    def send_email(self):
        webbrowser.open("mailto:talikarathod91@gmail.com")

    def open_chatbot(self):
        top = Toplevel(self.root)
        top.title("Chatbot Assistant")
        top.geometry("450x400")
        chat_frame = Frame(top, bg="#7b9ec1")
        chat_frame.pack(fill=BOTH, expand=True)
        self.chat_log = Text(chat_frame, bg="white", font=("Segoe UI", 11), wrap=WORD)
        self.chat_log.pack(fill=BOTH, expand=True, padx=10, pady=10)
        self.user_input = Entry(chat_frame, font=("Segoe UI", 11))
        self.user_input.pack(side=LEFT, fill=X, expand=True, padx=5, pady=5)
        Button(chat_frame, text="Send", command=self.handle_chat).pack(side=RIGHT, padx=5, pady=5)

    def handle_chat(self):
        user_msg = self.user_input.get()
        if user_msg:
            self.chat_log.insert(END, f"You: {user_msg}\n")
            reply = self.generate_bot_response(user_msg)
            self.chat_log.insert(END, f"Bot: {reply}\n")
            self.user_input.delete(0, END)

    def generate_bot_response(self, message):
        message = message.lower()
        if "email" in message:
            return "You can email us at talikarathod91@gmail.com."
        elif "error" in message or "issue" in message:
            return "Please use the feedback form to describe your issue."
        elif "thank" in message:
            return "You're welcome! 😊"
        else:
            return "I'm a simple assistant. For more help, visit our docs."

    def open_feedback_form(self):
        top = Toplevel(self.root)
        top.title("Feedback Form")
        top.geometry("500x450")
        top.config(bg="#df9393")

        Label(top, text="Feedback Form", font=("Segoe UI", 18, "bold"), bg="#ffffff", fg="#343a40").pack(pady=10)

        Label(top, text="Name", bg="#ffffff", font=("Segoe UI", 12)).pack(anchor=W, padx=20)
        name_entry = Entry(top, width=40, font=("Segoe UI", 11))
        name_entry.pack(padx=20, pady=5)

        Label(top, text="Email", bg="#ffffff", font=("Segoe UI", 12)).pack(anchor=W, padx=20)
        email_entry = Entry(top, width=40, font=("Segoe UI", 11))
        email_entry.pack(padx=20, pady=5)

        Label(top, text="Message", bg="#f2e7e7", font=("Segoe UI", 12)).pack(anchor=W, padx=20)
        msg_text = Text(top, height=6, width=40, font=("Segoe UI", 11))
        msg_text.pack(padx=20, pady=5)

        def save_feedback():
            feedback = {
                "name": name_entry.get(),
                "email": email_entry.get(),
                "message": msg_text.get("1.0", END).strip()
            }
            if not os.path.exists("feedback.json"):
                with open("feedback.json", "w") as f:
                    json.dump([], f)
            with open("feedback.json", "r+") as f:
                data = json.load(f)
                data.append(feedback)
                f.seek(0)
                json.dump(data, f, indent=4)
            messagebox.showinfo("Success", "Thank you for your feedback!")
            top.destroy()

        Button(top, text="Submit", bg="#198754", fg="white", font=("Segoe UI", 12), command=save_feedback).pack(pady=15)

    def show_faqs(self):
        faqs = (
            "Q: How do I reset my password?\nA: Contact admin.\n\n"
            "Q: How to report an error?\nA: Use the Feedback form.\n\n"
            "Q: What is this system for?\nA: It's for attendance using face recognition."
        )
        messagebox.showinfo("FAQs", faqs)

    def toggle_theme(self):
        self.is_dark = not self.is_dark
        bg_color = "#343a40" if self.is_dark else "white"
        fg_color = "white" if self.is_dark else "black"
        self.help_frame.config(bg=bg_color)
        for widget in self.help_frame.winfo_children():
            widget.config(bg=bg_color, fg=fg_color)

# Main Execution
if __name__ == "__main__":
    root = Tk()
    obj = Help(root)
    root.mainloop()