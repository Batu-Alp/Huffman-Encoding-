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
root.resizable(False, False)
root.geometry('900x600')

global stats4_h, stats4_p, stats5_h, stats5_p
stats4_h = []
stats4_p = []
stats5_h = []
stats5_p = []

def selectFile(event):
    if file_clicked.get() == "Image Compression":

        global fname
        global gui_img_panel

        root.filename = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
        fname = root.filename
        original_image_label = Label(root, text="Original Image", font=('Arial bold', 11)).place(x=170, y=200)
        gui_img_panel = open_img(fname, 120, 230)

        btn2 = tk.Button(root, text='Grayscale', bg='gray', width=10,
                         command=lambda: display_in_grayscale(gui_img_panel, fname))
        btn2.place(x=120, y=500)

        btn3 = tk.Button(root, text='Red', bg='red', width=10,
                         command=lambda: display_color_channel(gui_img_panel, 'red', fname))
        btn3.place(x=200, y=500)

        btn4 = tk.Button(root, text='Green', bg='SpringGreen2', width=10,
                         command=lambda: display_color_channel(gui_img_panel, 'green', fname))
        btn4.place(x=280, y=500)

        btn5 = tk.Button(root, text='Blue', bg='DodgerBlue2', width=10,
                         command=lambda: display_color_channel(gui_img_panel, 'blue', fname))
        btn5.place(x=360, y=500)

        print("Image Comp.")


    elif file_clicked.get() == "Text File Compression":

        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        global text_filename

        text_filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)

        showinfo(
            title='Selected File',
            message=text_filename
        )

    else:
        print("Error")


def printStatistics(func_name, huffman_encoding, problist, data):
    if func_name == "statistics1":
        original_image_label = Label(root, text="Comparison", font=('Arial bold', 11)).place(x=560, y=50)
        output = statistics1(huffman_encoding, problist, data)
        label_output = tk.Label(text=output, font=("Arial", 11)).place(x=460, y=80)

    elif func_name == "statistics2":
        original_image_label = Label(root, text="Comparison", font=('Arial bold', 11)).place(x=560, y=50)
        output = statistics2(huffman_encoding, problist, data)
        label_output = tk.Label(text=output, font=("Arial", 11)).place(x=460, y=80)

    elif func_name == "statistics3":
        original_image_label = Label(root, text="Comparison", font=('Arial bold', 11)).place(x=560, y=50)
        output = statistics3(huffman_encoding, problist, data)
        label_output = tk.Label(text=output, font=("Arial", 11)).place(x=460, y=80)

    elif func_name == "statistics4":
        original_image_label = Label(root, text="Comparison", font=('Arial bold', 11)).place(x=560, y=50)
        mv = 0
        #for i in stats4_h:
        for i, j, k in zip(huffman_encoding, problist, data):
            output = statistics4(i, j, k)
            label_output = tk.Label(text=output, font=("Arial", 11)).place(x=460, y=80 + mv)
            mv += 35

    elif func_name == "statistics5":
        original_image_label = Label(root, text="Comparison", font=('Arial bold', 11)).place(x=560, y=50)
        mv = 0
        for i, j, k in zip(huffman_encoding, problist, data):
            output = statistics5(i, j, k)
            label_output = tk.Label(text=output, font=("Arial", 11)).place(x=460, y=80 + mv)
            mv += 35


    else:
        label_output = tk.Label(text="Error", font=("Arial", 11)).place(x=460, y=80)
        print("Error")


def showDecompressFile(func_name, decoded_output, arr):
    if func_name == "saveDecompressedFile1":
        pass

    elif func_name == "saveDecompressedFile2":
        original_image_label = Label(root, text="Decompressed Image", font=('Arial bold', 11)).place(x=530, y=200)
        outpath = saveDecompressedFile2(decoded_output, arr)
        open_img(outpath, 500, 230)
        decoding_data_saved = Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=250, y=100)

    elif func_name == "saveDecompressedFile3":
        original_image_label = Label(root, text="Decompressed Image", font=('Arial bold', 11)).place(x=530, y=200)
        outpath = saveDecompressedFile3(decoded_output, arr)
        open_img(outpath, 500, 230)
        decoding_data_saved = Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=250, y=100)

    elif func_name == "saveDecompressedFile4":
        original_image_label = Label(root, text="Decompressed Image", font=('Arial bold', 11)).place(x=530, y=200)
        outpath = saveDecompressedFile4(decoded_output, arr)
        open_img(outpath, 500, 230)
        decoding_data_saved = Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=250, y=100)

    elif func_name == "saveDecompressedFile5":
        original_image_label = Label(root, text="Decompressed Image", font=('Arial bold', 11)).place(x=530, y=200)
        outpath = saveDecompressedFile5(decoded_output, arr)
        open_img(outpath, 500, 230)
        decoding_data_saved = Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=250, y=100)

    else:
        print("Error")


def compress_func(func_name, data, total_element, index):

    if func_name == "compress1":
        global outpath1, string1, tree1, encodingCodes1, prob_list1
        string1, tree1, encodingCodes1, prob_list1 = Huffman_Encoding1(data)
        outpath1 = compress1(string1)
        encoding_data_saved = Label(root, text="Encoding data is saved", font=('Arial bold', 11)).place(x=250, y=60)
        encoding_data_saved = Label(root, text="Encoded Data ", font=('Arial bold', 11)).place(x=250, y=200)
        encoding_data_saved = Label(root, text=string1, font=('Arial bold', 11)).place(x=250, y=240)

    elif func_name == "compress2":
        global outpath2, encoding2, tree2, huffman_encoding2, problist2
        encoding2, tree2, huffman_encoding2, problist2 = Huffman_Encoding2(data, total_element)
        outpath2 = compress2(encoding2)
        encoding_data_saved = Label(root, text="Encoding data is saved", font=('Arial bold', 11)).place(x=250, y=60)

    elif func_name == "compress3":
        global outpath3, encoding3, tree3, huffman_encoding3, problist3
        encoding3, tree3, huffman_encoding3, problist3 = Huffman_Encoding3(data, total_element)
        outpath3 = compress3(encoding3)
        encoding_data_saved = Label(root, text="Encoding data is saved", font=('Arial bold', 11)).place(x=250, y=60)

    elif func_name == "compress4":
        global outpath4, encoding4, tree4, huffman_encoding4, problist4
        encoding4, tree4, huffman_encoding4, problist4 = Huffman_Encoding4(data, total_element)

        if (index == 1):
            outpath4 = compress4(encoding4, "r")
            stats4_h.append(huffman_encoding4.copy())
            stats4_p.append(problist4)
            #printStatistics("statistics4", huffman_encoding4, problist4, r_4)

        elif (index == 2):
            outpath4 = compress4(encoding4, "g")
            stats4_h.append(huffman_encoding4.copy())
            stats4_p.append(problist4)            #
            #printStatistics("statistics4", huffman_encoding4, problist4, g_4)


        elif (index == 3):
            outpath4 = compress4(encoding4, "b")
            stats4_h.append(huffman_encoding4.copy())
            stats4_p.append(problist4)
            #printStatistics("statistics4", huffman_encoding4, problist4, b_4)


        else:
            print("Error in compress func.")
        encoding_data_saved = Label(root, text="Encoding data is saved", font=('Arial bold', 11)).place(x=250, y=60)


    elif func_name == "compress5":

        global outpath5, encoding5, tree5, huffman_encoding5, problist5
        encoding5, tree5, huffman_encoding5, problist5 = Huffman_Encoding5(data, total_element)

        if (index == 1):
            outpath5 = compress5(encoding5, "r")
            stats5_h.append(huffman_encoding5.copy())
            stats5_p.append(problist5)

        elif (index == 2):
            outpath5 = compress5(encoding5, "g")
            stats5_h.append(huffman_encoding5.copy())
            stats5_p.append(problist5)

        elif (index == 3):
            outpath5 = compress5(encoding5, "b")
            stats5_h.append(huffman_encoding5.copy())
            stats5_p.append(problist5)

        else:
            print("Error in compress func.")

        encoding_data_saved = Label(root, text="Encoding data is saved", font=('Arial bold', 11)).place(x=250, y=60)


    else:
        print("Error")

global total_list, total_list_5
total_list = []
total_list_5 = []


def decompress_func(func_name, arr, index):
    global array_rgb, output_r_array, output_g_array, output_b_array

    if func_name == "decompress1":
        decoded_output1 = Huffman_Decoding1(string1, tree1, outpath1)
        saveDecompressedFile1(decoded_output1)
        decoding_data_saved1 = Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=250, y=100)
        decoding_data_saved2 = Label(root, text="Decoded Data", font=('Arial bold', 11)).place(x=250, y=300)
        decoding_data_saved3 = Label(root, text= decoded_output1, font=('Arial bold', 11)).place(x=250, y=340)

    elif func_name == "decompress2":
        # global decoded_output
        decoded_output = Huffman_Decoding2(encoding2, tree2, outpath2, arr)
        showDecompressFile("saveDecompressedFile2", decoded_output, arr)

    elif func_name == "decompress3":
        decoded_output = Huffman_Decoding3(encoding3, tree3, outpath3, arr)
        showDecompressFile("saveDecompressedFile3", decoded_output, arr)

    elif func_name == "decompress4":

        (nrows, ncols) = arr.shape
        if (index == 1):
            decoded_data_r, output_r = Huffman_Decoding4(encoding4, tree4, outpath4, arr)
            total_list.append(output_r)
            output_r_array = np.array(output_r)
            #printStatistics(func_name, huffman_encoding, problist, data)
            #btn_comparison = Button(root, text="Comparison", width=10,command=lambda: printStatistics("statistics4", huffman_encoding4, problist4,r)).grid(row=1, column=11)


        elif (index == 2):
            decoded_data_g, output_g = Huffman_Decoding4(encoding4, tree4, outpath4, arr)
            total_list.append(output_g)
            output_g_array = np.array(output_g)


        elif (index == 3):
            decoded_data_b, output_b = Huffman_Decoding4(encoding4, tree4, outpath4, arr)
            total_list.append(output_b)
            output_b_array = np.array(output_b)

        elif (len(total_list) == 3):

            decode_r = Image.fromarray(output_r_array.reshape(nrows, ncols)).convert('L')
            decode_g = Image.fromarray(output_g_array.reshape(nrows, ncols)).convert('L')
            decode_b = Image.fromarray(output_b_array.reshape(nrows, ncols)).convert('L')
            final_img = Image.merge("RGB", (decode_r, decode_g, decode_b))  # Second argument is a tuple
            showDecompressFile("saveDecompressedFile4", final_img, arr)


        else:
            print("There is a mistake")

    elif func_name == "decompress5":

        (nrows, ncols) = arr.shape
        global output_r_array_5, output_g_array_5, output_b_array_5

        if (index == 1):
            decoded_data_r, output_r_5 = Huffman_Decoding5(encoding5, tree5, outpath5, arr)
            total_list_5.append(output_r_5)
            output_r_array_5 = np.array(output_r_5)

        elif (index == 2):
            decoded_data_g, output_g_5 = Huffman_Decoding5(encoding5, tree5, outpath5, arr)
            total_list_5.append(output_g_5)
            output_g_array_5 = np.array(output_g_5)

        elif (index == 3):
            decoded_data_b, output_b_5 = Huffman_Decoding5(encoding5, tree5, outpath5, arr)
            total_list_5.append(output_b_5)
            output_b_array_5 = np.array(output_b_5)

        elif (len(total_list_5) == 3):

            decode_r_5 = Image.fromarray(output_r_array_5.reshape(nrows, ncols)).convert('L')
            decode_g_5 = Image.fromarray(output_g_array_5.reshape(nrows, ncols)).convert('L')
            decode_b_5 = Image.fromarray(output_b_array_5.reshape(nrows, ncols)).convert('L')

            final_img_2 = Image.merge("RGB", (decode_r_5, decode_g_5, decode_b_5))  # Second argument is a tuple

            showDecompressFile("saveDecompressedFile5", final_img_2, arr)

        else:
            print("There is a mistake")

    else:
        print("Error")


def compress_decompress(func_name, r, g, b, arr, total_element):

    color_list = [r, g, b]
    if func_name == "compress4":
        for index, i in enumerate(color_list, start = 1):
            compress_func("compress4", i, total_element, index)
            decompress_func("decompress4", arr, index)
            #printStatistics("statistics4", huffman_encoding4, problist4, i)

    elif func_name == "compress5":
        for index, i in enumerate(color_list, start = 1):
            compress_func("compress5", i, total_element, index)
            decompress_func("decompress5", arr, index)
            #printStatistics("statistics5", huffman_encoding4, problist4, i)

    else:
        print("Error")



def selectMethod(event):

    if clicked.get() == "Level 1":
        data = readFile(text_filename)
        btn_compressed = Button(root, text="Compressed", width=10,
                                command=lambda: compress_func("compress1", data, 0, 0)).grid(row=1, column=7)
        btn_decompressed = Button(root, text="Decompressed", width=10,
                                  command=lambda: decompress_func("decompress1", 0, 0)).grid(row=1, column=8)
        btn_comparison = Button(root, text="Comparison", width=10,
                                command=lambda: printStatistics("statistics1", encodingCodes1, prob_list1, data)).grid(
            row=1, column=9)

    elif clicked.get() == "Level 2":
        data, total_element, arr = readPILimg(fname)
        btn_compressed = Button(root, text="Compressed", width=10,
                                command=lambda: compress_func("compress2", data, total_element, 0)).grid(row=1,
                                                                                                         column=7)
        btn_showdecompressedımg = Button(root, text="Decompressed", width=10,
                                         command=lambda: decompress_func("decompress2", arr, 0)).grid(row=1, column=8)
        btn_comparison = Button(root, text="Comparison", width=10,
                                command=lambda: printStatistics("statistics2", huffman_encoding2, problist2,
                                                                data)).grid(row=1, column=9)

    elif clicked.get() == "Level 3":
        diff_arr3, total_element, arr = readPILimg3(fname)
        btn_compressed = Button(root, text="Compressed", width=10,
                                command=lambda: compress_func("compress3", diff_arr3, total_element, 0)).grid(row=1,
                                                                                                              column=7)
        btn_decompressed = Button(root, text="Decompressed", width=10,
                                  command=lambda: decompress_func("decompress3", arr, 0)).grid(row=1, column=8)
        btn_comparison = Button(root, text="Comparison", width=10,
                                command=lambda: printStatistics("statistics3", huffman_encoding3, problist3,
                                                                diff_arr3)).grid(row=1, column=9)

    elif clicked.get() == "Level 4":

        img, r, g, b, arr, total_element = readPILimg4(fname)
        global r_4, g_4, b_4

        r_4 = np.array(r).flatten().tolist()
        g_4 = np.array(g).flatten().tolist()
        b_4 = np.array(b).flatten().tolist()

        array_rgb = [r_4,g_4,b_4]

        btn_compressed = Button(root, text="Compress - Decompressed", width=20,
                                  command=lambda: compress_decompress("compress4",r_4, g_4, b_4, arr, total_element)).grid(row=1, column=9)
        btn_decompressed = Button(root, text="Decompressed", width=10,
                                  command=lambda: decompress_func("decompress4", arr, 0)).grid(row=1, column=10)
        btn_comparison = Button(root, text="Comparison", width=10,command=lambda: printStatistics("statistics4", stats4_h, stats4_p,array_rgb)).grid(row=1, column=11)


    elif clicked.get() == "Level 5":

        img, r, g, b, arr, total_element = readPILimg5(fname)

        r = np.array(r)
        g = np.array(g)
        b = np.array(b)

        diff_r = difference5(arr, r)
        diff_g = difference5(arr, g)
        diff_b = difference5(arr, b)


        array_rgb = [diff_r,diff_g,diff_b]

        btn_decompressed = Button(root, text="Compress - Decompressed", width=20,
                                  command=lambda: compress_decompress("compress5",diff_r, diff_g, diff_b, arr, total_element)).grid(row=1, column=10)

        btn_decompressed = Button(root, text="Decompressed", width=10,
                                  command=lambda: decompress_func("decompress5", arr, 0)).grid(row=1, column=11)

        btn_comparison = Button(root, text="Comparison", width=10,
                            command=lambda: printStatistics("statistics5", stats5_h, stats5_p,
                                                            array_rgb)).grid(row=1, column=12)

    else:
        print("Error")


def open_image(image_panel):
    global image_file_path  # to modify the global variable image_file_path
    # get the path of the image file selected by the user
    file_path = filedialog.askopenfilename(initialdir=current_directory,
                                           title='Select an image file',
                                           filetypes=(('jpg files', '*.jpg'),
                                                      ("all files", "*.*")))

    if file_path == '':
        messagebox.showinfo('Warning', 'No image file is selected/opened.')
    else:
        image_file_path = file_path
        img = ImageTk.PhotoImage(file=image_file_path)
        image_panel.config(image=img)
        image_panel.photo_ref = img

    return image_file_path


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

    img_resize = img_grayscale.resize((200, 200), Image.ANTIALIAS)
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
    img_resize = pil_img.resize((200, 200), Image.ANTIALIAS)
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


file_options = ["Image Compression", "Text File Compression"]
file_clicked = StringVar()
file_clicked.set("File")
file_menu = OptionMenu(root, file_clicked, *file_options, command=selectFile)
file_menu.grid(row=1, column=2, pady=20)

options = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
clicked = StringVar()
clicked.set("Methods")
methods = OptionMenu(root, clicked, *options, command=selectMethod).grid(row=1, column=6, pady=20)


def open_img(outpath, cordx, cordy):
    img = Image.open(outpath)
    img = img.resize((200, 200), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    panel = Label(root, image=img)
    panel.image = img
    panel.place(x=cordx, y=cordy)
    return panel


def compress():
    pass


root.mainloop()
