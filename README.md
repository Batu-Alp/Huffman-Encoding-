# Image Compression Using Huffman Coding

## Abstract

Data is encoded as bit strings, whether it’s for photos, games, or videos. Huffman Coding is a lossless data compression algorithm that reduces the size of these bit strings, optimizing processing speed and storage space without loss of information. This project utilizes Huffman Coding to compress images and text files by encoding frequently used characters with shorter bit strings and less frequent ones with longer bit strings.

## Project Description

This project implements Huffman Encoding for both text and image compression, spanning six levels of increasing complexity. The Huffman algorithm ensures optimal compression by assigning variable-length codes based on symbol frequencies.

### Levels of the Project

#### Level 1: Huffman Tree for Text Compression
- Reads a text file and calculates symbol frequencies.
- Generates a Huffman Tree and assigns binary codes (0s and 1s) based on symbol frequency.
- Implements both encoding and decoding functions.

#### Level 2: Image Compression (Grayscale)
- Converts an image to grayscale, then into a one-dimensional array for compression.
- Encodes the array using Huffman Coding and saves the compressed data in a `.bin` file.
- Decodes the binary data back into the original image.

#### Level 3: Image Compression Using Differences
- Takes the difference between consecutive pixels in the grayscale image to reduce entropy.
- Encodes and decodes the difference array for more efficient compression.

#### Level 4: RGB Image Compression
- Compresses RGB images by separating the red, green, and blue channels.
- Applies Huffman Encoding to each channel separately and recombines them into a full image after decompression.

#### Level 5: RGB Image Compression with Differences
- Similar to Level 4, but first calculates the differences between consecutive pixel values in each channel (R, G, B).
- Encodes and decodes the difference arrays for each color channel before recombining them into an image.

#### Level 6: GUI for User Interaction
- A graphical user interface allows the user to select text or image files for compression/decompression.
- Displays statistics like entropy, code length, and compression ratio on the screen.

## Results

- **Level 1**: Successfully compressed and decompressed text files.
- **Level 2**: Successfully compressed grayscale images and verified decompressed image integrity.
- **Level 3**: Achieved higher compression by encoding pixel differences.
- **Level 4 & 5**: Successfully encoded and decoded RGB images, with further entropy reduction by using differences in pixel values.
- **Level 6**: GUI developed to enable users to select files and perform compression/decompression operations.
