from tkinter import Tk, Button, Label, LabelFrame, filedialog, Scale
from PIL import ImageTk, Image, ImageOps, ImageFilter, ImageEnhance
from cv2 import cvtColor, COLOR_BGR2RGB, VideoWriter, VideoWriter_fourcc, COLOR_BGR2GRAY, imshow,\
    waitKey, VideoCapture, COLOR_GRAY2RGB, Canny, threshold, THRESH_BINARY, findContours, RETR_TREE, CHAIN_APPROX_NONE,\
    drawContours, COLOR_RGB2GRAY, imread, setMouseCallback, EVENT_LBUTTONDOWN, resize, putText, FONT_HERSHEY_SIMPLEX,\
    LINE_AA, medianBlur
from moviepy.editor import VideoFileClip, concatenate_videoclips
from numpy import zeros, uint8, hstack, array
from datetime import datetime


# Navigate images and view selected (Ali Alam)
def nav_view_img():
    # Accepted file types
    acc_types = (("jpg files", "*.jpg"), ("png files", "*.png"))
    # Create a file menu
    global img, img_view, edited_img, vid
    vid = 0
    file_path = filedialog.askopenfilename(initialdir="C:/", title="Select an Image", filetypes=acc_types)
    # Open the image in an acceptable format and resize
    img = imread(file_path)
    img_view = Image.open(file_path)
    img_view = ImageTk.PhotoImage(img_view.resize((230, 263)))
    # View the img
    Label(win, image=img_view).place(x=233, y=160)

# Navigate videos and view first frame of selected video (Abdallah Badran)
def nav_view_video():
    # Create a file menu , filetypes=("mp4 videos", "*.mp4")
    global clip, frame_view, vid_mode, vid, frame1
    vid = 1
    vid_mode = ""
    vid_file_path = filedialog.askopenfilename(initialdir="C:/", title="Select a Video")
    clip = VideoFileClip(vid_file_path)
    frame1 = clip.get_frame(1)
    frame_view = Image.fromarray(frame1)
    frame_view = ImageTk.PhotoImage(frame_view.resize((230, 263)))
    Label(win, image=frame_view).place(x=233, y=160)

# Convert to greyscale (Abdallah Badran)
def greyscale():
    # for image
    if vid == 0:
        global gray_img_view, edited_img
        # Convert image to grayscale
        edited_img = Image.fromarray(img)
        edited_img = ImageOps.grayscale(edited_img)
        # Open the image in an acceptable format and resize
        gray_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
        # View the img
        Label(win, image=gray_img_view).place(x=533, y=160)
    # for video
    else:
        global gray_frame_view, vid_mode
        # Convert video to grayscale
        vid_mode = "grey"
        # View the img
        gray_frame_view = Image.fromarray(frame1)
        gray_frame_view = ImageOps.grayscale(gray_frame_view)
        gray_frame_view = ImageTk.PhotoImage(gray_frame_view.resize((230, 263)))
        Label(win, image=gray_frame_view).place(x=533, y=160)

# Apply canny (Abdallah Badran)
def canny():
    # for image
    if vid == 0:
        global can_img_view, edited_img
        # Convert image to grayscale
        edited_img = Image.fromarray(img)
        edited_img = ImageOps.grayscale(edited_img)
        edited_img = edited_img.filter(ImageFilter.FIND_EDGES)
        # Open the image in an acceptable format and resize
        can_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
        # View the img
        Label(win, image=can_img_view).place(x=533, y=160)
    # for video
    else:
        global canny_frame_view, vid_mode
        # Convert video to grayscale
        vid_mode = "canny"
        # View the img
        canny_frame_view = Image.fromarray(frame1)
        canny_frame_view = ImageOps.grayscale(canny_frame_view)
        canny_frame_view = canny_frame_view.filter(ImageFilter.FIND_EDGES)
        canny_frame_view = ImageTk.PhotoImage(canny_frame_view.resize((230, 263)))
        Label(win, image=canny_frame_view).place(x=533, y=160)

# Draw contours (Gerges Wageh)
def contour():
    if vid == 0:
        global cont_img_view, edited_img
        # Convert image to grayscale
        edited_img = cvtColor(img, COLOR_RGB2GRAY)
        thresholdValue, edited_img = threshold(edited_img, 127, 255, THRESH_BINARY)
        contours, hierarchy = findContours(edited_img, RETR_TREE, CHAIN_APPROX_NONE)
        edited_img = drawContours(img, contours, -1, (0, 255, 0), 2)
        edited_img = Image.fromarray(edited_img)
        cont_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
        # View the img
        Label(win, image=cont_img_view).place(x=533, y=160)
    else:
        global cont_frame_view, vid_mode
        # Convert video to grayscale
        vid_mode = "contour"
        # View the img
        cont_frame_view = cvtColor(frame1, COLOR_RGB2GRAY)
        thresholdValue, cont_frame_view = threshold(cont_frame_view, 127, 255, THRESH_BINARY)
        contours, hierarchy = findContours(cont_frame_view, RETR_TREE, CHAIN_APPROX_NONE)
        cont_frame_view = drawContours(frame1, contours, -1, (0, 255, 0), 2)
        cont_frame_view = Image.fromarray(cont_frame_view)
        cont_frame_view = ImageTk.PhotoImage(cont_frame_view.resize((230, 263)))
        Label(win, image=cont_frame_view).place(x=533, y=160)

# callback function for the "detect" function to detect color selected for image (Ali Alam)
def img_mouse_click(event, x, y, flag, param):
    global detect_img_view, edited_img
    if event == EVENT_LBUTTONDOWN:
        blue_value = img[y, x, 0]
        green_value = img[y, x, 1]
        red_value = img[y, x, 2]
        edited_img = zeros([300, 300, 3], uint8)
        edited_img[:] = [blue_value, green_value, red_value]
        edited_img = Image.new(mode="RGB", size=(600, 600), color=(red_value, green_value, blue_value))
        detect_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
        string = str(blue_value) + "," + str(green_value) + "," + str(red_value)
        putText(img, string, (x, y), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        imshow("Detect Color", img)
        # View the img
        Label(win, image=detect_img_view).place(x=533, y=160)

# callback function for the "detect" function to detect color selected for video (Ali Alam)
def vid_mouse_click(event, x, y, flag, param):
    global detect_frame_view, edited_frame, frame
    if event == EVENT_LBUTTONDOWN:
        blue_value = frame[y, x, 0]
        green_value = frame[y, x, 1]
        red_value = frame[y, x, 2]
        edited_frame = zeros([300, 300, 3], uint8)
        edited_frame[:] = [blue_value, green_value, red_value]
        edited_frame = Image.new(mode="RGB", size=(600, 600), color=(red_value, green_value, blue_value))
        detect_frame_view = ImageTk.PhotoImage(edited_frame.resize((230, 263)))
        string = str(blue_value) + "," + str(green_value) + "," + str(red_value)
        putText(frame, string, (x, y), FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        imshow("Detect Color", frame)
        # View the img
        Label(win, image=detect_frame_view).place(x=533, y=160)

# detect colors for seleceted regions for images and videos (Ali Alam)
def detect():
    if vid == 0:
        global cont_img_view, edited_img
        imshow("Detect Color", img)
        setMouseCallback("Detect Color", img_mouse_click)
        waitKey(0)
    else:
        global cont_frame_view, vid_mode, frame
        for frame in clip.iter_frames():
            frame = cvtColor(frame, COLOR_BGR2RGB)
            imshow("Detect Color", frame)
            setMouseCallback("Detect Color", vid_mouse_click)
            if waitKey(5) == ord("e"):
                break
# Append an image/video to existing image/video (Gerges Wageh)
def append():
    if vid == 0:
        global append_img_view, edited_img
        # Accepted file types
        acc_types = (("jpg files", "*.jpg"), ("png files", "*.png"))
        file_path = filedialog.askopenfilename(initialdir="C:/", title="Select an Image", filetypes=acc_types)
        # Open the image in an acceptable format and resize
        img2 = imread(file_path)
        imshow("Selected", img2)
        img_temp = cvtColor(img, COLOR_BGR2RGB)
        img_temp = Image.fromarray(img_temp)
        img2 = cvtColor(img2, COLOR_BGR2RGB)
        img2 = Image.fromarray(img2)
        edited_img = Image.new('RGB', (img_temp.width + img2.width, img_temp.height))
        edited_img.paste(img_temp, (0, 0))
        edited_img.paste(img2, (img_temp.width, 0))
        #edited_img = Image.fromarray(edited_img)
        append_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
        # View the img
        Label(win, image=append_img_view).place(x=533, y=160)
    else:
        global frame2_view, vid_mode, final_vid
        # Convert video to grayscale
        vid_mode = "append"
        # View the img
        vid2_file_path = filedialog.askopenfilename(initialdir="C:/", title="Select a Video")
        clip2 = VideoFileClip(vid2_file_path)
        frame2 = clip2.get_frame(1)
        frame2_view = Image.fromarray(frame2)
        frame2_view = ImageTk.PhotoImage(frame2_view.resize((230, 263)))
        Label(win, image=frame2_view).place(x=533, y=160)
        final_vid = concatenate_videoclips([clip, clip2])

# slider for image sharpening (Mohamed Ramadan)
def scaler_fn():
    global sharpen_img_view, edited_img
    # Open the image in an acceptable format and resize
     # View the img
    edited_img = cvtColor(img, COLOR_BGR2RGB)
    edited_img = Image.fromarray(edited_img)
    enhancer = ImageEnhance.Sharpness(edited_img)
    scaler_val = int(slider.get())
    edited_img = enhancer.enhance(scaler_val)
    sharpen_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
    Label(win, image=sharpen_img_view).place(x=533, y=160)
    #scaler_win.quit()

# slider for video sharpening (Mohamed Ramadan)
def vid_scaler_fn():
    global edited_frame, vid_scaler_win, vid_slider, vid_scaler_val
    # Open the image in an acceptable format and resize
     # View the img
    #edited_frame = cvtColor(frame1, COLOR_BGR2RGB)
    edited_frame = Image.fromarray(frame1)
    enhancer = ImageEnhance.Sharpness(edited_frame)
    vid_scaler_val = int(vid_slider.get())
    edited_frame = enhancer.enhance(vid_scaler_val)
    edited_frame = ImageTk.PhotoImage(edited_frame.resize((230, 263)))
    Label(win, image=edited_frame).place(x=533, y=160)

# sharpening function (Mohammed Ramdan)
def sharpen():
    # for image
    if vid == 0:
        global  edited_img, scaler_win, slider
        scaler_win = Tk()
        scaler_win.title("Sharpen")
        scaler_win.geometry("300x200")
        slider = Scale(scaler_win, from_=0, to=255, orient="horizontal")
        slider.pack()
        Button(scaler_win, text="Apply", fg="white", bg="blue", width=5, bd=5, height=3, activebackground="white",
               activeforeground="blue", font=("Segoe Script", 10), command= scaler_fn).pack(pady=10)
        scaler_win.mainloop()
    # for video
    else:
        global  edited_frame, vid_scaler_win, vid_slider, vid_mode
        vid_mode = "sharp"
        vid_scaler_win = Tk()
        vid_scaler_win.title("Sharpen")
        vid_scaler_win.geometry("300x200")
        vid_slider = Scale(vid_scaler_win, from_=0, to=255, orient="horizontal")
        vid_slider.pack()
        Button(vid_scaler_win, text="Apply", fg="white", bg="blue", width=5, bd=5, height=3, activebackground="white",
               activeforeground="blue", font=("Segoe Script", 10), command= vid_scaler_fn).pack(pady=10)
        vid_scaler_win.mainloop()

# slider for bluring image (Abdelhamid Khaled)
def blur_scaler_fn():
    global blur_img_view, edited_img
    # Open the image in an acceptable format and resize
     # View the img
    edited_img = cvtColor(img, COLOR_BGR2RGB)
    edited_img = Image.fromarray(edited_img)
    scaler_val = int(slider.get())
    edited_img = edited_img.filter(ImageFilter.GaussianBlur(scaler_val))
    blur_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
    Label(win, image=blur_img_view).place(x=533, y=160)
    #scaler_win.quit()

# slider for bluring video (Abdelhamid Khaled)
def vid_blur_scaler_fn():
    global edited_frame, vid_scaler_win, vid_slider, vid_scaler_val
    # Open the image in an acceptable format and resize
     # View the img
    edited_frame = Image.fromarray(frame1)
    vid_scaler_val = int(vid_slider.get())
    edited_frame = edited_frame.filter(ImageFilter.GaussianBlur(vid_scaler_val))
    edited_frame = ImageTk.PhotoImage(edited_frame.resize((230, 263)))
    Label(win, image=edited_frame).place(x=533, y=160)

# blurring function (Abdelhamid Khaled)
def blur():
    # for image
    if vid == 0:
        global  edited_img, scaler_win, slider
        scaler_win = Tk()
        scaler_win.title("Blur")
        scaler_win.geometry("300x200")
        slider = Scale(scaler_win, from_=0, to=255, orient="horizontal")
        slider.pack()
        Button(scaler_win, text="Apply", fg="white", bg="blue", width=5, bd=5, height=3, activebackground="white",
               activeforeground="blue", font=("Segoe Script", 10), command= blur_scaler_fn).pack(pady=10)
        scaler_win.mainloop()
    # for video
    else:
        global  edited_frame, vid_scaler_win, vid_slider, vid_mode
        vid_mode = "sharp"
        vid_scaler_win = Tk()
        vid_scaler_win.title("Blur")
        vid_scaler_win.geometry("300x200")
        vid_slider = Scale(vid_scaler_win, from_=0, to=255, orient="horizontal")
        vid_slider.pack()
        Button(vid_scaler_win, text="Apply", fg="white", bg="blue", width=5, bd=5, height=3, activebackground="white",
               activeforeground="blue", font=("Segoe Script", 10), command= vid_blur_scaler_fn).pack(pady=10)
        vid_scaler_win.mainloop()

# write date and time (Abdelhamid khaled)
def date_time():
    if vid == 0:
        global date_img_view, edited_img
        edited_img = cvtColor(img, COLOR_BGR2RGB)
        edited_img = putText(edited_img, str(datetime.now()), (10, 30), FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2, LINE_AA)
        edited_img = Image.fromarray(edited_img)
        # Open the image in an acceptable format and resize
        date_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
        # View the img
        Label(win, image=date_img_view).place(x=533, y=160)
    else:
        global date_frame_view, vid_mode
        # Convert video to grayscale
        vid_mode = "date"
        # View the img
        putText(frame1, str(datetime.now()), (10, 30), FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2, LINE_AA)
        date_frame_view = Image.fromarray(frame1)
        date_frame_view = ImageTk.PhotoImage(date_frame_view.resize((230, 263)))
        Label(win, image=date_frame_view).place(x=533, y=160)

# clear noise (Mohammed Ramdan)
def clear_noise():
    if vid == 0:
        global clr_img_view, edited_img
        # Convert image to grayscale
        edited_img = medianBlur(img, 5)
        edited_img = Image.fromarray(edited_img)
        # Open the image in an acceptable format and resize
        clr_img_view = ImageTk.PhotoImage(edited_img.resize((230, 263)))
        # View the img
        Label(win, image=clr_img_view).place(x=533, y=160)
    else:
        global c_frame_view, vid_mode
        # Convert video to grayscale
        vid_mode = "clear"
        # View the img
        c_frame_view = medianBlur(frame1, 5)
        c_frame_view = Image.fromarray(c_frame_view)
        c_frame_view = ImageTk.PhotoImage(c_frame_view.resize((230, 263)))
        Label(win, image=c_frame_view).place(x=533, y=160)

# save edited image/video for each case
def save_edited():
    # Select folder to save edited image
    global clip
    # Save edited image (Ali Alam)
    if vid == 0:
        # Accepted file types
        acc_types = (("jpg files", "*.jpg"), ("png files", "*.png"))
        img_path = filedialog.asksaveasfilename(title="Select File", defaultextension=".*", filetypes=acc_types,
                                        initialfile="Edited.jpg", initialdir="D:/")
        edited_img.save(img_path)
    # Save grey video (Abdallah Badran)
    elif vid_mode == "grey" and vid == 1:
        #acc_types = (("mp4 videos", ".mp4"))
        vid_path = filedialog.asksaveasfilename(title="Select File", defaultextension="*.mp4",
                                        initialfile="Edited.mp4", initialdir="D:/")
        width, height = clip.size
        writer = VideoWriter(vid_path, VideoWriter_fourcc('m', 'p', '4', 'v'), clip.fps, (width, height), 0)
        for frame in clip.iter_frames():
            frame = cvtColor(frame, COLOR_BGR2GRAY)
            writer.write(frame)
    # save canny video (Abdallah Badran)
    elif vid_mode == "canny" and vid == 1:
        vid_path = filedialog.asksaveasfilename(title="Select File", defaultextension="*.mp4",
                                                initialfile="Edited.mp4", initialdir="D:/")
        width, height = clip.size
        writer = VideoWriter(vid_path, VideoWriter_fourcc('m', 'p', '4', 'v'), clip.fps, (width, height), 0)
        for frame in clip.iter_frames():
            #frame = cvtColor(frame, COLOR_BGR2GRAY)
            canny_frame = Canny(frame, 50, 200)
            writer.write(canny_frame)
    # save contour video (Gerges Wageh)
    elif vid_mode == "contour" and vid == 1:
        vid_path = filedialog.asksaveasfilename(title="Select File", defaultextension="*.mp4",
                                                initialfile="Edited.mp4", initialdir="D:/")
        width, height = clip.size
        writer = VideoWriter(vid_path, VideoWriter_fourcc('m', 'p', '4', 'v'), clip.fps, (width, height))
        for frame in clip.iter_frames():
            #frame = cvtColor(frame, COLOR_BGR2GRAY)
            cont_frame = cvtColor(frame, COLOR_RGB2GRAY)
            thresholdValue, cont_frame = threshold(cont_frame, 127, 255, THRESH_BINARY)
            contours, hierarchy = findContours(cont_frame, RETR_TREE, CHAIN_APPROX_NONE)
            cont_frame = drawContours(frame, contours, -1, (0, 255, 0), 2)
            writer.write(cont_frame)
    # save appended video (Gerges Wageh)
    elif vid_mode == "append" and vid == 1:
        vid_path = filedialog.asksaveasfilename(title="Select File", defaultextension="*.mp4",
                                                initialfile="Edited.mp4", initialdir="D:/")
        final_vid.write_videofile(vid_path)
    # save sahrpened video (Mohammed Ramadan)
    elif vid_mode == "sharp" and vid == 1:
        vid_path = filedialog.asksaveasfilename(title="Select File", defaultextension="*.mp4",
                                                initialfile="Edited.mp4", initialdir="D:/")
        width, height = clip.size
        writer = VideoWriter(vid_path, VideoWriter_fourcc('m', 'p', '4', 'v'), clip.fps, (width, height))
        for frame in clip.iter_frames():
            # frame = cvtColor(frame, COLOR_BGR2GRAY)
            frame = cvtColor(frame, COLOR_BGR2RGB)
            frame = Image.fromarray(frame)
            frame = frame.filter(ImageFilter.GaussianBlur(vid_scaler_val))
            writer.write(array(frame))
            #vid_scaler_val
    # save date and time video (Abelhamid khaled)
    elif vid_mode == "date" and vid == 1:
        vid_path = filedialog.asksaveasfilename(title="Select File", defaultextension="*.mp4",
                                                initialfile="Edited.mp4", initialdir="D:/")
        width, height = clip.size
        writer = VideoWriter(vid_path, VideoWriter_fourcc('m', 'p', '4', 'v'), clip.fps, (width, height))
        for frame in clip.iter_frames():
            # frame = cvtColor(frame, COLOR_BGR2GRAY)
            frame = cvtColor(frame, COLOR_BGR2RGB)
            putText(frame, str(datetime.now()), (10, 30), FONT_HERSHEY_SIMPLEX, 1.1, (255, 0, 0), 2, LINE_AA)
            writer.write(frame)
            #vid_scaler_val
    # save cleared noise video (Mohhamed ramadan)
    elif vid_mode == "clear" and vid == 1:
        #acc_types = (("mp4 videos", ".mp4"))
        vid_path = filedialog.asksaveasfilename(title="Select File", defaultextension="*.mp4",
                                        initialfile="Edited.mp4", initialdir="D:/")
        width, height = clip.size
        writer = VideoWriter(vid_path, VideoWriter_fourcc('m', 'p', '4', 'v'), clip.fps, (width, height))
        for frame in clip.iter_frames():
            frame = medianBlur(frame, 3)
            writer.write(frame)


# ALL participants shared in the GUI via zoom meetings to agree on a suitable layout

# Create a main window
win = Tk()
# Set the window main size
win.geometry("1000x600")
# Title the main window
win.title("Dead Pixels Editor")
# Set the main window background
win.configure(background="#A2BAF5")
# Create window label
Label(win, text="Dead Pixels", font=("Segoe Script", 30, "bold"), bg="#A2BAF5", relief="groove", bd=10)\
    .place(x=370, y=10)
# Create upload image button
Button(win, text="+\nUpload Image", fg="white", bg="blue", width=10, bd=10, height=3, activebackground="white",
       activeforeground="blue", font=("Segoe Script", 13), command=nav_view_img).place(x=220, y=450)
# Create upload video button
Button(win, text="+\nUpload Video", fg="white", bg="blue", width=10, bd=10, height=3, activebackground="white",
       activeforeground="blue", font=("Segoe Script", 13), command=nav_view_video).place(x=630, y=450)
# Create save button
Button(win, text="Save\nEdited", fg="white", bg="blue", width=10, bd=10, height=3, activebackground="white",
       activeforeground="blue", font=("Segoe Script", 13), command=save_edited).place(x=430, y=450)
# Create left buttons frame
LabelFrame(win, text="tools", labelanchor="n", relief="groove", bd=10, width=200, height=420,
           bg="#A2BAF5", font=("Segoe Script", 20, "bold")).place(x=10, y=50)
# Create right buttons frame
LabelFrame(win, text="tools", labelanchor="n", relief="groove", bd=10, width=200, height=420,
           bg="#A2BAF5", font=("Segoe Script", 20, "bold")).place(x=790, y=50)
# Create original frame
LabelFrame(win, text="Original", labelanchor="n", width=260, height=320, font=("Segoe Script", 20, "bold"), bg="#A2BAF5"
           , relief="groove", bd=10).place(x=220, y=120)
# Create edited frame
LabelFrame(win, text="Edited", labelanchor="n", width=260, height=320, font=("Segoe Script", 20, "bold"), bg="#A2BAF5",
           relief="groove", bd=10).place(x=520, y=120)
# Grayscale button
Button(win, text="Grayscale", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=greyscale).place(x=40, y=100)
# Canny button
Button(win, text="Canny", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=canny).place(x=40, y=170)
# Contours button
Button(win, text="Contours", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=contour).place(x=40, y=240)
# Detect color
Button(win, text="Detect Color", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=detect).place(x=40, y=310)
# Append
Button(win, text="Append", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=append).place(x=40, y=380)
# sharpen
Button(win, text="Sharpen", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=sharpen).place(x=820, y=120)
# Blur
Button(win, text="Blur", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=blur).place(x=820, y=200)
# date and time
Button(win, text="Date-Time", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=date_time).place(x=820, y=280)
# Clear Noise
Button(win, text="Clear Noise", fg="white", bg="blue", width=15, bd=8, height=2, activebackground="white",
       activeforeground="blue", font=("System", 5), command=clear_noise).place(x=820, y=360)

# Running the window
win.mainloop()
