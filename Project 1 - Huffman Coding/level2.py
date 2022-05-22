import os
from PIL import *
from PIL import Image
import numpy as np
import math


class HuffmanNode:

    def __init__(self, probability, symbol, left=None, right=None):
        self.probability = probability
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''


codes = {}


def ConstructionOfCodes(node, val=''):
    string = val + str(node.code)
    if (node.left):
        ConstructionOfCodes(node.left, string)

    if (node.right):
        ConstructionOfCodes(node.right, string)

    if node.left == None and node.right == None:
        codes[node.symbol] = string

    return codes


def FindProbability(data, total_element):
    symbols = {}
    for i in data:
        if i in symbols:
            symbols[i] += 1
        else:
            symbols[i] = 1

    values = symbols.values()
    total = sum(values)

    prob_list = []
    for i in symbols:
        prob_list.append(symbols[i] / (total_element))


    entropy = 0
    for i in prob_list:
        entropy += i * (math.log(i, 2))

    return symbols, prob_list


def Huffman_Encoding2(data, total_element):
    probabilityOfSymbols, problist = FindProbability(data, total_element)
    symbols = probabilityOfSymbols.keys()
    probabilities = probabilityOfSymbols.values()

    list_nodes = []

    for i in symbols:
        node_list = HuffmanNode(probabilityOfSymbols.get(i), i)
        list_nodes.append(node_list)

    while len(list_nodes) > 1:
        sorted_nodes = sorted(list_nodes, key=lambda node: node.probability)

        right = sorted_nodes[0]
        left = sorted_nodes[1]

        left.code = 0
        right.code = 1

        newNode = HuffmanNode(left.probability + right.probability, left.symbol + right.symbol, left, right)

        list_nodes.remove(left)
        list_nodes.remove(right)
        list_nodes.append(newNode)


    encodingCodes = ConstructionOfCodes(list_nodes[0])

    len_list = []
    for i in encodingCodes:
        len_list.append(len(encodingCodes[i]))

    res_list = []
    res_list = [a * b for a, b in zip(len_list, problist)]
    lAvg = sum(res_list)

    encodingOutput = []
    for i in data:
        encodingOutput.append(encodingCodes[i])

    string = ''.join([str(item) for item in encodingOutput])

    return string, list_nodes[0], encodingCodes,problist


def Huffman_Decoding2(encodedData, huffmanTree, filename, arr):

    f =  open(filename, "rb")
    encoded_data = f.read()

    current = huffmanTree
    output = []

    for i in encoded_data:

        if int(i) == 0:
            huffmanTree = huffmanTree.left

        elif int(i) == 1:
            huffmanTree = huffmanTree.right

        if huffmanTree.left == None and huffmanTree.right == None:
            output.append(huffmanTree.symbol)
            huffmanTree = current

    string = ''.join([str(item) for item in output])


    return string


def get_encoded_text(string):
    encoded_text = ""
    for character in string:
        encoded_text += codes[character]
    return encoded_text


def pad_encoded_text(encoded_text):
    extra_padding = 8 - len(encoded_text) % 8
    for i in range(extra_padding):
        encoded_text += "0"

    padded_info = "{0:08b}".format(extra_padding)
    encoded_text = padded_info + encoded_text
    return encoded_text


def get_byte_array(padded_encoded_text):
    if (len(padded_encoded_text) % 8 != 0):
        print("Encoded text not padded properly")
        exit(0)

    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i + 8]
        b.append(int(byte, 2))
    return b

def compress2(encoded_text):

    filename = "E:/Users/batu_/Desktop/MEF Üniversitesi 2.Sınıf 2021 - 2022 Dönemi/2021-2022 Bahar Dönemi Ders Programı/Programming Studio/ImageProject/Huffman Coding - Project 1/Project 1 - Huffman Coding/CompressDecompressFiles/compressed_file_lvl2.txt"
    f = open(filename, "w")
    f.write(encoded_text)
    f.close()

    output_path = "E:/Users/batu_/Desktop/MEF Üniversitesi 2.Sınıf 2021 - 2022 Dönemi/2021-2022 Bahar Dönemi Ders Programı/Programming Studio/ImageProject/Huffman Coding - Project 1/Project 1 - Huffman Coding/CompressDecompressFiles/compressed_file_lvl2.bin"

    with  open(output_path, 'wb') as output:

        padded_encoded_text = pad_encoded_text(encoded_text)
        byte_array = get_byte_array(padded_encoded_text)
        output.write(bytes(byte_array))


    return output_path

def saveDecompressedFile2(decodedOutput, arr):

    (nrows, ncols) = arr.shape
    decoded_arr = np.array(decodedOutput)
    decoded_arr = Image.fromarray(arr.reshape(nrows, ncols), 'L')

    #global outpath_lvl2
    outpath_lvl2 = "E:/Users/batu_/Desktop/MEF Üniversitesi 2.Sınıf 2021 - 2022 Dönemi/2021-2022 Bahar Dönemi Ders Programı/Programming Studio/ImageProject/Huffman Coding - Project 1/Project 1 - Huffman Coding/CompressDecompressFiles/decompressed_file_lvl2.JPG"
    decoded_arr.save(outpath_lvl2)

    return outpath_lvl2

def readPILimg(fname):

    img = Image.open(fname)
    img_gray = color2gray(img)

    arr = PIL2np(img_gray)
    arr_list = arr.flatten()
    data = arr_list.tolist()
    (nrows, ncols) = arr.shape
    total_element = (nrows * ncols)

    return data, total_element, arr


def color2gray(img):
    img_gray = img.convert('L')
    return img_gray


def PIL2np(img):
    nrows = img.size[0]
    ncols = img.size[1]
    imgarray = np.array(img.convert("L"))
    return imgarray


def np2PIL(im):
    img = Image.fromarray(np.uint8(im))

    return img

def statistics2(huffman_encoding, problist, data):

    len_list = []
    for i in huffman_encoding:
        len_list.append(len(huffman_encoding[i]))

    res_list = []
    res_list = [a * b for a, b in zip(len_list, problist)]
    lAvg = sum(res_list)

    before_compression = len(data) * 8  # total bit space to stor the data before compressio
    after_compression = 0
    symbols = huffman_encoding.keys()

    for i in symbols:
        count = data.count(i)
        after_compression += count * len(
            huffman_encoding[i])  # calculate how many bit is required for that symbol in total

    # Entropy
    entropy = 0
    for i in problist:
        entropy += i * (math.log(i, 2))


    output =  "The entropy is : {0:.3f}\n".format((-1 * entropy)), "L_avg is : {0:.3f}\n".format(lAvg), "Before the " \
                                                                                                         "compression : {" \
                                                                                                         "}\n".format(
            before_compression), "After the compression : {}\n".format(
            after_compression), "The Compression Ratio (Cr) is " \
                                "{0:.3f} ".format(
            before_compression / after_compression)

    return output
