from level1 import *
from level2 import *
from level3 import *
from level4 import *
from level5 import *
import os
from PIL import *
from PIL import Image
import numpy as np
from tkinter import *
from PIL import ImageTk, Image
from tkinter import filedialog, messagebox
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

root = Tk()
root.title("Huffman Coding")
root.geometry('900x600')
root.resizable(False, False)

# Global variables
stats4_h, stats4_p, stats5_h, stats5_p = [], [], [], []

def display_in_grayscale(image_panel, fname):
    img_rgb = Image.open(fname)

    img_grayscale = img_rgb.convert('L')
    print('\nFor the color image')
    print('----------------------------------------------------------------------')
    width, height = img_rgb.size
    print('the width in pixels:', width, 'and the height in pixels:', height)
    img_rgb_array = pil_to_np(img_rgb)
    print('the dimensions of the image array:', img_rgb_array.shape)
    print('\nFor the grayscale image')
    print('----------------------------------------------------------------------')
    width, height = img_grayscale.size
    print('the width in pixels:', width, 'and the height in pixels:', height)
    img_grayscale_array = pil_to_np(img_grayscale)
    print('the dimensions of the image array:', img_grayscale_array.shape)

    img_resize = img_grayscale.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(image=img_resize)
    image_panel.config(image=img)
    image_panel.photo_ref = img


# Function for displaying a given color channel of the current image
# -------------------------------------------------------------------------------
def display_color_channel(image_panel, channel, fname):
    # red channel -> 0, green channel -> 1 and blue channel -> 2
    if channel == 'red':
        channel_index = 0
    elif channel == 'green':
        channel_index = 1
    else:
        channel_index = 2
    # open the current image as a PIL image
    img_rgb = Image.open(fname)
    # convert the current image to a numpy array
    image_array = pil_to_np(img_rgb)
    # traverse all the pixels in the image array
    n_rows = image_array.shape[0]
    n_cols = image_array.shape[1]
    for row in range(n_rows):
        for col in range(n_cols):
            # make all the values 0 for the color channels except the given channel
            for rgb in range(3):
                if (rgb != channel_index):
                    image_array[row][col][rgb] = 0
    # convert the modified image array (numpy) to a PIL image
    pil_img = np_to_pil(image_array)
    # modify the displayed image
    img_resize = pil_img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(image=img_resize)
    image_panel.config(image=img)
    image_panel.photo_ref = img


def pil_to_np(img):
    img_array = np.array(img)
    return img_array

def np_to_pil(img_array):
    img = Image.fromarray(np.uint8(img_array))
    #img.show()
    return img

def open_img(outpath, cordx, cordy):
    img = Image.open(outpath)
    img = img.resize((200, 200), Image.LANCZOS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.place(x=cordx, y=cordy)
    return panel
# File selection
def selectFile(event):
    if file_clicked.get() == "Image Compression":
        global fname, gui_img_panel
        fname = filedialog.askopenfilename(
            initialdir="/",
            title="Select A File",
            filetypes=(("jpg files", "*.jpg"), ("all files", "*.*"))
        )
        if fname:
            Label(root, text="Original Image", font=('Arial bold', 11)).place(x=170, y=200)
            gui_img_panel = open_img(fname, 120, 230)
            color_buttons = [
                ('Grayscale', 'gray', lambda: display_in_grayscale(gui_img_panel, fname), 120),
                ('Red', 'red', lambda: display_color_channel(gui_img_panel, 'red', fname), 200),
                ('Green', 'SpringGreen2', lambda: display_color_channel(gui_img_panel, 'green', fname), 280),
                ('Blue', 'DodgerBlue2', lambda: display_color_channel(gui_img_panel, 'blue', fname), 360)
            ]
            for text, color, command, x in color_buttons:
                Button(root, text=text, bg=color, width=10, command=command).place(x=x, y=500)
        print("Image Comp.")

    elif file_clicked.get() == "Text File Compression":
        global text_filename
        text_filename = filedialog.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=(('text files', '*.txt'), ('All files', '*.*'))
        )
        if text_filename:
            messagebox.showinfo('Selected File', text_filename)
    else:
        print("Error")



def printStatistics(func_name, huffman_encoding, problist, data):
    def display_output(stat_func, y_start):
        mv = 0
        for i, j, k in zip(huffman_encoding, problist, data):
            output = stat_func(i, j, k)
            tk.Label(root, text=output, font=("Arial", 11)).place(x=460, y=y_start + mv)
            mv += 35
    
    tk.Label(root, text="Comparison", font=('Arial bold', 11)).place(x=560, y=50)
    y_start = 80

    stat_funcs = {
        "statistics1": statistics1,
        "statistics2": statistics2,
        "statistics3": statistics3
    }

    if func_name in stat_funcs:
        output = stat_funcs[func_name](huffman_encoding, problist, data)
        print("output: ", output)
        tk.Label(root, text=output, font=("Arial", 11)).place(x=460, y=y_start)
    elif func_name in ["statistics4", "statistics5"]:
        stat_func = statistics4 if func_name == "statistics4" else statistics5
        display_output(stat_func, y_start)
    else:
        tk.Label(root, text="Error", font=("Arial", 11)).place(x=460, y=y_start)
        print("Error")

# Decompression display
def showDecompressFile(func_name, decoded_output, arr):
    if func_name.startswith("saveDecompressedFile"):
        Label(root, text="Decompressed Image", font=('Arial bold', 11)).place(x=530, y=200)
        outpath = globals().get(func_name)(decoded_output, arr)
        if outpath:
            open_img(outpath, 500, 230)
            Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=250, y=100)
    else:
        print("Error")

# Compression function
def compress_func(func_name, data, total_element, index):
    global encoding, tree, huffman_encoding, prob_list, outpath
    compression_functions = {
        "compress1": (Huffman_Encoding1, compress1),
        "compress2": (Huffman_Encoding2, compress2),
        "compress3": (Huffman_Encoding3, compress3),
        "compress4": (Huffman_Encoding4, compress4),
        "compress5": (Huffman_Encoding5, compress5)
    }
    encoding_func, compress_func = compression_functions.get(func_name)
    if encoding_func:
        ''' 
        global string1, tree1, encodingCodes1, prob_list1,encoding2, tree2, huffman_encoding2, problist2,encoding3, tree3, huffman_encoding3, problist3
        string1, tree1, encodingCodes1, prob_list1 = Huffman_Encoding1(data)
        encoding2, tree2, huffman_encoding2, problist2 = Huffman_Encoding2(data, total_element)
        encoding3, tree3, huffman_encoding3, problist3 = Huffman_Encoding3(data, total_element)
        '''
        encoding, tree, huffman_encoding, prob_list = encoding_func(data, total_element if 'total_element' in locals() else 0)
        outpath = compress_func(encoding)
        globals()[f"outpath{func_name[-1]}"] = outpath
        globals()[f"encoding{func_name[-1]}"] = encoding
        globals()[f"tree{func_name[-1]}"] = tree
        globals()[f"huffman_encoding{func_name[-1]}"] = huffman_encoding
        globals()[f"prob_list{func_name[-1]}"] = prob_list
        Label(root, text="Encoding data is saved", font=('Arial bold', 11)).place(x=250, y=60)
        if func_name.startswith("compress4") or func_name.startswith("compress5"):
            if index in {1, 2, 3}:
                stats = stats4_h if func_name == "compress4" else stats5_h
                prob_stats = stats4_p if func_name == "compress4" else stats5_p
                stats.append(huffman_encoding.copy())
                prob_stats.append(prob_list)
    else:
        print("Error")

def decompress_func(func_name, arr, index):
    def handle_decompression(func, encoding, tree, outpath, arr, output_array):
        decoded_data, output = func(encoding, tree, outpath, arr)
        output_array[:] = np.array(output)
        return decoded_data

    def display_decoded_data(decoded_output, label_positions):
        Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=label_positions[0], y=label_positions[1])
        Label(root, text="Decoded Data", font=('Arial bold', 11)).place(x=label_positions[0], y=label_positions[2])
        Label(root, text=decoded_output, font=('Arial bold', 11)).place(x=label_positions[0], y=label_positions[3])

    global output_r_array, output_g_array, output_b_array, output_r_array_5, output_g_array_5, output_b_array_5
    global total_list, total_list_5

    if func_name == "decompress1":
        decoded_output1 = Huffman_Decoding1(encoding, tree, outpath)
        saveDecompressedFile1(decoded_output1)
        display_decoded_data(decoded_output1, [250, 100, 300, 340])

    elif func_name == "decompress2":
        decoded_output = Huffman_Decoding2(encoding, tree, outpath, arr)
        showDecompressFile("saveDecompressedFile2", decoded_output, arr)

    elif func_name == "decompress3":
        decoded_output = Huffman_Decoding3(encoding, tree, outpath, arr)
        showDecompressFile("saveDecompressedFile3", decoded_output, arr)

    elif func_name == "decompress4":
        nrows, ncols = arr.shape
        if index == 1:
            handle_decompression(Huffman_Decoding4, encoding, tree, outpath, arr, output_r_array)
            total_list.append(output_r_array)

        elif index == 2:
            handle_decompression(Huffman_Decoding4, encoding, tree, outpath, arr, output_g_array)
            total_list.append(output_g_array)

        elif index == 3:
            handle_decompression(Huffman_Decoding4, encoding, tree, outpath, arr, output_b_array)
            total_list.append(output_b_array)

        if len(total_list) == 3:
            decode_r = Image.fromarray(output_r_array.reshape(nrows, ncols)).convert('L')
            decode_g = Image.fromarray(output_g_array.reshape(nrows, ncols)).convert('L')
            decode_b = Image.fromarray(output_b_array.reshape(nrows, ncols)).convert('L')
            final_img = Image.merge("RGB", (decode_r, decode_g, decode_b))
            showDecompressFile("saveDecompressedFile4", final_img, arr)
        else:
            print("Error: Incomplete color channels for decompression 4")

    elif func_name == "decompress5":
        nrows, ncols = arr.shape
        if index == 1:
            handle_decompression(Huffman_Decoding5, encoding, tree, outpath, arr, output_r_array_5)
            total_list_5.append(output_r_array_5)

        elif index == 2:
            handle_decompression(Huffman_Decoding5, encoding, tree, outpath, arr, output_g_array_5)
            total_list_5.append(output_g_array_5)

        elif index == 3:
            handle_decompression(Huffman_Decoding5, encoding, tree, outpath, arr, output_b_array_5)
            total_list_5.append(output_b_array_5)

        if len(total_list_5) == 3:
            decode_r_5 = Image.fromarray(output_r_array_5.reshape(nrows, ncols)).convert('L')
            decode_g_5 = Image.fromarray(output_g_array_5.reshape(nrows, ncols)).convert('L')
            decode_b_5 = Image.fromarray(output_b_array_5.reshape(nrows, ncols)).convert('L')
            final_img_2 = Image.merge("RGB", (decode_r_5, decode_g_5, decode_b_5))
            showDecompressFile("saveDecompressedFile5", final_img_2, arr)
        else:
            print("Error: Incomplete color channels for decompression 5")

    else:
        print("Error: Invalid decompression function name")

def compress_decompress(func_name, r, g, b, arr, total_element):
    color_list = [r, g, b]
    if func_name in ["compress4", "compress5"]:
        for index, color in enumerate(color_list, start=1):
            compress_func(func_name, color, total_element, index)
            decompress_func(f"decompress{func_name[-1]}", arr, index)
            # Optional: printStatistics("statistics4" or "statistics5", huffman_encoding4 or huffman_encoding5, problist4 or problist5, color)
    else:
        print("Error: Invalid compression function name")



# Method selection
def selectMethod(event):
    method = clicked.get()
    if method == "Level 1":
        data = readFile(text_filename)
        Button(root, text="Compressed", width=10, command=lambda: compress_func("compress1", data, 0, 0)).grid(row=1, column=7)
        Button(root, text="Decompressed", width=10, command=lambda: decompress_func("decompress1", 0, 0)).grid(row=1, column=8)
        Button(root, text="Comparison", width=10, command=lambda: printStatistics("statistics1", huffman_encoding, prob_list, data)).grid(row=1, column=9)
    elif method == "Level 2":
        data, total_element, arr = readPILimg(fname)
        Button(root, text="Compressed", width=10, command=lambda: compress_func("compress2", data, total_element, 0)).grid(row=1, column=7)
        Button(root, text="Decompressed", width=10, command=lambda: decompress_func("decompress2", arr, 0)).grid(row=1, column=8)
        Button(root, text="Comparison", width=10, command=lambda: printStatistics("statistics2", huffman_encoding, prob_list, data)).grid(row=1, column=9)
    elif method == "Level 3":
        diff_arr3, total_element, arr = readPILimg3(fname)
        Button(root, text="Compressed", width=10, command=lambda: compress_func("compress3", diff_arr3, total_element, 0)).grid(row=1, column=7)
        Button(root, text="Decompressed", width=10, command=lambda: decompress_func("decompress3", arr, 0)).grid(row=1, column=8)
        Button(root, text="Comparison", width=10, command=lambda: printStatistics("statistics3", huffman_encoding, prob_list, diff_arr3)).grid(row=1, column=9)
    elif method == "Level 4":
        img, r, g, b, arr, total_element = readPILimg4(fname)
        global r_4, g_4, b_4, arr_4
        r_4, g_4, b_4, arr_4 = r, g, b, arr
        Button(root, text="Compressed", width=10, command=lambda: compress_decompress("compress4", r, g, b, arr, total_element)).grid(row=1, column=7)
        Button(root, text="Decompressed", width=10, command=lambda: decompress_func("decompress4", arr_4, 0)).grid(row=1, column=8)
        Button(root, text="Comparison", width=10, command=lambda: printStatistics("statistics4", stats4_h, stats4_p, r)).grid(row=1, column=9)
    elif method == "Level 5":
        img, r, g, b, arr, total_element = readPILimg5(fname)
        global r_5, g_5, b_5, arr_5
        r_5, g_5, b_5, arr_5 = r, g, b, arr
        Button(root, text="Compressed", width=10, command=lambda: compress_decompress("compress5", r, g, b, arr, total_element)).grid(row=1, column=7)
        Button(root, text="Decompressed", width=10, command=lambda: decompress_func("decompress5", arr_5, 0)).grid(row=1, column=8)
        Button(root, text="Comparison", width=10, command=lambda: printStatistics("statistics5", stats5_h, stats5_p, r)).grid(row=1, column=9)
    else:
        print("Error")


def update_method_options(selected_file_type):
    if selected_file_type == "Image Compression":
        method_options = ["Level 2", "Level 3", "Level 4", "Level 5"]
    elif selected_file_type == "Text File Compression":
        method_options = ["Level 1"]
    clicked.set(method_options[0])  # Set default to the first option
    method_menu["menu"].delete(0, "end")
    for option in method_options:
        method_menu["menu"].add_command(label=option, command=tk._setit(clicked, option))

def on_file_option_change(*args):
    selected_file_type = file_clicked.get()
    update_method_options(selected_file_type)


file_clicked = StringVar()
file_clicked.set("Text File Compression")
file_menu = OptionMenu(root, file_clicked, "Image Compression", "Text File Compression", command=on_file_option_change)
file_menu.grid(row=0, column=0)

clicked = StringVar()
clicked.set("Level 1")
method_menu = OptionMenu(root, clicked, "Level 1")  # Initial option
method_menu.grid(row=0, column=1)

# Call on_file_option_change to initialize method menu options
on_file_option_change()

Button(root, text="Select File", width=10, command=lambda: selectFile(None)).grid(row=0, column=2)
Button(root, text="Select Method", width=10, command=lambda: selectMethod(None)).grid(row=0, column=3)

root.mainloop()
