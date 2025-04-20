from PIL import Image
import sys
import os

def convert_webp_to_jpg(input_path):
    """Convert a WebP image to JPG format."""
    try:
        # Open the WebP image
        img = Image.open(input_path)
        
        # Create output filename by replacing .webp with .jpg
        output_path = os.path.splitext(input_path)[0] + '.jpg'
        
        # Convert and save as JPG
        img.convert('RGB').save(output_path, 'JPEG')
        print(f"Successfully converted '{input_path}' to '{output_path}'")
        return True
    except Exception as e:
        print(f"Error converting {input_path}: {str(e)}")
        return False

def process_directory(directory_path):
    """Process all WebP files in the given directory."""
    if not os.path.exists(directory_path):
        print(f"Error: Directory '{directory_path}' not found.")
        return
    
    if not os.path.isdir(directory_path):
        print(f"Error: '{directory_path}' is not a directory.")
        return
    
    # Count statistics
    total_files = 0
    converted_files = 0
    
    # Find all WebP files in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith('.webp'):
            total_files += 1
            input_path = os.path.join(directory_path, filename)
            if convert_webp_to_jpg(input_path):
                converted_files += 1
    
    # Print summary
    if total_files == 0:
        print(f"No WebP files found in '{directory_path}'")
    else:
        print(f"\nConversion complete!")
        print(f"Total WebP files found: {total_files}")
        print(f"Successfully converted: {converted_files}")
        print(f"Failed conversions: {total_files - converted_files}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python webp_to_jpg.py <directory_path>")
    else:
        process_directory(sys.argv[1])
