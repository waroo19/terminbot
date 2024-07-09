import requests
import cv2
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

# TODO: does not work as of yet!


# Set the Tesseract executable path if it's not in your system PATH
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Function to download the CAPTCHA image
def download_captcha(url, filename):
    response = requests.get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)

# Function to process the image and extract text using pytesseract
def solve_captcha(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Increase image resolution
    gray = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
    
    # Enhance the contrast of the image
    pil_image = Image.fromarray(gray)
    enhancer = ImageEnhance.Contrast(pil_image)
    enhanced_image = enhancer.enhance(2)
    
    # Optionally, apply filters to improve clarity
    enhanced_image = enhanced_image.filter(ImageFilter.SHARPEN)
    
    # Save the processed image temporarily
    temp_filename = "temp.png"
    enhanced_image.save(temp_filename)
    
    # Print the temp filename for debugging
    print(f"Processed image saved as: {temp_filename}")

    # Manually open the image for inspection
    enhanced_image.show()
    
    # Use pytesseract to extract text from the image
    custom_config = r'--oem 3 --psm 8'
    text = pytesseract.image_to_string(enhanced_image, config=custom_config)
    
    print(f"Extracted text: {text.strip()}")
    
    return text.strip()

def main():
    captcha_url = "https://tevis.ekom21.de/fra/app/securimage/securimage_show.php?type=1&source=personaldata&44e9b94bab25dcfd1b5cab4e35c987b2"
    captcha_image_path = "captcha.jpg"
    
    download_captcha(captcha_url, captcha_image_path)
    
    captcha_text = solve_captcha(captcha_image_path)
    print("Final Extracted CAPTCHA text:", captcha_text)

if __name__ == "__main__":
    main()