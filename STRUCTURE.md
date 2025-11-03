# Project Structure

```
ImageAudioEncoder/
├── .gitignore                    # Git ignore file (excludes output/ and cache)
├── README.md                     # Main project documentation
├── requirements.txt              # Python dependencies
├── FIXES.md                      # Documentation of bug fixes
│
├── image_audio_encoder.py        # Main encoder/decoder class
├── example.py                    # Example usage demonstration
│
├── test_values.py                # Test individual pixel value encoding/decoding
├── debug.py                      # Debug script for testing small images
├── debug_header.py               # Debug script for header encoding
├── compare_images.py             # Compare original vs decoded images
├── analyze_fft.py                # FFT resolution analysis tool
│
└── output/                       # All generated files go here
    ├── README.md                 # Documentation for output folder
    ├── sample_image.png          # Generated test image
    ├── encoded_image.wav         # Encoded audio file
    ├── decoded_image.png         # Decoded image
    └── [test files...]           # Debug/test outputs
```

## Clean Directory Structure

All generated files (images and audio) are now stored in the `output/` folder:
- Keeps the project root clean and organized
- Easy to find all generated content in one place
- `.gitignore` excludes the output folder from version control
- Scripts automatically create the `output/` directory if it doesn't exist

## Running the Example

```bash
python example.py
```

This will create:
- `output/sample_image.png`
- `output/encoded_image.wav`
- `output/decoded_image.png`

All scripts have been updated to read from and write to the `output/` folder.
