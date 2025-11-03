"""
Test encoding and decoding of specific values
"""

from image_audio_encoder import ImageAudioEncoder
import numpy as np

encoder = ImageAudioEncoder()

# Test specific values
test_values = [0, 1, 2, 3, 4, 5, 10, 20, 50, 100, 150, 200, 250, 255]

print("Testing encoding/decoding of specific values:")
print("Value -> Encoded Freq -> Decoded Value")
print("-" * 50)

for val in test_values:
    # Encode
    audio = encoder._encode_pixel(val)
    
    # Calculate actual frequency
    freq_min = encoder.carrier_freq * 0.8
    freq_max = encoder.carrier_freq * 1.2
    expected_freq = freq_min + (val / 255.0) * (freq_max - freq_min)
    
    # Decode
    decoded = encoder._decode_pixel(audio)
    
    print(f"{val:3d} -> {expected_freq:7.2f} Hz -> {decoded:3d}  (error: {decoded - val:+d})")
