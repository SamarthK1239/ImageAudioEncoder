"""
Example usage of the Image Audio Encoder
Demonstrates encoding an image to audio and decoding it back
"""

from image_audio_encoder import ImageAudioEncoder
from PIL import Image
import numpy as np
import os


def create_sample_image(filename: str = "output/sample_image.png", width: int = 100, height: int = 100):
    """
    Create a simple test image with a gradient pattern.
    
    Args:
        filename: Output filename for the sample image
        width: Width of the image
        height: Height of the image
    """
    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)
    
    # Create a gradient pattern
    img_array = np.zeros((height, width), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            # Create a circular gradient pattern
            center_x, center_y = width // 2, height // 2
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            max_distance = np.sqrt(center_x**2 + center_y**2)
            value = int(255 * (1 - distance / max_distance))
            img_array[y, x] = value
    
    # Save the image
    img = Image.fromarray(img_array, mode='L')
    img.save(filename)
    print(f"Created sample image: {filename}")
    return filename


def main():
    print("=" * 60)
    print("Image Audio Encoder - Example Usage")
    print("Inspired by NASA's Golden Records")
    print("=" * 60)
    
    # Create an encoder instance
    encoder = ImageAudioEncoder(
        sample_rate=44100,      # CD quality audio
        carrier_freq=1000.0,    # 1kHz carrier frequency
        pixel_duration=0.05     # 50ms per pixel (balanced speed/accuracy)
    )
    
    # Step 1: Create a sample image (or use your own)
    print("\n[Step 1] Creating sample image...")
    sample_image = create_sample_image("output/sample_image.png", width=50, height=50)
    
    # Step 2: Encode the image to audio
    print("\n[Step 2] Encoding image to audio...")
    width, height = encoder.encode_image_to_audio(
        image_path=sample_image,
        output_audio_path="output/encoded_image.wav"
    )
    print(f"✓ Encoded {width}x{height} image to 'output/encoded_image.wav'")
    
    # Step 3: Decode the audio back to an image
    print("\n[Step 3] Decoding audio back to image...")
    width, height = encoder.decode_audio_to_image(
        audio_path="output/encoded_image.wav",
        output_image_path="output/decoded_image.png"
    )
    print(f"✓ Decoded audio to {width}x{height} image: 'output/decoded_image.png'")
    
    print("\n" + "=" * 60)
    print("✓ Complete! Check the generated files in the 'output' folder:")
    print("  - output/sample_image.png    (original)")
    print("  - output/encoded_image.wav   (audio representation)")
    print("  - output/decoded_image.png   (reconstructed)")
    print("\nYou can listen to the audio file to hear the encoded image!")
    print("=" * 60)
    
    # Example with your own image
    print("\n" + "=" * 60)
    print("To use with your own image:")
    print("=" * 60)
    print("""
from image_audio_encoder import ImageAudioEncoder

encoder = ImageAudioEncoder()

# Encode
encoder.encode_image_to_audio('my_photo.jpg', 'my_photo.wav')

# Decode
encoder.decode_audio_to_image('my_photo.wav', 'recovered_photo.png')
""")


if __name__ == "__main__":
    main()
