"""
Compare original and decoded images
"""

from PIL import Image
import numpy as np

# Load images
original = np.array(Image.open("output/sample_image.png"))
decoded = np.array(Image.open("output/decoded_image.png"))

print("Image Comparison:")
print("=" * 50)
print(f"Original shape: {original.shape}")
print(f"Decoded shape:  {decoded.shape}")
print()

if original.shape == decoded.shape:
    diff = np.abs(original.astype(int) - decoded.astype(int))
    
    print(f"Max error:  {np.max(diff)} pixels")
    print(f"Mean error: {np.mean(diff):.3f} pixels")
    print(f"Pixels with error > 0: {np.sum(diff > 0)} / {diff.size} ({100*np.sum(diff > 0)/diff.size:.2f}%)")
    print()
    
    if np.max(diff) == 0:
        print("✓ Perfect match! Images are identical.")
    elif np.max(diff) <= 1:
        print("✓ Excellent! Maximum error is only 1 pixel value.")
    elif np.max(diff) <= 5:
        print("✓ Good! Maximum error is within acceptable range (≤5).")
    else:
        print("⚠ Significant differences detected.")
else:
    print("⚠ Images have different dimensions!")
