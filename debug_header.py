"""
Debug the header decoding specifically
"""

from image_audio_encoder import ImageAudioEncoder
from PIL import Image
import numpy as np
from scipy.io import wavfile
import os

# Ensure output directory exists
os.makedirs("output", exist_ok=True)

# Create encoder
encoder = ImageAudioEncoder()

# Test encoding just the header for a 4x4 image
print("Testing header encoding for 4x4 image...")
print(f"Width: 4, Height: 4")
print(f"Width bytes: high={4 >> 8}, low={4 & 0xFF}")
print(f"Height bytes: high={4 >> 8}, low={4 & 0xFF}")

# Create test image
test_img = np.ones((4, 4), dtype=np.uint8) * 128
img = Image.fromarray(test_img, mode='L')
img.save("output/test_header.png")

# Encode
encoder.encode_image_to_audio("output/test_header.png", "output/test_header.wav")

# Read audio
sample_rate, audio_data = wavfile.read("output/test_header.wav")
audio_data = audio_data.astype(np.float32) / 32767.0

print(f"\nAudio samples: {len(audio_data)}")
print(f"Samples per pixel: {encoder.samples_per_pixel}")
print(f"Header samples: {encoder.samples_per_pixel * 4}")

# Try to decode header manually
print("\nDecoding header manually...")
for i in range(4):
    start = i * encoder.samples_per_pixel
    end = start + encoder.samples_per_pixel
    segment = audio_data[start:end]
    value = encoder._decode_pixel(segment)
    print(f"Pulse {i}: decoded value = {value}")

# Reconstruct dimensions
width_high = encoder._decode_pixel(audio_data[0:encoder.samples_per_pixel])
width_low = encoder._decode_pixel(audio_data[encoder.samples_per_pixel:2*encoder.samples_per_pixel])
height_high = encoder._decode_pixel(audio_data[2*encoder.samples_per_pixel:3*encoder.samples_per_pixel])
height_low = encoder._decode_pixel(audio_data[3*encoder.samples_per_pixel:4*encoder.samples_per_pixel])

print(f"\nDecoded bytes:")
print(f"Width:  high={width_high}, low={width_low} -> {(width_high << 8) | width_low}")
print(f"Height: high={height_high}, low={height_low} -> {(height_high << 8) | height_low}")
