from PIL import Image, ImageDraw, ImageFont
import os

# Create a 800x600 image with a gradient background
width, height = 800, 600
image = Image.new('RGB', (width, height), color='#f0f4f8')

draw = ImageDraw.Draw(image)

# Draw a gradient background
for y in range(height):
    r = int(59 + (99 - 59) * y / height)
    g = int(130 + (179 - 130) * y / height)
    b = int(246 + (229 - 246) * y / height)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# Draw a simple car silhouette shape
car_color = '#2563eb'
# Car body
draw.rectangle([200, 300, 600, 450], fill=car_color, outline='#1e40af', width=3)
# Car roof
draw.rectangle([280, 250, 520, 300], fill=car_color, outline='#1e40af', width=3)
# Windows
draw.rectangle([290, 260, 390, 295], fill='#60a5fa', outline='#1e40af', width=2)
draw.rectangle([410, 260, 510, 295], fill='#60a5fa', outline='#1e40af', width=2)
# Wheels
draw.ellipse([230, 420, 310, 500], fill='#1f2937', outline='#000000', width=2)
draw.ellipse([490, 420, 570, 500], fill='#1f2937', outline='#000000', width=2)
# Wheel centers
draw.ellipse([255, 445, 285, 475], fill='#6b7280')
draw.ellipse([515, 445, 545, 475], fill='#6b7280')

# Add text
try:
    # Try to use a nice font
    font_large = ImageFont.truetype("arial.ttf", 48)
    font_small = ImageFont.truetype("arial.ttf", 24)
except:
    # Fallback to default font
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Draw text
text = "No Image Available"
bbox = draw.textbbox((0, 0), text, font=font_large)
text_width = bbox[2] - bbox[0]
text_x = (width - text_width) // 2
draw.text((text_x, 100), text, fill='#1e293b', font=font_large)

text2 = "Premium Car Rentals"
bbox2 = draw.textbbox((0, 0), text2, font=font_small)
text2_width = bbox2[2] - bbox2[0]
text2_x = (width - text2_width) // 2
draw.text((text2_x, 520), text2, fill='#475569', font=font_small)

# Save the image
output_path = os.path.join('static', 'car_images', 'default_car.jpg')
image.save(output_path, 'JPEG', quality=95)
print(f"Default car image created successfully at: {output_path}")
