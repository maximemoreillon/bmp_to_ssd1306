import PIL as pillow
from PIL import Image
import sys
import numpy as np
import os

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as tkMessageBox
import tkinter.simpledialog as tkSimpleDialog
from tkinter.simpledialog import Dialog


def print_image_from_char_array_to_console(image_bytes_hex, width, height):
    # Prints image in console

    # Create a string containing all the bits of the image
    pixels_string = "";
    for char in image_bytes_hex:
        pixels_string += bin(int(char,16))[2:].zfill(8)[::-1]

    # Print the string to console
    print ("Image as it appears on SSD1306:")
    print ("")
    for y in range(0,height):
        for x in range(0,width):
            if pixels_string[width*y+x] == "1":
                sys.stdout.write("#")
            else:
                sys.stdout.write(" ")
        print ("")

def print_char_array_to_console(image_bytes_hex):
    # Prints the char array corresponding to the image

    # Select display format (number of rows and columns)
    output_column_count = 16
    output_row_count = len(image_bytes_hex)/output_column_count

    print ("Char array:")
    print ("")

    for row in range(0,output_row_count):
        for col in range(0,output_column_count):
            sys.stdout.write(image_bytes_hex[row*output_column_count+col]+",")
        print ("")
    print ("")

def print_char_array_to_file(image_bytes_hex, image_width, image_height, image_name):
    # Prints the char array corresponding to the image

    output_file = open(image_name + ".h","w+")

    # Select display format (number of rows and columns)
    output_column_count = 16
    output_row_count = int(len(image_bytes_hex)/output_column_count)

    output_file.write("#define " + image_name.upper() + "_WIDTH " + str(image_width) +"\n")
    output_file.write("#define " + image_name.upper() + "_HEIGHT " + str(image_height) +"\n")

    output_file.write("\n");
    output_file.write("const char "+image_name+"[] PROGMEM = {\n");


    for row in range(0,output_row_count):
        output_file.write("  ")
        for col in range(0,output_column_count):
            output_file.write(image_bytes_hex[row*output_column_count+col]+",")
        output_file.write("\n")
    output_file.write("};")

    output_file.close()

def pixels_to_binary(image_pixels, image_width, image_height):
    # Convert image pixels to string of bits

    # Storing binary pixels into an array
    binary_image_string = ""
    for y in range(0,image_height):
        for x in range(0,image_width):
            if image_pixels[y,x]:
                binary_image_string += "0"
            else:
                binary_image_string += "1"

    return binary_image_string

def bits_to_hex(image_bits):
    # Converting image bits to bytes in hex format

    image_bytes_hex = []

    image_byte_count = int(len(image_bits)/8)

    for pixel in range(0,image_byte_count):
        # Extract 8 bits in reverse order
        byte_binary = image_bits[8*pixel:8*pixel+8][::-1]
        # Conversion to hex and storing into result array
        image_bytes_hex.append(hex(int(byte_binary, 2)))

    return image_bytes_hex

# Loading image
root = tk.Tk()
root.withdraw()
image_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
image_bmp = Image.open(image_path)
image_filename = os.path.splitext(os.path.basename(image_path))[0]

# Get pixels from image
image_pixels = np.array(image_bmp)

# Extract image dimensions from pixel array
image_width = image_pixels.shape[1]
image_height = image_pixels.shape[0]

# Convert image pixels to string of bits
image_bits = pixels_to_binary(image_pixels, image_width, image_height)

# Convert image bits in bytes, hex format
image_bytes_hex = bits_to_hex(image_bits);

# Write to file
print_char_array_to_file(image_bytes_hex,image_width,image_height,image_filename)

# Print image to console
print_image_from_char_array_to_console(image_bytes_hex, image_width, image_height)
