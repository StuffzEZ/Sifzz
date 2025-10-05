"""
Sound Module for Sifzz
Provides audio playback capabilities using winsound

Commands:
- play beep frequency <freq> duration <dur>: Play a beep sound
- play sound "filename": Play .wav file
- stop sound: Stop currently playing sound
"""

import sys
import os
import winsound
import threading

# Add parent directory to sys.path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

try:
    from sifzz import SifzzModule
except ImportError as e:
    print(f"[ERROR] Could not import SifzzModule: {e}")
    raise

class SoundModule(SifzzModule):
    """Module for playing sounds"""
    
    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.current_thread = None
    
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
            "Play a .wav sound file"
        )
        
        self.register(
            r'stop sound',
            self.stop_sound,
            "Stop currently playing sound"
        )
    
    def play_beep(self, match):
        """Play a beep sound"""
        try:
            freq = int(match.group(1))
            duration = int(match.group(2))
            winsound.Beep(freq, duration)
        except Exception as e:
            print(f"[ERROR] Failed to play beep: {e}")
    
    def play_sound_file(self, match):
        """Play .wav sound file"""
        filepath = match.group(1)
        if not os.path.exists(filepath):
            print(f"[ERROR] File not found: {filepath}")
            return
            
        def play_thread():
            try:
                winsound.PlaySound(filepath, winsound.SND_FILENAME)
            except Exception as e:
                print(f"[ERROR] Failed to play sound: {e}")
        
        self.stop_sound(None)  # Stop any playing sound
        self.current_thread = threading.Thread(target=play_thread)
        self.current_thread.start()
    
    def stop_sound(self, match):
        """Stop currently playing sound"""
        winsound.PlaySound(None, winsound.SND_PURGE)