from PIL import Image, ImageTk
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from lv2 import lv2_encode, lv2_decode
from lv3 import lv3_encode, lv3_decode
from lv4 import lv4_encode, lv4_decode
from lv5 import lv5_encode, lv5_decode

# Initialize global variables
current_directory = os.path.dirname(os.path.realpath(__file__))
image_file_path = current_directory + '/thumbs_up.bmp'  # Default image

def start():

    # Create the main window
    gui = tk.Tk()
    gui.title('Image Operations')
    gui['bg'] = 'SeaGreen1'

    # Create a frame for the layout
    frame = tk.Frame(gui)
    frame.grid(row=0, column=0, padx=15, pady=15)
    frame['bg'] = 'DodgerBlue4'

    # Create a sub-frame for the top-left part to hold the image
    image_frame = tk.Frame(frame)
    image_frame.grid(row=0, column=0, padx=10, pady=10)

    # Create a sub-frame for the bottom-left part (can add more content here)
    bottom_left_frame = tk.Frame(frame)
    bottom_left_frame.grid(row=1, column=0, padx=10, pady=10)

    # Create a sub-frame for the top-right part to hold the buttons
    button_frame = tk.Frame(frame)
    button_frame.grid(row=0, column=1, padx=10, pady=10)

    # Create a sub-frame for the bottom-right part (can add more content here)
    bottom_right_frame = tk.Frame(frame)
    bottom_right_frame.grid(row=1, column=1, padx=10, pady=10)

    # Display the initial image in the image frame (top-left part)
    gui_img = ImageTk.PhotoImage(file=image_file_path)
    gui_img_panel = tk.Label(image_frame, image=gui_img)
    gui_img_panel.grid(row=0, column=0, padx=10, pady=10)

    # Create buttons for image manipulation in the button frame (top-right part)
    btn1 = tk.Button(button_frame, text='Open File', width=15)
    btn1['command'] = lambda: open_image(gui_img_panel)
    btn1.grid(row=0, column=0)

    btn2 = tk.Button(button_frame, text='Grayscale', bg='gray', width=15)
    btn2['command'] = lambda: display_in_grayscale(gui_img_panel, bottom_left_frame)
    btn2.grid(row=1, column=0)

    btn3 = tk.Button(button_frame, text='Red', bg='red', width=15)
    btn3['command'] = lambda: display_color_channel(gui_img_panel, 'red', bottom_left_frame)
    btn3.grid(row=2, column=0)

    btn4 = tk.Button(button_frame, text='Green', bg='SpringGreen2', width=15)
    btn4['command'] = lambda: display_color_channel(gui_img_panel, 'green', bottom_left_frame)
    btn4.grid(row=3, column=0)

    btn5 = tk.Button(button_frame, text='Blue', bg='DodgerBlue2', width=15)
    btn5['command'] = lambda: display_color_channel(gui_img_panel, 'blue', bottom_left_frame)
    btn5.grid(row=4, column=0)

    # Create a multi-select drop-down list (OptionMenu)
    select_label = tk.Label(button_frame, text="Select Operations:")
    select_label.grid(row=5, column=0, padx=10, pady=10)

    options = [
        'lv1_encode', 'lv1_decode',
        'lv2_encode', 'lv2_decode',
        'lv3_encode', 'lv3_decode',
        'lv4_encode', 'lv4_decode',
        'lv5_encode', 'lv5_decode'
    ]

    selected_operations = tk.StringVar()
    selected_operations.set(options[0])  # defaul value

    select_menu = tk.OptionMenu(button_frame, selected_operations, *options)
    select_menu.grid(row=6, column=0, padx=10, pady=10)

    # Add a button to apply selected operation
    btn_apply = tk.Button(button_frame, text="Apply Selected", width=15,
                          command=lambda: apply_selected_operations(gui_img_panel, bottom_left_frame,
                                                                    selected_operations, bottom_right_frame))
    btn_apply.grid(row=7, column=0, padx=10, pady=10)

    # Start the GUI event loop
    gui.mainloop()

# Function for displaying the current image in grayscale and placing it in bottom-left frame
def display_in_grayscale(image_panel, bottom_left_frame):
    img_rgb = Image.open(image_file_path)
    img_grayscale = img_rgb.convert('L')
    img = ImageTk.PhotoImage(image=img_grayscale)

    # Remove previous image if exists in bottom_left_frame
    for widget in bottom_left_frame.winfo_children():
        widget.destroy()

    # Place the new grayscale image in the bottom-left frame
    img_panel = tk.Label(bottom_left_frame, image=img)
    img_panel.grid(row=0, column=0, padx=10, pady=10)
    img_panel.photo_ref = img

# Function for displaying a specific color channel of the image in bottom-left frame
def display_color_channel(image_panel, channel, bottom_left_frame):
    img_rgb = Image.open(image_file_path)
    img_array = np.array(img_rgb)

    if channel == 'red':
        img_array[:, :, 1:] = 0
    elif channel == 'green':
        img_array[:, :, [0, 2]] = 0
    elif channel == 'blue':
        img_array[:, :, :2] = 0

    img_rgb_channel = Image.fromarray(img_array)
    img = ImageTk.PhotoImage(image=img_rgb_channel)

    # Remove previous image if exists in bottom_left_frame
    for widget in bottom_left_frame.winfo_children():
        widget.destroy()

    # Place the new color channel image in the bottom-left frame
    img_panel = tk.Label(bottom_left_frame, image=img)
    img_panel.grid(row=0, column=0, padx=10, pady=10)
    img_panel.photo_ref = img

# Function to apply the selected operation
def apply_selected_operations(image_panel, bottom_left_frame, selected_operations, bottom_right_frane):
    selected_operation = selected_operations.get()

    # Remove previous image if exists in bottom_left_frame in changing opr
    for widget in bottom_left_frame.winfo_children():
        widget.destroy()

    for widget in bottom_right_frane.winfo_children():
        widget.destroy()

    if selected_operation == 'lv2_encode':
        # lv2.py encode func
        stats, out_path = lv2_encode(image_file_path)
        print(stats)  # follow with gui and terminal
        messagebox.showinfo('Info', 'lv2 encoding completed!')

        # add stats info
        stats_label = tk.Label(bottom_right_frane, text=f"Result:\n{stats}", justify=tk.LEFT, anchor="w")
        stats_label.grid(row=0, column=0, padx=10, pady=10)

        #  reading encode data to see
        with open(out_path, 'rb') as bin_file:
            bin_content = bin_file.read(512)  # some size opr

            # add  content of .bin file
            bin_content_label = tk.Text(bottom_left_frame, height=16, width=50)
            bin_content_label.grid(row=1, column=0, padx=10, pady=10)
            bin_content_label.insert(tk.END, f"\n{bin_content.hex()}")
            bin_content_label.config(state=tk.DISABLED)  # just show, can not change


    elif selected_operation == 'lv2_decode':
        # lv2.py decode func
        stats,img = lv2_decode(image_file_path)
        print(stats)  # follow gui and terminal
        messagebox.showinfo('Info', 'lv2 decoding completed!')

        img_tk=ImageTk.PhotoImage(img)

        img_panel = tk.Label(bottom_left_frame, image=img_tk)
        img_panel.grid(row=0, column=0, padx=10, pady=10)
        img_panel.image = img_tk

    elif selected_operation == 'lv3_encode':
        #
        stats, out_path = lv3_encode(image_file_path)
        print(stats)  #z
        messagebox.showinfo('Info', 'lv3 encoding completed!')

        #
        stats_label = tk.Label(bottom_right_frane, text=f"Stats:\n{stats}", justify=tk.LEFT, anchor="w")
        stats_label.grid(row=0, column=0, padx=10, pady=10)

        #
        with open(out_path, 'rb') as bin_file:
            bin_content = bin_file.read(512)  #

            #
            bin_content_label = tk.Text(bottom_left_frame, height=16, width=50)
            bin_content_label.grid(row=1, column=0, padx=10, pady=10)
            bin_content_label.insert(tk.END, f"\n{bin_content.hex()}")
            bin_content_label.config(state=tk.DISABLED)  # Sadece görüntüleme için, düzenlenemez hale getirelim.


    elif selected_operation == 'lv3_decode':
        #
        stats, img = lv3_decode(image_file_path)
        print(stats)  #
        messagebox.showinfo('Info', 'lv3 decoding completed!')

        img_tk = ImageTk.PhotoImage(img)

        img_panel = tk.Label(bottom_left_frame, image=img_tk)
        img_panel.grid(row=0, column=0, padx=10, pady=10)
        img_panel.image = img_tk
    elif selected_operation == 'lv4_encode':
        #
        stats, out_path = lv4_encode(image_file_path)
        print(stats)  #
        messagebox.showinfo('Info', 'lv4 encoding completed!')

        #
        stats_label = tk.Label(bottom_right_frane, text=f"Stats:\n{stats}", justify=tk.LEFT, anchor="w")
        stats_label.grid(row=0, column=0, padx=10, pady=10)

        #
        with open(out_path, 'rb') as bin_file:
            bin_content = bin_file.read(512)  # Sadece ilk 512 byte'ı oku

            #
            bin_content_label = tk.Text(bottom_left_frame, height=16, width=50)
            bin_content_label.grid(row=1, column=0, padx=10, pady=10)
            bin_content_label.insert(tk.END, f"\n{bin_content.hex()}")
            bin_content_label.config(state=tk.DISABLED)  # Sadece görüntüleme için, düzenlenemez hale getirelim.


    elif selected_operation == 'lv4_decode':
        #
        stats, img = lv4_decode(image_file_path)
        print(stats)  #
        messagebox.showinfo('Info', 'lv4 decoding completed!')

        img_tk = ImageTk.PhotoImage(img)

        img_panel = tk.Label(bottom_left_frame, image=img_tk)
        img_panel.grid(row=0, column=0, padx=10, pady=10)
        img_panel.image = img_tk

    elif selected_operation == 'lv5_encode':
        #
        stats, out_path = lv5_encode(image_file_path)
        print(stats)  #
        messagebox.showinfo('Info', 'lv5 encoding completed!')

        #
        stats_label = tk.Label(bottom_right_frane, text=f"Stats:\n{stats}", justify=tk.LEFT, anchor="w")
        stats_label.grid(row=0, column=0, padx=10, pady=10)

        #
        with open(out_path, 'rb') as bin_file:
            bin_content = bin_file.read(512)  # Sadece ilk 512 byte'ı oku

            #
            bin_content_label = tk.Text(bottom_left_frame, height=16, width=50)
            bin_content_label.grid(row=1, column=0, padx=10, pady=10)
            bin_content_label.insert(tk.END, f"\n{bin_content.hex()}")
            bin_content_label.config(state=tk.DISABLED)  # Sadece görüntüleme için, düzenlenemez hale getirelim.


    elif selected_operation == 'lv5_decode':
        #
        stats, img = lv5_decode(image_file_path)
        print(stats)  #
        messagebox.showinfo('Info', 'lv5 decoding completed!')

        img_tk = ImageTk.PhotoImage(img)

        img_panel = tk.Label(bottom_left_frame, image=img_tk)
        img_panel.grid(row=0, column=0, padx=10, pady=10)
        img_panel.image = img_tk

# Function for opening an image from a file
def open_image(image_panel):
    global image_file_path
    file_path = filedialog.askopenfilename(initialdir=current_directory,
                                           title='Choose image ( .bmp ) or .bin fle',
                                           filetypes=[('Image file', '*.bmp'),
                                                      ('Binary file', '*.bin'),
                                                      ('Whole file', '*.*')])
    if file_path == '':
        messagebox.showinfo('Warning', 'Nothing happened.')
    else:
        image_file_path = file_path
        print(f"Path of choose fle: {image_file_path}")  # every time each print for follow

        # check file .bmp or .bin
        if file_path.endswith('.bmp'):
            img = ImageTk.PhotoImage(file=image_file_path)
            image_panel.config(image=img)
            image_panel.photo_ref = img  # Resmi ekrana yerleştir

            # if choose before .bin file destroy
            for widget in image_panel.winfo_children():
                widget.destroy()

        elif file_path.endswith('.bin'):
            with open(file_path, 'rb') as bin_file:
                bin_content = bin_file.read(512)  # to see content of file
                bin_content_label = tk.Text(image_panel, height=16, width=50)
                bin_content_label.grid(row=0, column=0, padx=10, pady=10)
                bin_content_label.insert(tk.END, f"\n{bin_content.hex()}")
                bin_content_label.config(state=tk.DISABLED)

        else:
            messagebox.showinfo('Error', 'Not support file type.')

    return

# Start the application
if __name__ == '__main__':
    start()
