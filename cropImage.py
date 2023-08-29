import os
from PIL import Image

def crop_whitespace(image_path, output_path):
    # Open the image using PIL
    img = Image.open(image_path)
    
    # Convert the image to grayscale for easier analysis
    gray_img = img.convert("L")
    
    # Get the dimensions of the image
    width, height = gray_img.size

    # Go through each pixel and get the average color value
    colors = []
    for y in range(height):
        for x in range(width):
            colors.append(gray_img.getpixel((x, y)))
    
    # Get the average color value
    avg_color = sum(colors) / len(colors)
    avg_color+=25
    if avg_color > 240:
        avg_color = 240
    print(f"avg_color: {avg_color}")

    bound_box = []
    found_first = False
    
    # Find the first non-white pixel moving from left to right, top to bottom
    for y in range(height):
        for x in range(width):
            if lessThanFunc(gray_img.getpixel((x, y)), avg_color):
                if not checkSurroundingPixels(gray_img, x, y, avg_color):
                    bound_box.append((x,y))
                    found_first = True
                    break
        if found_first:
            break
    
    # Find the first non-white pixel moving from right to left, top to bottom
    found_first = False
    for y in range(height):
        for x in range(width-1, -1, -1):
            if lessThanFunc(gray_img.getpixel((x, y)), avg_color):
                if not checkSurroundingPixels(gray_img, x, y, avg_color):
                    bound_box.append((x,y))
                    found_first = True
                    break
        if found_first:
            break

    # Find the first non-white pixel moving from bottom to top, left to right
    found_first = False
    for x in range(width):
        for y in range(height-1, -1, -1):
            if lessThanFunc(gray_img.getpixel((x, y)), avg_color):
                if not checkSurroundingPixels(gray_img, x, y, avg_color):
                    bound_box.append((x,y))
                    found_first = True
                    break
        if found_first:
            break

    # Find the first non-white pixel moving from bottom to top, right to left
    found_first = False
    for x in range(width-1, -1, -1):
        for y in range(height-1, -1, -1):
            if lessThanFunc(gray_img.getpixel((x, y)), avg_color):
                if not checkSurroundingPixels(gray_img, x, y, avg_color):
                    bound_box.append((x,y))
                    found_first = True
                    break
        if found_first:
            break
    

    print(bound_box)
    
    # Find the bounding box of the non-white region
    min_x = min(x for x, y in bound_box)
    max_x = max(x for x, y in bound_box)
    min_y = min(y for x, y in bound_box)
    max_y = max(y for x, y in bound_box)
    
    # Crop the image to the bounding box
    cropped_img = img.crop((min_x-3,           min_y-3,           max_x+4,           max_y+4))
    
    # Save the cropped image
    cropped_img.save(output_path)
    print("Cropped image saved successfully.")

# this function takes in an image and check to see if the surrounding pixels are white
# if they are, then it will return true, otherwise it will return false
def checkSurroundingPixels(image, x, y, avg_color):
    width, height = image.size
    if x == 0 or x == width-1 or y == 0 or y == height-1:
        # Edge case
        return False
    if image.getpixel((x-3, y-3)) > avg_color or image.getpixel((x, y-3)) > avg_color or image.getpixel((x+3, y-3)) > avg_color or image.getpixel((x-3, y)) > avg_color or image.getpixel((x+3, y)) > avg_color or image.getpixel((x-3, y+3)) > avg_color or image.getpixel((x, y+3)) > avg_color or image.getpixel((x+3, y+3)) > avg_color:
        # Surrounding pixels are white
        return True
    # Surrounding pixels are not white
    return False

def lessThanFunc(value, avg_color):
    return value <= avg_color

def get_image_files(directory_path):
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    image_files = {}

    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in image_extensions):
                image_files[str(os.path.join(root, file).replace('\\', '/'))] = file
    
    return image_files

if __name__ == "__main__":
    # Get all images in the current directory
    print(get_image_files('./images'))

    #input_image_path = input("Enter filepath to image: ")  # Replace with your input image file path
    images = get_image_files('./images')
    for input_image_path in images:
        print(input_image_path)
        output_image_path = f"output/{str(images[input_image_path]).split('.')[0]}-cropped.jpg"
        print(output_image_path)
    
        crop_whitespace(input_image_path, output_image_path)
