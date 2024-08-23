import subprocess
import os
from PIL import Image
import numpy as np
import cv2

# Define paths
input_video = r'C:\Users\teamo\Desktop\personal\badapple.flv'
output_folder = r'C:\Users\teamo\Desktop\personal\frame'
binary_folder = r'C:\Users\teamo\Desktop\personal\binary'
ffmpeg_path = r'C:\Users\teamo\Desktop\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe'  # Correct path to ffmpeg.exe

print(f"Input Video: {input_video}")
print(f"Output Folder: {output_folder}")
print(f"Binary Folder: {binary_folder}")
print(f"FFmpeg Path: {ffmpeg_path}")

# Create output directories if they don't exist
os.makedirs(output_folder, exist_ok=True)
os.makedirs(binary_folder, exist_ok=True)

# Extract frames
subprocess.run([
    ffmpeg_path, '-i', input_video, 
    '-vf', 'scale=600:400',
    os.path.join(output_folder, 'frame_%04d.png')
], check=True)  # Added check=True to raise an exception for non-zero exit codes

# Convert frames to binary images
for frame_file in sorted(os.listdir(output_folder)):
    if frame_file.endswith('.png'):
        img = Image.open(os.path.join(output_folder, frame_file)).convert('L')
        img_array = np.array(img)
        binary_array = (img_array < 128).astype(np.uint8)
        binary_img = Image.fromarray(binary_array * 255)
        binary_img.save(os.path.join(binary_folder, frame_file))

# Load binary frames
binary_frames = sorted([os.path.join(binary_folder, f) for f in os.listdir(binary_folder) if f.endswith('.png')])

frame_delay = 10  # Time in milliseconds between frames
key = cv2.waitKey(frame_delay)


# Read and display frames
frame_index = 0
while True:
    # Load current frame
    frame_file = binary_frames[frame_index]
    frame = cv2.imread(frame_file, cv2.IMREAD_GRAYSCALE)
    
    # Display the frame
    cv2.imshow('Binary Animation', frame)
    
    # Wait and handle key events
    key = cv2.waitKey(50)  # Adjust frame rate (50 ms between frames)
    if key == ord('q'):  # Press 'q' to quit
        break
    
    # Move to the next frame
    frame_index = (frame_index + 1) % len(binary_frames)

# Clean up
cv2.destroyAllWindows()










