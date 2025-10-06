"""
Enhanced Sound Module for Sifzz
Provides audio playback capabilities across platforms

Commands:
- play beep frequency <freq> duration <dur>: Play a beep sound
- play sound "filename": Play audio file (.wav, .mp3, etc)
- play url "url": Play audio from URL
- stop sound: Stop currently playing sound
- set volume <0-100>: Set playback volume (0-100%)
- get duration "filename": Get audio file duration in seconds
"""

import sys
import os
import threading
from urllib.parse import urlparse
from urllib.request import urlretrieve
import tempfile
import time

# Ignore PyGame warning- pygame devs need to fix that
os.environ['PYTHONWARNINGS'] = 'ignore::UserWarning:pygame.pkgdata'

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from sifzz import SifzzModule, PackageAPI, DEBUG_MODE
except ImportError as e:
    print(f"[ERROR] Could not import SifzzModule: {e}")
    raise


PackageAPI.getDependency('pygame')
PackageAPI.getDependency('numpy')  # Required for beep on non-Windows
PackageAPI.getDependency('requests')
import pygame.mixer
import numpy
import requests

class SoundModule(SifzzModule):
    """Enhanced cross-platform sound module"""
    
    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.current_thread = None
        self.volume = 100
        self.temp_files = []
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
            pygame.mixer.music.set_volume(self.volume / 100)
        except Exception as e:
            print(f"[ERROR] Failed to initialize audio: {e}")
    
    def __del__(self):
        """Cleanup temporary files"""
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"[WARNING] Failed to cleanup temp file {temp_file}: {e}")
    
    def register_commands(self):
        """Register sound commands"""
        self.register(
            r'play beep frequency (\d+) duration (\d+)',
            self.play_beep,
            "Play a beep with specified frequency and duration (ms)"
        )
        
        self.register(
            r'play sound "([^"]+)"',
            self.play_sound_file,
            "Play an audio file (supports various formats)"
        )
        
        self.register(
            r'play url "([^"]+)"',
            self.play_url,
            "Play audio from URL"
        )
        
        self.register(
            r'stop sound',
            self.stop_sound,
            "Stop currently playing sound"
        )
        
        self.register(
            r'set volume (\d+)',
            self.set_volume,
            "Set playback volume (0-100)"
        )
        
        self.register(
            r'get duration "([^"]+)"',
            self.get_duration,
            "Get audio file duration in seconds"
        )
    
    def play_beep(self, match):
        """Play a beep sound cross-platform"""
        try:
            freq = int(match.group(1))
            duration = int(match.group(2))
            
            if sys.platform == 'win32':
                import winsound
                winsound.Beep(freq, duration)
            else:
                # Use pygame for other platforms
                sample_rate = 44100
                t = numpy.linspace(0, duration/1000, int(duration * sample_rate/1000))
                wave = numpy.sin(2 * numpy.pi * freq * t)
                sound = numpy.asarray([32767 * wave] * 2).T.astype(numpy.int16)
                pygame.sndarray.make_sound(sound).play()
                time.sleep(duration/1000)
        except Exception as e:
            print(f"[ERROR] Failed to play beep: {e}")
    
    def play_sound_file(self, match):
        """Play audio file using pygame"""
        filepath = match.group(1)
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return
            
        def play_thread():
            try:
                pygame.mixer.music.load(filepath)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
            except Exception as e:
                print(f"[ERROR] Failed to play sound: {e}")
        
        self.stop_sound(None)
        self.current_thread = threading.Thread(target=play_thread)
        self.current_thread.start()
    
    def play_url(self, match):
        """Play audio from URL"""
        url = match.group(1)
        try:
            # Download to temporary file
            temp_file = tempfile.mktemp(suffix=os.path.splitext(urlparse(url).path)[1])
            if DEBUG_MODE:
                print(f"[INFO] Downloading {url}...")
            urlretrieve(url, temp_file)
            self.temp_files.append(temp_file)
            
            # Play the downloaded file
            self.play_sound_file(type('Match', (), {'group': lambda x: temp_file}))
        except Exception as e:
            print(f"[ERROR] Failed to play URL: {e}")
    
    def stop_sound(self, match):
        """Stop currently playing sound"""
        try:
            pygame.mixer.music.stop()
        except Exception as e:
            print(f"[ERROR] Failed to stop sound: {e}")
    
    def set_volume(self, match):
        """Set playback volume"""
        try:
            volume = int(match.group(1))
            if 0 <= volume <= 100:
                self.volume = volume
                pygame.mixer.music.set_volume(volume / 100)
            if DEBUG_MODE:
                print(f"[INFO] Volume set to {volume}%")
            else:
                print("[ERROR] Volume must be between 0 and 100")
        except Exception as e:
            print(f"[ERROR] Failed to set volume: {e}")
    
    def get_duration(self, match):
        """Get audio file duration in seconds"""
        filepath = match.group(1)
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return
            
        try:
            sound = pygame.mixer.Sound(filepath)
            duration = sound.get_length()
            print(f"Duration: {duration:.2f} seconds")
        except Exception as e:
            print(f"[ERROR] Failed to get duration: {e}")