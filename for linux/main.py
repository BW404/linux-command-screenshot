import pyautogui
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import PyPDF2
import os
from PIL import ImageGrab


def generate_image():    
    if not os.path.exists("image"):
        os.makedirs("image")
    time.sleep(2)
    
    with open("command.txt", "r") as f: 
        pyautogui.hotkey('ctrl', 'alt', 't')
        time.sleep(3)
        pyautogui.hotkey('win', 'up')
        pyautogui.typewrite("clear")
        pyautogui.press('enter')
              
        for i in range(1, 22):
            x = f.readline().replace("\n", "")
            pyautogui.typewrite(x)
            pyautogui.press('enter') 
            time.sleep(1)
            pyautogui.hotkey('ctrl', 'shift', 'home')

            # Use ImageGrab to take a screenshot
            screenshot = ImageGrab.grab()
            screenshot.save(f"image/image{i}.png")

            pyautogui.typewrite("clear")
            pyautogui.press('enter')
            print(x)  
            
    pyautogui.typewrite("exit")
    pyautogui.press('enter')
    pyautogui.typewrite("exit")
    pyautogui.press('enter')      
    print("Done")

def create_pdfs():
    def generate_pdf(text1, image_path1, text2, image_path2, count):
        if not os.path.exists("raw_pdfs"):
            os.makedirs("raw_pdfs")
        
        output_path = f"raw_pdfs/pdf{count}.pdf"
        
        # Define image dimensions in pixels
        image_width_px = 384 
        image_height_px = 216 
        # Create a document template
        pdf = SimpleDocTemplate(output_path, pagesize=letter)
        
        # Get style for the paragraph text
        styles = getSampleStyleSheet()
        style = styles["Normal"]

        # Create the text paragraph and the image
        story = []

        # Add text with auto-wrapping
        story.append(Paragraph(text1, style))

        # Convert image dimensions from pixels to points
        image_width_pt = image_width_px / 72  # Convert width from px to points
        image_height_pt = image_height_px / 72  # Convert height from px to points

        # Add a spacer to create blank lines before the image
        story.append(Spacer(1, 20))  # 1 inch of vertical space

        # Add image to the story with custom dimensions
        img = Image(image_path1, width=image_width_pt * inch, height=image_height_pt * inch)
        story.append(img)
        
        story.append(Spacer(1, 40))       
        
        # Add text with auto-wrapping
        story.append(Paragraph(text2, style))

        story.append(Spacer(1, 20))  # 1 inch of vertical space

        img = Image(image_path2, width=image_width_pt * inch, height=image_height_pt * inch)
        story.append(img)

        # Build the PDF
        pdf.build(story)
        print(f"PDF saved at {output_path}")

    command_desc_list = open("command_desc.txt", "r") 
    count = 1
    i = 1
    while i <= 20:
        text1 = command_desc_list.readline().strip()
        text2 = command_desc_list.readline().strip()
        
        image_path1 = f"image/image{i}.png"
        i += 1
        image_path2 = f"image/image{i}.png"    
        i += 1
        
        generate_pdf(text1, image_path1, text2, image_path2, count)
        count += 1

    command_desc_list.close()
    print("All PDFs created successfully")

def merge_pdfs():
    merger = PyPDF2.PdfMerger()

    for file in os.listdir(os.curdir + "/raw_pdfs"):
        file = os.path.join(os.curdir + "/raw_pdfs", file)
        if file.endswith(".pdf"):
            merger.append(file)
    merger.write("screenshot.pdf")
    
    print("All PDFs merged successfully. Output file: screenshot.pdf")

input("Press enter to start the process. Do not use the PC while the process is running.")
generate_image()
create_pdfs()
merge_pdfs()
input("Press Enter to exit")
