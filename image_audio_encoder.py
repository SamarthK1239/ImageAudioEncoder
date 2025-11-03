"""
Image to Audio Encoder/Decoder
Inspired by NASA's Golden Records

This module encodes grayscale images into analog audio signals and decodes them back.
The audio represents pixel intensities as frequency-modulated signals, similar to 
analog television and the Voyager Golden Record encoding.
"""

import numpy as np
from PIL import Image
from scipy.io import wavfile
from typing import Tuple


class ImageAudioEncoder:
    """Encodes grayscale images to audio files and decodes them back."""
    
    def __init__(self, sample_rate: int = 44100, carrier_freq: float = 1000.0, 
                 pixel_duration: float = 0.05):
        """
        Initialize the encoder/decoder.
        
        Args:
            sample_rate: Audio sample rate in Hz (default: 44100)
            carrier_freq: Base carrier frequency in Hz (default: 1000)
            pixel_duration: Duration of each pixel in seconds (default: 0.05 = 50ms)
        """
        self.sample_rate = sample_rate
        self.carrier_freq = carrier_freq
        self.pixel_duration = pixel_duration
        self.samples_per_pixel = int(sample_rate * pixel_duration)
        
    def encode_image_to_audio(self, image_path: str, output_audio_path: str) -> Tuple[int, int]:
        """
        Encode a grayscale image into an audio file.
        
        The encoding works by:
        1. Converting image to grayscale
        2. Adding sync pulses at the start for width/height information
        3. Converting each pixel value to a frequency (darker = lower, brighter = higher)
        4. Generating audio waveform
        
        Args:
            image_path: Path to input image file
            output_audio_path: Path to output WAV file
            
        Returns:
            Tuple of (image_width, image_height)
        """
        # Load and convert image to grayscale
        img = Image.open(image_path).convert('L')
        width, height = img.size
        pixels = np.array(img)
        
        print(f"Encoding image: {width}x{height} pixels")
        
        # Create header with sync pulses for dimensions
        header = self._create_header(width, height)
        
        # Flatten pixel data (row by row)
        pixel_data = pixels.flatten()
        
        # Generate audio signal for pixel data
        audio_signal = []
        
        # Add header
        audio_signal.extend(header)
        
        # Encode each pixel as frequency modulation
        for pixel_value in pixel_data:
            pixel_audio = self._encode_pixel(pixel_value)
            audio_signal.extend(pixel_audio)
        
        # Convert to numpy array and normalize
        audio_signal = np.array(audio_signal, dtype=np.float32)
        
        # Normalize to 16-bit integer range
        audio_signal_int = np.int16(audio_signal * 32767)
        
        # Write to WAV file
        wavfile.write(output_audio_path, self.sample_rate, audio_signal_int)
        
        print(f"Audio file created: {output_audio_path}")
        print(f"Duration: {len(audio_signal) / self.sample_rate:.2f} seconds")
        
        return width, height
    
    def decode_audio_to_image(self, audio_path: str, output_image_path: str) -> Tuple[int, int]:
        """
        Decode an audio file back into a grayscale image.
        
        Args:
            audio_path: Path to input WAV file
            output_image_path: Path to output image file
            
        Returns:
            Tuple of (image_width, image_height)
        """
        # Read audio file
        sample_rate, audio_data = wavfile.read(audio_path)
        
        if sample_rate != self.sample_rate:
            print(f"Warning: Audio sample rate ({sample_rate}) differs from encoder rate ({self.sample_rate})")
            self.sample_rate = sample_rate
            self.samples_per_pixel = int(sample_rate * self.pixel_duration)
        
        # Normalize audio data to [-1, 1]
        audio_data = audio_data.astype(np.float32) / 32767.0
        
        # Decode header to get dimensions
        width, height = self._decode_header(audio_data)
        print(f"Decoding image: {width}x{height} pixels")
        
        # Calculate header length
        header_samples = self.samples_per_pixel * 4  # 4 sync pulses for dimensions
        
        # Extract pixel data portion
        pixel_audio = audio_data[header_samples:]
        
        # Decode each pixel
        num_pixels = width * height
        pixels = []
        
        for i in range(num_pixels):
            start_idx = i * self.samples_per_pixel
            end_idx = start_idx + self.samples_per_pixel
            
            if end_idx > len(pixel_audio):
                break
                
            pixel_segment = pixel_audio[start_idx:end_idx]
            pixel_value = self._decode_pixel(pixel_segment)
            pixels.append(pixel_value)
        
        # Reshape to image dimensions
        pixels = np.array(pixels[:num_pixels], dtype=np.uint8)
        pixels = pixels.reshape((height, width))
        
        # Create and save image
        img = Image.fromarray(pixels, mode='L')
        img.save(output_image_path)
        
        print(f"Image decoded: {output_image_path}")
        
        return width, height
    
    def _create_header(self, width: int, height: int) -> list:
        """Create header with sync pulses encoding image dimensions."""
        header = []
        
        # Encode width (2 sync pulses)
        header.extend(self._encode_dimension(width))
        
        # Encode height (2 sync pulses)
        header.extend(self._encode_dimension(height))
        
        return header
    
    def _encode_dimension(self, value: int) -> list:
        """Encode a dimension value as two frequency pulses (high and low bytes)."""
        # Split into high and low bytes (supports up to 65535)
        high_byte = (value >> 8) & 0xFF
        low_byte = value & 0xFF
        
        signal = []
        signal.extend(self._encode_pixel(high_byte))
        signal.extend(self._encode_pixel(low_byte))
        
        return signal
    
    def _decode_header(self, audio_data: np.ndarray) -> Tuple[int, int]:
        """Decode header to extract image dimensions."""
        # Decode width (first 2 pulses)
        width_high = self._decode_pixel(audio_data[0:self.samples_per_pixel])
        width_low = self._decode_pixel(audio_data[self.samples_per_pixel:2*self.samples_per_pixel])
        width = (width_high << 8) | width_low
        
        # Decode height (next 2 pulses)
        height_high = self._decode_pixel(audio_data[2*self.samples_per_pixel:3*self.samples_per_pixel])
        height_low = self._decode_pixel(audio_data[3*self.samples_per_pixel:4*self.samples_per_pixel])
        height = (height_high << 8) | height_low
        
        return width, height
    
    def _encode_pixel(self, pixel_value: int) -> np.ndarray:
        """
        Encode a single pixel value (0-255) as a frequency-modulated audio segment.
        
        Lower pixel values (darker) = lower frequency
        Higher pixel values (brighter) = higher frequency
        """
        # Map pixel value (0-255) to frequency range
        # Use range from 0.8x to 1.2x the carrier frequency (narrower for better resolution)
        freq_min = self.carrier_freq * 0.8
        freq_max = self.carrier_freq * 1.2
        frequency = freq_min + (pixel_value / 255.0) * (freq_max - freq_min)
        
        # Generate time array for this pixel
        t = np.linspace(0, self.pixel_duration, self.samples_per_pixel, endpoint=False)
        
        # Generate sine wave at the calculated frequency
        signal = np.sin(2 * np.pi * frequency * t)
        
        return signal
    
    def _decode_pixel(self, audio_segment: np.ndarray) -> int:
        """
        Decode a pixel value from an audio segment by detecting its frequency.
        
        Uses FFT with windowing and zero-padding to find the dominant frequency and map it back to pixel value.
        """
        # Apply Hann window to reduce spectral leakage
        window = np.hanning(len(audio_segment))
        windowed_signal = audio_segment * window
        
        # Zero-pad to increase FFT resolution (4x padding)
        n_fft = len(audio_segment) * 4
        
        # Perform FFT to find dominant frequency
        fft = np.fft.rfft(windowed_signal, n=n_fft)
        freqs = np.fft.rfftfreq(n_fft, 1/self.sample_rate)
        
        # Find frequency with maximum magnitude (skip DC component at index 0)
        magnitude = np.abs(fft)
        # Skip DC component (index 0) when finding max
        dominant_freq_idx = np.argmax(magnitude[1:]) + 1
        dominant_freq = freqs[dominant_freq_idx]
        
        # Optional: Use parabolic interpolation for better frequency estimate
        if 1 < dominant_freq_idx < len(magnitude) - 1:
            # Get magnitude values around the peak
            alpha = magnitude[dominant_freq_idx - 1]
            beta = magnitude[dominant_freq_idx]
            gamma = magnitude[dominant_freq_idx + 1]
            
            # Parabolic interpolation (with safety check for division)
            denom = alpha - 2*beta + gamma
            if abs(denom) > 1e-10:  # Avoid division by zero
                p = 0.5 * (alpha - gamma) / denom
                
                # Adjust frequency estimate
                freq_bin_width = freqs[1] - freqs[0]
                dominant_freq = freqs[dominant_freq_idx] + p * freq_bin_width
        
        # Map frequency back to pixel value
        freq_min = self.carrier_freq * 0.8
        freq_max = self.carrier_freq * 1.2
        
        # Clamp frequency to expected range
        dominant_freq = np.clip(dominant_freq, freq_min, freq_max)
        
        # Calculate pixel value with rounding for better accuracy
        pixel_value = ((dominant_freq - freq_min) / (freq_max - freq_min)) * 255.0
        pixel_value = int(np.round(np.clip(pixel_value, 0, 255)))
        
        return pixel_value


def main():
    """Example usage of the ImageAudioEncoder."""
    encoder = ImageAudioEncoder(
        sample_rate=44100,
        carrier_freq=1000.0,
        pixel_duration=0.001  # 1ms per pixel
    )
    
    # Example: Encode an image
    print("=" * 50)
    print("Image to Audio Encoder - NASA Golden Records Style")
    print("=" * 50)
    print("\nUsage:")
    print("  Encode: encoder.encode_image_to_audio('input.jpg', 'output.wav')")
    print("  Decode: encoder.decode_audio_to_image('output.wav', 'decoded.jpg')")
    print("\nReady to encode/decode images!")


if __name__ == "__main__":
    main()
