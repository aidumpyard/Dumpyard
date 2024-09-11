import win32com.client

# Start PowerPoint application
ppt_app = win32com.client.Dispatch("PowerPoint.Application")
ppt_app.Visible = True

# Open the PowerPoint presentation
presentation = ppt_app.Presentations.Open(r'C:\path\to\your\presentation.pptx')

# Define the new size (in points)
new_width = 300  # You can adjust this value
new_height = 150  # You can adjust this value

# Loop through each slide in the presentation
for slide in presentation.Slides:
    print(f"Slide {slide.SlideIndex}:")
    
    # Loop through each shape in the slide
    for shape in slide.Shapes:
        shape_type = shape.Type
        left = shape.Left
        top = shape.Top
        
        try:
            if shape.HasTextFrame and shape.TextFrame.HasText:
                value = shape.TextFrame.TextRange.Text.strip()
                print(f"Shape Type: {shape_type}, Position: ({left}, {top}), Value: {value}")
                
                # Example condition: resize shape if it contains a number or specific text
                if value.isdigit():  # Resize only if the text is a number
                    shape.Width = new_width
                    shape.Height = new_height
                    print(f"Resized shape with number {value} to {new_width}x{new_height}")
                elif "Resize me" in value:  # Example: Resize shapes with specific text
                    shape.Width = new_width
                    shape.Height = new_height
                    print(f"Resized shape with text '{value}' to {new_width}x{new_height}")
            else:
                print(f"Shape Type: {shape_type}, Position: ({left}, {top}), No text available")
        except AttributeError:
            print(f"Shape Type: {shape_type}, Position: ({left}, {top}), No text available")

# Close the presentation without saving
presentation.Close()

# Quit PowerPoint application
ppt_app.Quit()