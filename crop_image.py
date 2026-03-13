from PIL import Image, ImageDraw

def create_circular_image(input_path, output_path, target_size=(400, 400)):
    # Open the image
    img = Image.open(input_path).convert("RGBA")
    
    # Calculate dimensions for a square crop from the center
    width, height = img.size
    min_dim = min(width, height)
    left = (width - min_dim) // 2
    top = (height - min_dim) // 4  # Slightly offset to the top for a headshot
    right = (width + min_dim) // 2
    bottom = top + min_dim
    
    # Crop to square
    img = img.crop((left, top, right, bottom))
    
    # Resize to target size for consistency
    img = img.resize(target_size, Image.Resampling.LANCZOS)
    
    # Create a circular mask
    mask = Image.new("L", target_size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, target_size[0], target_size[1]), fill=255)
    
    # Apply the mask to the image
    circular_img = Image.new("RGBA", target_size, (0, 0, 0, 0))
    circular_img.paste(img, (0, 0), mask=mask)
    
    # Add a professional white border
    border_width = 8
    border_img = Image.new("RGBA", (target_size[0] + 2*border_width, target_size[1] + 2*border_width), (0, 0, 0, 0))
    draw_border = ImageDraw.Draw(border_img)
    draw_border.ellipse((0, 0, border_img.width, border_img.height), fill=(255, 255, 255, 255))
    
    # Paste the circular image onto the border background
    border_img.paste(circular_img, (border_width, border_width), mask=circular_img)
    
    # Save as PNG to preserve transparency
    border_img.save(output_path, "PNG")

# Apply to the profile images
create_circular_image("change.jpg.jpeg", "profile-pic.png")
create_circular_image("change.jpg.jpeg", "about-pic.png")

print("Successfully cropped and formatted images!")
