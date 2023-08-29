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
                    print(gray_img.getpixel((x, y)))
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
                    print(gray_img.getpixel((x, y)))
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
                    print(gray_img.getpixel((x, y)))
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
                print(gray_img.getpixel((x, y)))
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

    print((min_x, min_y))
    print((max_x, max_y))
    
    # Crop the image to the bounding box
    cropped_img = img.crop((min_x-1, min_y-1, max_x+1, max_y+1))
    
    # Save the cropped image
    cropped_img.save(output_path)
    print("Cropped image saved successfully.")

# this function takes in an image and check to see if the surrounding pixels are white
# if they are, then it will return true, otherwise it will return false
def checkSurroundingPixels(image, x, y, avg_color):
    width, height = image.size
    if x == 0 or x == width-1 or y == 0 or y == height-1:
        print("Edge case")
        return False
    if image.getpixel((x-3, y-3)) > avg_color or image.getpixel((x, y-3)) > avg_color or image.getpixel((x+3, y-3)) > avg_color or image.getpixel((x-3, y)) > avg_color or image.getpixel((x+3, y)) > avg_color or image.getpixel((x-3, y+3)) > avg_color or image.getpixel((x, y+3)) > avg_color or image.getpixel((x+3, y+3)) > avg_color:
        return True
    return False

def lessThanFunc(value, avg_color):
    return value <= avg_color

if __name__ == "__main__":
    input_image_path = input("filename with extension: ")  # Replace with your input image file path
    output_image_path = f"{input_image_path.split('.')[0]}-cropped.{input_image_path.split('.')[1]}"  # Replace with your desired output image file path
    
    crop_whitespace(input_image_path, output_image_path)
