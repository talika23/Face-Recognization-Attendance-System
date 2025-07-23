
from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
import numpy as np
import cv2

class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        self.title_lbl = Label(self.root, text="TRAIN DATA SET", font=("times new roman", 35, "bold"), bg="white", fg="red")
        self.title_lbl.place(x=0, y=0, width=1530, height=45)

        # Top Image
        try:
            img_top = Image.open("My images/face scan.png").resize((1530, 325), Image.LANCZOS)
            self.photoimg_top = ImageTk.PhotoImage(img_top)
            self.f_lbl = Label(self.root, image=self.photoimg_top)
            self.f_lbl.place(x=0, y=55, width=1530, height=325)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading top image: {str(e)}")

        # Train Button
        self.b1_1 = Button(self.root, text="TRAIN DATA", command=self.train_classifier, cursor="hand2",
                           font=("times new roman", 30, "bold"), bg="red", fg="white")
        self.b1_1.place(x=0, y=380, width=1530, height=60)

        # Bottom Image
        try:
            img_bottom = Image.open("My images/face scanner.png").resize((1530, 325), Image.LANCZOS)
            self.photoimg_bottom = ImageTk.PhotoImage(img_bottom)
            self.f_lbl = Label(self.root, image=self.photoimg_bottom)
            self.f_lbl.place(x=5, y=440, width=1530, height=325)
        except Exception as e:
            messagebox.showerror("Error", f"Error loading bottom image: {str(e)}")

    def train_classifier(self):
        try:
            data_dir = "data"
            if not os.path.exists(data_dir):
                messagebox.showerror("Error", "Data folder not found!")
                return

            path = [os.path.join(data_dir, file) for file in os.listdir(data_dir) if file.endswith(".jpg")]

            faces = []
            ids = []

            for image in path:
                try:
                    img = Image.open(image).convert('L')  # Gray scale
                    imageNp = np.array(img, 'uint8')

                    id = int(os.path.split(image)[1].split('.')[1])
                    print(f"Training Image: {image}, ID: {id}")
                    faces.append(imageNp)
                    ids.append(id)

                    cv2.imshow("Training", imageNp)
                    if cv2.waitKey(1) & 0xFF == 27:  # Escape key
                    
                        break
                except Exception as e:
                    print(f"Skipping image {image}: {str(e)}")

            ids = np.array(ids)

            # Train and Save Model
            clf = cv2.face.LBPHFaceRecognizer_create()
            if len(faces) > 0 and len(ids) > 0:
              clf.train(faces, ids)
            #   clf.train(faces, np.array(ids))
              clf.write("classifier.xml")
            else:
              messagebox.showerror("Error", "No data found for training.")

            cv2.destroyAllWindows()
            messagebox.showinfo("Result", "Training dataset completed!")

        except Exception as e:
            messagebox.showerror("Error", f"Training failed due to: {str(e)}")

# Main Execution
if __name__ == "__main__":
    root = Tk()
    obj = Train(root)
    root.mainloop()





                                                                       

    
       









