# Image Audio Encoder

**Encode images into analog audio files and decode them back - Inspired by NASA's Golden Records!**

This Python application converts grayscale images into audio waveforms using frequency modulation, similar to how images were encoded on the Voyager Golden Records sent into space in 1977. Each pixel's brightness is represented as a specific audio frequency, creating an audible representation of visual data.

## 🌟 Features

- **Image to Audio Encoding**: Convert any image to a single-channel (mono) audio file
- **Audio to Image Decoding**: Reconstruct images from encoded audio files
- **Grayscale Support**: Works with grayscale images for single-channel encoding
- **Frequency Modulation**: Uses FM techniques similar to analog television and NASA's Golden Records
- **Customizable Parameters**: Adjust sample rate, carrier frequency, and pixel duration

## 🔧 Installation

1. Clone this repository:
```bash
git clone https://github.com/SamarthK1239/ImageAudioEncoder.git
cd ImageAudioEncoder
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Requirements
- Python 3.7+
- NumPy
- Pillow (PIL)
- SciPy

## 🚀 Quick Start

### Run the Example

```bash
python example.py
```

This will:
1. Create a sample gradient image
2. Encode it to an audio file (`encoded_image.wav`)
3. Decode the audio back to an image (`decoded_image.png`)

### Use with Your Own Images

```python
from image_audio_encoder import ImageAudioEncoder

# Create encoder instance
from image_audio_encoder import ImageAudioEncoder

# Create encoder instance
encoder = ImageAudioEncoder(
    sample_rate=44100,      # Audio sample rate (Hz)
    carrier_freq=1000.0,    # Base carrier frequency (Hz)
    pixel_duration=0.05     # Duration per pixel (seconds)
)

# Encode an image to audio
encoder.encode_image_to_audio('my_photo.jpg', 'output/my_photo.wav')

# Decode audio back to image
encoder.decode_audio_to_image('output/my_photo.wav', 'output/recovered_photo.png')
```

**Note**: All output files (audio and images) are saved to the `output/` folder by default.

## 📖 How It Works

### Encoding Process

1. **Image Conversion**: The input image is converted to grayscale
2. **Header Creation**: Sync pulses encode the image dimensions (width and height)
3. **Pixel Encoding**: Each pixel value (0-255) is mapped to a frequency:
   - Darker pixels (lower values) → Lower frequencies
   - Brighter pixels (higher values) → Higher frequencies
4. **Audio Generation**: A sine wave is generated for each pixel at its corresponding frequency
5. **WAV Export**: The complete audio signal is saved as a WAV file

### Decoding Process

1. **Audio Import**: Read the WAV file
2. **Header Decoding**: Extract image dimensions from sync pulses
3. **Frequency Analysis**: Use FFT to detect the dominant frequency in each pixel segment
4. **Pixel Recovery**: Map frequencies back to pixel values (0-255)
5. **Image Reconstruction**: Reshape pixel array to original dimensions and save

### Frequency Modulation

- **Carrier Frequency**: Base frequency (default: 1kHz)
- **Frequency Range**: 0.8× to 1.2× carrier frequency (800 Hz - 1200 Hz)
- **Pixel Mapping**: Linear mapping from pixel value to frequency
- **FFT Resolution**: Uses zero-padding (4x) and parabolic interpolation for accurate frequency detection

## 🎨 Example Output

When you run the example, you'll get files in the `output/` folder:
- `output/sample_image.png` - Original grayscale image (50×50 pixels)
- `output/encoded_image.wav` - Audio file (~2 minutes for 50×50 image)
- `output/decoded_image.png` - Reconstructed image (perfect quality!)

You can actually **listen** to what an image sounds like! Different patterns create different audio characteristics.

## 🎛️ Customization

### Adjusting Parameters

```python
encoder = ImageAudioEncoder(
    sample_rate=44100,      # Higher = better quality, larger files
    carrier_freq=1000.0,    # Center frequency for encoding
    pixel_duration=0.05     # Duration per pixel (default: 50ms)
)
```

**Trade-offs:**
- Higher `sample_rate`: Better frequency resolution but larger files
- Longer `pixel_duration`: More accurate encoding/decoding but longer audio duration
  - **Minimum recommended**: 0.05s (50ms) for accurate 8-bit reconstruction
  - **Faster (lower quality)**: 0.02s (20ms) - may have ±1-2 pixel errors
  - **Perfect accuracy**: 0.05s+ (50ms+) - zero error reconstruction
- Higher `carrier_freq`: Moves audio to a different frequency range

### Image Size Considerations

- A 100×100 pixel image takes ~500 seconds (8 minutes) of audio at 50ms/pixel
- A 50×50 pixel image takes ~125 seconds (2 minutes)  
- A 200×200 pixel image takes ~2000 seconds (33 minutes)
- For faster encoding, reduce pixel_duration (with slight quality trade-off)
- Consider resizing large images before encoding

## 🔬 Technical Details

### Encoding Specification

- **Audio Format**: Mono WAV, 16-bit PCM
- **Default Sample Rate**: 44.1 kHz (CD quality)
- **Frequency Range**: 800 Hz - 1200 Hz (0.8× to 1.2× carrier frequency)
- **Pixel Duration**: 50 milliseconds per pixel (default)
- **Header Format**: 4 sync pulses (width high/low, height high/low)
- **FFT Enhancement**: 4× zero-padding + parabolic interpolation for sub-bin accuracy

### Limitations

- Maximum image dimensions: 65,535 × 65,535 pixels (16-bit encoding)
- Color images are converted to grayscale
- Audio duration scales linearly with pixel count
- With proper settings (50ms+ pixel duration), achieves perfect 8-bit reconstruction

## 🌌 Inspiration: NASA's Golden Records

The Voyager Golden Records contained 115 images encoded as audio, using a technique similar to this project. The records included:
- Instructions for playback
- Scientific information
- Images of Earth and humanity
- Sounds and music from Earth

This project recreates that fascinating encoding technique using modern Python!

## 📝 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 🔮 Future Enhancements

- [ ] RGB color encoding (3-channel audio)
- [ ] Error correction and noise reduction
- [ ] Compression techniques for shorter audio
- [ ] Real-time visualization during encoding/decoding
- [ ] Support for other audio formats (MP3, FLAC)
- [ ] GUI application

## 📧 Contact

Created by [@SamarthK1239](https://github.com/SamarthK1239)

---

*"The spacecraft will be encountered and the record played only if there are advanced space-faring civilizations in interstellar space."* - Carl Sagan
