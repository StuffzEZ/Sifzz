# Sifzz Sound Module

An **OFFICIAL** Sifzz module that provides cross-platform audio playback capabilities.

---

## Table of Contents

1. [Installation](#installation)
2. [Features](#features)
3. [Commands](#commands)
4. [Examples](#examples)
5. [Platform Support](#platform-support)
6. [Technical Details](#technical-details)
7. [Troubleshooting](#troubleshooting)

---

## Installation

1. Place `playSound.py` in your `modules/` directory
2. Dependencies will be automatically installed using PackageAPI:
   - pygame (audio playback)
   - numpy (beep generation)
   - requests (URL playback)

The module will be automatically loaded when you run Sifzz.

> **Offline Installation:**
>
> ```bash
> pip install pygame numpy requests
> ```

---

## Features

- 🔊 Cross-platform audio playback
- 🎵 Multiple audio format support (WAV, MP3, etc.)
- 🌐 URL streaming capability
- 🎛️ Volume control
- 📊 Audio file duration detection
- 🔔 Beep tone generation

---

## Commands

### Play Audio File

```
play sound "filename"
```

- Supports common audio formats (WAV, MP3, OGG, etc.)
- File path can be absolute or relative

### Play from URL

```
play url "url"
```

- Downloads and plays audio from web URLs
- Automatically cleans up temporary files

### Generate Beep

```
play beep frequency <freq> duration <dur>
```

- `freq`: Frequency in Hz (20-20000)
- `dur`: Duration in milliseconds

### Control Playback

```
stop sound
```

- Stops any currently playing audio

### Volume Control

```
set volume <0-100>
```

- Sets volume level (0-100%)

### Get Audio Duration

```
get duration "filename"
```

- Returns duration in seconds

---

## Examples

### Basic Audio Playback

```
# Play a local file
play sound "music.mp3"

# Adjust volume
set volume 75

# Check duration
get duration "music.mp3"
```

### Beep Sequence

```
# Play musical notes
play beep frequency 440 duration 500  # A4
play beep frequency 554 duration 500  # C#5
play beep frequency 659 duration 500  # E5
```

### URL Streaming

```
# Play from web
play url "https://example.com/audio.mp3"
```

---

## Platform Support

### Windows

- Full native support
- Uses WinSound for beep generation
- All features available

### macOS & Linux

- Full support via pygame
- Hardware-accelerated audio playback
- All features available

---

## Technical Details

### Audio Processing

- Threaded playback for non-blocking operation
- Automatic resource cleanup
- Cross-platform compatibility layer

### File Formats

- WAV: Highest compatibility
- MP3: Most common format
- OGG: Open format alternative
- Others supported by pygame

### Resource Management

- Automatic temporary file cleanup
- Memory-efficient streaming
- Thread safety measures

---

## Troubleshooting

### Common Issues

1. **No Sound Output**

   - Check system volume
   - Verify audio device
   - Ensure file format is supported

2. **URL Playback Fails**

   - Check internet connection
   - Verify URL is accessible
   - Ensure URL points to audio file

3. **Performance Issues**
   - Reduce audio file size
   - Use local files instead of URLs
   - Check system resources

### Error Messages

- `[ERROR] File not found`: Check file path
- `[ERROR] Failed to initialize audio`: Check audio device
- `[ERROR] Failed to play sound`: Check file format
- `[ERROR] Failed to play URL`: Check internet connection

---

## Best Practices

1. **File Formats**

   - Use WAV for best compatibility
   - Use MP3 for size efficiency
   - Test files before deployment

2. **Resource Management**

   - Stop sounds when not needed
   - Clean up temporary files
   - Use appropriate volume levels

3. **Error Handling**
   - Check file existence
   - Handle network errors
   - Provide user feedback

---

**Module Information**

- Version: 1.0
- Author: StuffzEZ/OptionallyBlueStudios
- License: GNU GPLv3
- Dependencies: pygame, numpy, requests
