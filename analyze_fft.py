"""
Analyze FFT resolution and frequency detection accuracy
"""

import numpy as np
from scipy.io import wavfile

# Test parameters
sample_rate = 44100
pixel_duration = 0.01  # Updated to 10ms
samples_per_pixel = int(sample_rate * pixel_duration)  # 441 samples

print(f"Samples per pixel: {samples_per_pixel}")
print(f"FFT will have {samples_per_pixel // 2 + 1} frequency bins")

# Calculate frequency resolution
freq_resolution = sample_rate / samples_per_pixel
print(f"Frequency resolution: {freq_resolution:.2f} Hz")

# Our frequency range is 500-2000 Hz
print(f"\nFrequency range: 500-2000 Hz (1500 Hz span)")
print(f"Number of distinguishable frequencies: {1500 / freq_resolution:.1f}")
print(f"This means we can only distinguish ~{int(1500 / freq_resolution)} different pixel values!")
print(f"\nWe need 256 different frequencies for 8-bit pixels")
print(f"Required frequency resolution: {1500 / 256:.2f} Hz")
print(f"Required samples per pixel: {int(sample_rate / (1500 / 256))}")
