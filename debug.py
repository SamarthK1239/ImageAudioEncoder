"""
Debug script to identify encoding/decoding issues
"""

from image_audio_encoder import ImageAudioEncoder
from PIL import Image
import numpy as np
import os

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Create a simple test image with known values
test_img = np.array([
    [0, 85, 170, 255],
    [50, 100, 150, 200],
    [25, 75, 125, 175],
    [10, 20, 30, 40]
], dtype=np.uint8)

img = Image.fromarray(test_img, mode='L')
img.save("output/test_input.png")

print("Original image:")
print(test_img)
print()

# Encode and decode
encoder = ImageAudioEncoder()
encoder.encode_image_to_audio("output/test_input.png", "output/test_audio.wav")
encoder.decode_audio_to_image("output/test_audio.wav", "output/test_output.png")

# Load decoded image
decoded_img = np.array(Image.open("output/test_output.png"))
print("\nDecoded image:")
print(decoded_img)
print()

# Calculate differences
diff = np.abs(test_img.astype(int) - decoded_img.astype(int))
print("\nAbsolute differences:")
print(diff)
print(f"\nMax error: {np.max(diff)}")
print(f"Mean error: {np.mean(diff):.2f}")
