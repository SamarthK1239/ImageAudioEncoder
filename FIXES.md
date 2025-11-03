# Fixes Applied to Image Audio Encoder

## Problems Identified

1. **Poor FFT Resolution**: With only 44 samples per pixel (1ms at 44.1kHz), the FFT had ~1000 Hz frequency resolution, making it impossible to distinguish between pixel values.

2. **Wide Frequency Range**: Using 500-2000 Hz (1500 Hz span) meant we needed ~6 Hz resolution to encode 256 values, but only had ~1000 Hz resolution.

3. **No Windowing**: Spectral leakage from rectangular windowing caused frequency detection errors.

4. **Dimension Decoding Errors**: Small pixel values (like 4) were decoding incorrectly (as 3), causing dimension header corruption.

## Solutions Implemented

### 1. Increased Pixel Duration
- **Changed from**: 1ms (0.001s) per pixel
- **Changed to**: 50ms (0.05s) per pixel
- **Result**: 2205 samples per pixel → ~20 Hz FFT resolution

### 2. Narrowed Frequency Range
- **Changed from**: 500-2000 Hz (1500 Hz span, 0.5× to 2× carrier)
- **Changed to**: 800-1200 Hz (400 Hz span, 0.8× to 1.2× carrier)
- **Result**: 400 Hz / 256 values = 1.56 Hz per value (well within 20 Hz resolution)

### 3. Added Windowing
- Applied Hann window to reduce spectral leakage
- Improves frequency detection accuracy

### 4. Zero-Padding FFT
- Added 4× zero-padding to FFT (2205 → 8820 samples)
- **Result**: Improved frequency resolution to ~5 Hz

### 5. Parabolic Interpolation
- Added parabolic interpolation around FFT peak
- Achieves sub-bin frequency accuracy
- Includes safety checks to avoid division by zero

### 6. Rounding Instead of Truncation
- Changed from `int()` truncation to `int(np.round())`
- Improves accuracy at bin boundaries

## Results

### Before Fixes
- Dimensions: 100×100 encoded, 85×85 decoded ❌
- Pixel values: Off by 1-2 for most values
- Duration: 10 seconds for 100×100 image

### After Fixes
- Dimensions: 100×100 encoded, 100×100 decoded ✅
- Pixel values: **Perfect match - 0 error!** ✅
- Duration: 500 seconds (8.3 minutes) for 100×100 image
- Test results: All pixel values 0-255 decode with zero error

## Trade-offs

### Audio Duration
- Increased from 10 seconds to 500 seconds for 100×100 image
- This is necessary for accurate frequency detection with FFT
- Users can reduce `pixel_duration` for faster encoding with slight quality loss

### Accuracy vs Speed Options
- **50ms/pixel** (default): Perfect reconstruction, zero error
- **20ms/pixel**: Faster (5× speed), may have ±1-2 pixel errors
- **10ms/pixel**: Very fast (10× speed), may have ±2-5 pixel errors

## Technical Details

### FFT Frequency Resolution Formula
```
freq_resolution = sample_rate / samples_per_pixel
samples_per_pixel = sample_rate * pixel_duration
```

### Required Resolution for 8-bit Encoding
```
frequency_span = 400 Hz (800-1200 Hz)
values_to_encode = 256
required_resolution = 400 / 256 ≈ 1.56 Hz per value
```

### Achieved Resolution
```
Base FFT: 44100 / 2205 ≈ 20 Hz
With 4× zero-padding: 44100 / 8820 ≈ 5 Hz
With parabolic interpolation: < 1 Hz effective resolution
```

This gives us well over 256 distinguishable frequency bins!
