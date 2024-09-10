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


def Huffman_Encoding4(data, total_element):
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

    encodingOutput = []
    for i in data:
        encodingOutput.append(encodingCodes[i])

    string = ''.join([str(item) for item in encodingOutput])
    #print("encodingCodes : ", encodingCodes)

    return string, list_nodes[0], encodingCodes, problist


def Huffman_Decoding4(encodedData, huffmanTree, filename, arr):

    f = open(filename, "rb")
    encoded_data = f.read()

    print("encodedData is : ", encodedData[:20])
    print("encoded_data is : ", encoded_data[:20])

    current = huffmanTree
    output = []

    for i in encodedData:

        if int(i) == 0:
            huffmanTree = huffmanTree.left

        elif int(i) == 1:
            huffmanTree = huffmanTree.right

        if huffmanTree.left == None and huffmanTree.right == None:
            output.append(huffmanTree.symbol)
            huffmanTree = current

    string = ''.join([str(item) for item in output])

    codes.clear()
    return string, output


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


def compress4(encoded_text, item):
    output_path = "E:/Users/batu_/Desktop/Git Large Files/Huffman-Encoding/Huffman-Encoding-/Project 1 - Huffman Coding/CompressDecompressFiles/compressed_file_lvl4.bin"
    with open(output_path, 'wb') as output:
        padded_encoded_text = pad_encoded_text(encoded_text)
        byte_array = get_byte_array(padded_encoded_text)
        output.write(byte_array)

    print("Compressed")
    return output_path


def readPILimg4(fname):
    img = Image.open(fname).convert("RGB")
    arr = PIL2np(img)
    (nrows, ncols) = arr.shape
    total_element = (nrows * ncols)
    r, g, b = img.split()

    return img, r, g, b, arr, total_element

def color2gray(img):
    img_gray = img.convert('L')
    return img_gray

def PIL2np(img):
    nrows = img.size[0]
    ncols = img.size[1]
    imgarray = np.array(img.convert("L"))
    return imgarray

def np2PIL(im):
    print("size of arr: ", im.shape)
    img = Image.fromarray(np.uint8(im))
    return img


def saveDecompressedFile4(decodedOutput_r, arr):
    outpath = "E:/Users/batu_/Desktop/Git Large Files/Huffman-Encoding/Huffman-Encoding-/Project 1 - Huffman Coding/CompressDecompressFiles/decompressed_file_lvl4.JPG"
    decodedOutput_r.save(outpath)
    return outpath


def statistics4(huffman_encoding, problist, data):
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
        after_compression += count * len(huffman_encoding[i])

    # Entropy
    entropy = 0
    for i in problist:
        entropy += i * (math.log(i, 2))

    output = (
        f"The entropy is : {entropy:.3f}\n"
        f"L_avg is : {lAvg:.3f}\n"
        f"Before the compression : {before_compression}\n"
        f"After the compression : {after_compression}\n"
        f"The Compression Ratio (Cr) is {before_compression / after_compression:.3f}"
    )

    return output

