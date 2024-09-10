import numpy as np
import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
import heapq
import pickle
import zlib
import os
from level1 import *
from level2 import *
from level3 import *
from level4 import *
from level5 import *
from PIL import Image, ImageTk
from tkinter import filedialog, messagebox, StringVar, Label, Button, OptionMenu
from collections import Counter, defaultdict


class HuffmanCodingApp:
    def __init__(self, root):
        self.image_stats = {}
        self.root = root
        self.root.title("Huffman Coding")
        self.root.resizable(False, False)
        self.root.geometry('900x600')

        self.setup_ui()
        self.reset()
    
    def setup_ui(self):
        self.file_clicked = StringVar()
        self.file_clicked.set("File")
        file_options = ["Image Compression", "Text File Compression"]
        file_menu = OptionMenu(self.root, self.file_clicked, *file_options, command=self.select_file)
        file_menu.grid(row=1, column=2, pady=20)

        self.clicked = StringVar()
        self.clicked.set("Methods")
        options = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]
        methods = OptionMenu(self.root, self.clicked, *options, command=self.select_method)
        methods.grid(row=1, column=6, pady=20)

        self.file_label = Label(self.root, text="Select a file", font=('Arial bold', 11))
        self.file_label.grid(row=2, column=2, columnspan=4)

        self.img_panel = Label(self.root)
        self.img_panel.grid(row=2, column=6, columnspan=4, rowspan=4)

    def reset(self):
        self.fname = None
        self.text_filename = None
        self.stats4_h = []
        self.stats4_p = []
        self.stats5_h = []
        self.stats5_p = []

    def select_file(self, event):
        if self.file_clicked.get() == "Image Compression":
            self.fname = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                                   filetypes=(("jpg files", "*.jpg"), ("all files", "*.*")))
            
            fname = self.fname
            original_image_label = Label(self.root, text="Original Image", font=('Arial bold', 11)).place(x=170, y=200)
            gui_img_panel = self.display_image(fname, 120, 230)
            self.setup_image_buttons(gui_img_panel)
            ''' 
            if self.fname:
                self.display_image(self.fname,120,130)
                self.setup_image_buttons()
            '''
        elif self.file_clicked.get() == "Text File Compression":
            self.text_filename = filedialog.askopenfilename(title='Open a file',
                                                            initialdir='/',
                                                            filetypes=[('text files', '*.txt'), ('All files', '*.*')])
            if self.text_filename:
                messagebox.showinfo(title='Selected File', message=self.text_filename)

    def display_image(self,outpath, cordx, cordy):
        img = Image.open(outpath)
        img = img.resize((200, 200), Image.LANCZOS)
        img = ImageTk.PhotoImage(img)
        panel = Label(self.root, image=img)
        panel.image = img
        panel.place(x=cordx, y=cordy)
        return panel

    def setup_image_buttons(self, gui_img_panel):
        buttons = [
            ("Grayscale", 'gray', 120, 500, lambda: self.display_in_grayscale(gui_img_panel)),
            ("Red", 'red', 200, 500, lambda: self.display_color_channel('red')),
            ("Green", 'SpringGreen2', 280, 500, lambda: self.display_color_channel('green')),
            ("Blue", 'DodgerBlue2', 360, 500, lambda: self.display_color_channel('blue'))
        ]
        for text, bg, x, y, command in buttons:
            Button(self.root, text=text, bg=bg, width=10, command=command).place(x=x, y=y)

    def display_in_grayscale(self, fname):
        img_rgb = Image.open(fname)
        img_grayscale = img_rgb.convert('L')
        img_resize = img_grayscale.resize((200, 200), Image.LANCZOS)
        img = ImageTk.PhotoImage(image=img_resize)
        self.img_panel.config(image=img)
        self.img_panel.photo_ref = img

    def display_color_channel(self, channel):
        channel_index = {'red': 0, 'green': 1, 'blue': 2}.get(channel)
        img_rgb = Image.open(self.fname)
        image_array = np.array(img_rgb)
        image_array[..., [i for i in range(3) if i != channel_index]] = 0
        pil_img = Image.fromarray(np.uint8(image_array))
        img_resize = pil_img.resize((200, 200), Image.LANCZOS)
        img = ImageTk.PhotoImage(image=img_resize)
        self.img_panel.config(image=img)
        self.img_panel.photo_ref = img

    def select_method(self, event):
        methods = {
            "Level 1": self.setup_level1,
            "Level 2": self.setup_level2,
            "Level 3": self.setup_level3,
            "Level 4": self.setup_level4,
            "Level 5": self.setup_level5
        }
        method = methods.get(self.clicked.get())
        if method:
            method()

    def setup_level1(self):
        data = readFile(self.text_filename)
        self.create_compression_buttons("compress1", data, "decompress1", "statistics1")

    def setup_level2(self):
        data, total_element, arr = readPILimg(self.fname)
        self.create_compression_buttons("compress2", data, "decompress2", "statistics2", total_element, arr)

    def setup_level3(self):
        diff_arr3, total_element, arr = readPILimg3(self.fname)
        self.create_compression_buttons("compress3", diff_arr3, "decompress3", "statistics3", total_element, arr)

    def setup_level4(self):
        img, r, g, b, arr, total_element = readPILimg4(self.fname)
        self.create_compression_buttons("compress4", [r, g, b], "decompress4", "statistics4", total_element, arr)

    def setup_level5(self):
        img, r, g, b, arr, total_element = readPILimg5(self.fname)
        diff_r = difference5(arr, r)
        diff_g = difference5(arr, g)
        diff_b = difference5(arr, b)
        self.create_compression_buttons("compress5", [diff_r, diff_g, diff_b], "decompress5", "statistics5", total_element, arr)

    def create_compression_buttons(self, compress_func, data, decompress_func, stats_func, total_element=None, arr=None):
        Button(self.root, text="Compressed", width=10,
               command=lambda: self.compress_func(compress_func, data, 0, 0)).grid(row=1, column=7)
        Button(self.root, text="Decompressed", width=10,
               command=lambda: self.decompress_func(decompress_func, 0, 0)).grid(row=1, column=8)
        Button(self.root, text="Comparison", width=10,
               command=lambda: self.print_statistics(stats_func, data)).grid(row=1, column=9)

    def compress_func(self, func_name, data, total_element, index):
        def display_encoding_saved():
            Label(root, text="Encoding data is saved", font=('Arial bold', 11)).place(x=250, y=60)

        def update_label(text, y_position):
            Label(root, text=text, font=('Arial bold', 11)).place(x=250, y=y_position)

        if func_name == "compress1":
            string1, tree1, encodingCodes1, prob_list1 = Huffman_Encoding1(data)
            outpath1 = compress1(string1)
            display_encoding_saved()
            update_label("Encoded Data ", 200)
            update_label(string1, 240)

        elif func_name == "compress2":
            encoding2, tree2, huffman_encoding2, problist2 = Huffman_Encoding2(data, total_element)
            outpath2 = compress2(encoding2)
            display_encoding_saved()

        elif func_name == "compress3":
            encoding3, tree3, huffman_encoding3, problist3 = Huffman_Encoding3(data, total_element)
            outpath3 = compress3(encoding3)
            display_encoding_saved()

        elif func_name == "compress4":
            encoding4, tree4, huffman_encoding4, problist4 = Huffman_Encoding4(data, total_element)
            color_map = {1: "r", 2: "g", 3: "b"}
            color = color_map.get(index)
            if color:
                outpath4 = compress4(encoding4, color)
                stats4_h.append(huffman_encoding4.copy())
                stats4_p.append(problist4)
            else:
                print("Error: Invalid index for compress4.")
            display_encoding_saved()

        elif func_name == "compress5":
            encoding5, tree5, huffman_encoding5, problist5 = Huffman_Encoding5(data, total_element)
            color_map = {1: "r", 2: "g", 3: "b"}
            color = color_map.get(index)
            if color:
                outpath5 = compress5(encoding5, color)
                stats5_h.append(huffman_encoding5.copy())
                stats5_p.append(problist5)
            else:
                print("Error: Invalid index for compress5.")
            display_encoding_saved()

        else:
            print("Error: Invalid function name.")
            
    def decompress_func(self, func_name, arr, index):
        def display_decoding_saved():
            Label(root, text="Decoding data is saved", font=('Arial bold', 11)).place(x=250, y=100)

        def update_label(text, y_position):
            Label(root, text=text, font=('Arial bold', 11)).place(x=250, y=y_position)

        def handle_rgb_decoding(func, encoding, tree, outpath, arr):
            (nrows, ncols) = arr.shape
            decoded_data, output_array = func(encoding, tree, outpath, arr)
            return decoded_data, np.array(output_array).reshape(nrows, ncols)

        def merge_and_show_images(output_r, output_g, output_b, func_name):
            decode_r = Image.fromarray(output_r).convert('L')
            decode_g = Image.fromarray(output_g).convert('L')
            decode_b = Image.fromarray(output_b).convert('L')
            final_img = Image.merge("RGB", (decode_r, decode_g, decode_b))
            showDecompressFile(f"saveDecompressedFile{func_name[-1]}", final_img, arr)

        if func_name == "decompress1":
            decoded_output1 = Huffman_Decoding1(string1, tree1, outpath1)
            saveDecompressedFile1(decoded_output1)
            display_decoding_saved()
            update_label("Decoded Data", 300)
            update_label(decoded_output1, 340)

        elif func_name == "decompress2":
            decoded_output = Huffman_Decoding2(encoding2, tree2, outpath2, arr)
            showDecompressFile("saveDecompressedFile2", decoded_output, arr)

        elif func_name == "decompress3":
            decoded_output = Huffman_Decoding3(encoding3, tree3, outpath3, arr)
            showDecompressFile("saveDecompressedFile3", decoded_output, arr)

        elif func_name == "decompress4":
            color_map = {1: 'r', 2: 'g', 3: 'b'}
            color = color_map.get(index)

            if color:
                func = Huffman_Decoding4
                decoded_data, output_array = handle_rgb_decoding(func, encoding4, tree4, outpath4, arr)

                if color == 'r':
                    output_r_array = output_array
                elif color == 'g':
                    output_g_array = output_array
                elif color == 'b':
                    output_b_array = output_array

                if len(total_list) == 3:
                    merge_and_show_images(output_r_array, output_g_array, output_b_array, func_name)
                else:
                    print("There is a mistake")

            else:
                print("Error: Invalid index for decompress4.")

        elif func_name == "decompress5":
            color_map = {1: 'r', 2: 'g', 3: 'b'}
            color = color_map.get(index)

            if color:
                func = Huffman_Decoding5
                decoded_data, output_array = handle_rgb_decoding(func, encoding5, tree5, outpath5, arr)

                if color == 'r':
                    output_r_array_5 = output_array
                elif color == 'g':
                    output_g_array_5 = output_array
                elif color == 'b':
                    output_b_array_5 = output_array

                if len(total_list_5) == 3:
                    merge_and_show_images(output_r_array_5, output_g_array_5, output_b_array_5, func_name)
                else:
                    print("There is a mistake")

            else:
                print("Error: Invalid index for decompress5.")

        else:
            print("Error: Invalid function name.")


    def print_statistics(self, func_name, data):
        try:
            stats = None
            if func_name == "statistics1":
                stats = self.calculate_text_statistics(data)
            elif func_name == "statistics2":
                stats = self.calculate_image_statistics(data)
            elif func_name == "statistics3":
                stats = self.calculate_image_diff_statistics(data)
            elif func_name == "statistics4":
                stats = self.calculate_image_color_statistics(data)
            elif func_name == "statistics5":
                stats = self.calculate_image_color_diff_statistics(data)
            else:
                raise ValueError("Unknown statistics method")
            
            if stats:
                self.display_statistics(stats)
            else:
                print("No statistics available!")
        except Exception as e:
            print(f"An error occurred while calculating statistics: {str(e)}")

    # Compression and Decompression Methods

    def compress_text_data(self, data):
        # Simple text compression using zlib
        compressed_data = zlib.compress(data.encode('utf-8'))
        with open('compressed_text.gz', 'wb') as f:
            f.write(compressed_data)
    
    def decompress_text_data(self, arr):
        # Decompress text data
        compressed_data = arr
        decompressed_data = zlib.decompress(compressed_data).decode('utf-8')
        print(decompressed_data)
    
    def compress_image_data(self, data):
        # Compress image using PNG format
        image = Image.open(data)
        compressed_data = image.save('compressed_image.png', format='PNG')
    
    def decompress_image_data(self, arr):
        # Decompress image
        image = Image.open(arr)
        image.show()
    
    def compress_image_diff_data(self, data):
        # Simple image difference compression
        image = Image.open(data).convert('L')
        image_diff = np.diff(np.array(image), axis=0)
        compressed_diff = zlib.compress(image_diff.tobytes())
        with open('compressed_image_diff.gz', 'wb') as f:
            f.write(compressed_diff)
    
    def decompress_image_diff_data(self, arr):
        # Decompress image difference
        compressed_diff = arr
        image_diff = np.frombuffer(zlib.decompress(compressed_diff), dtype=np.uint8)
        # Assuming image dimensions are known
        height, width = 512, 512  # Example dimensions
        image_diff = image_diff.reshape((height-1, width))
        image = np.zeros((height, width), dtype=np.uint8)
        image[1:] = image_diff
        Image.fromarray(image).show()

    def compress_image_color_data(self, data):
        # Compress color image using PNG format
        image = Image.open(data)
        compressed_data = image.save('compressed_color_image.png', format='PNG')
    
    def decompress_image_color_data(self, arr):
        # Decompress color image
        image = Image.open(arr)
        image.show()
    
    def compress_image_color_diff_data(self, data):
        # Simple color image difference compression
        image = Image.open(data).convert('RGB')
        image_diff = np.diff(np.array(image), axis=0)
        compressed_diff = zlib.compress(image_diff.tobytes())
        with open('compressed_color_image_diff.gz', 'wb') as f:
            f.write(compressed_diff)
    
    def decompress_image_color_diff_data(self, arr):
        # Decompress color image difference
        compressed_diff = arr
        image_diff = np.frombuffer(zlib.decompress(compressed_diff), dtype=np.uint8)
        # Assuming image dimensions are known
        height, width, channels = 512, 512, 3  # Example dimensions
        image_diff = image_diff.reshape((height-1, width, channels))
        image = np.zeros((height, width, channels), dtype=np.uint8)
        image[1:] = image_diff
        Image.fromarray(image).show()

    # Statistics Calculation Methods

    def calculate_text_statistics(self, data):
        # Basic statistics for text data
        word_count = len(data.split())
        char_count = len(data)
        return {'word_count': word_count, 'char_count': char_count}

    def calculate_image_statistics(self, data):
        # Basic statistics for image data
        image = Image.open(data)
        width, height = image.size
        return {'width': width, 'height': height}

    def calculate_image_diff_statistics(self, data):
        # Basic statistics for image difference data
        compressed_diff = data
        original_size = len(compressed_diff)
        return {'original_size': original_size}

    def calculate_image_color_statistics(self, data):
        # Basic statistics for color image data
        image = Image.open(data)
        width, height = image.size
        return {'width': width, 'height': height}

    def calculate_image_color_diff_statistics(self, data):
        # Basic statistics for color image difference data
        compressed_diff = data
        original_size = len(compressed_diff)
        return {'original_size': original_size}

    def display_statistics(self, stats):
        # Display statistics in a simple format
        for key, value in stats.items():
            print(f"{key}: {value}")

# Example usage
root = tk.Tk()
app = HuffmanCodingApp(root)
''' 
text_data = "This is an example text for compression and decompression."
image_file = 'example_image.png'  # Path to your image file

app.compress_func("compress1", text_data, len(text_data))
app.decompress_func("decompress1", open('compressed_text.gz', 'rb').read())
app.print_statistics("statistics1", text_data)

app.compress_func("compress2", image_file, os.path.getsize(image_file))
app.decompress_func("decompress2", 'compressed_image.png')
app.print_statistics("statistics2", image_file)
'''
root.mainloop()
