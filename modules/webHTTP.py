"""
This is an official Sifzz module!

Web/HTTP Module for Sifzz
Place this file in the modules/ directory

This module adds HTTP requests to Sifzz:
- get "http://example.com" and store in variable
- post "data" to "http://example.com" and store in variable
- download "http://example.com/file.zip" as "local.zip"
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sifzz import SifzzModule
import re

class WebModule(SifzzModule):
    """Adds HTTP/Web operations to Sifzz"""
    
    def register_commands(self):
        """Register all web operation commands"""
        
        # HTTP GET
        self.register(
            r'get "([^"]+)" and store in (\w+)',
            self.http_get,
            "Make HTTP GET request and store response"
        )
        
        # HTTP POST
        self.register(
            r'post "([^"]+)" to "([^"]+)" and store in (\w+)',
            self.http_post,
            "Make HTTP POST request with data"
        )
        
        # Download file
        self.register(
            r'download "([^"]+)" as "([^"]+)"',
            self.download_file,
            "Download a file from URL"
        )
        
        # Set HTTP timeout
        self.register(
            r'set http timeout to (\d+)',
            self.set_timeout,
            "Set HTTP request timeout in seconds"
        )
    
    def __init__(self, interpreter):
        super().__init__(interpreter)
        self.timeout = 10  # Default timeout
        
        # Try to import requests
        try:
            import requests
            self.requests = requests
            self.available = True
        except ImportError:
            print("[WARNING] Web module requires 'requests' library")
            print("          Install with: pip install requests")
            self.available = False
    
    def http_get(self, match):
        """Make HTTP GET request"""
        if not self.available:
            print("Error: requests library not available")
            return
        
        url = match.group(1)
        var_name = match.group(2)
        
        try:
            response = self.requests.get(url, timeout=self.timeout)
            self.interpreter.variables[var_name] = response.text
        except Exception as e:
            print(f"Error making GET request: {e}")
            self.interpreter.variables[var_name] = ""
    
    def http_post(self, match):
        """Make HTTP POST request"""
        if not self.available:
            print("Error: requests library not available")
            return
        
        data = match.group(1)
        url = match.group(2)
        var_name = match.group(3)
        
        try:
            response = self.requests.post(url, data=data, timeout=self.timeout)
            self.interpreter.variables[var_name] = response.text
        except Exception as e:
            print(f"Error making POST request: {e}")
            self.interpreter.variables[var_name] = ""
    
    def download_file(self, match):
        """Download file from URL"""
        if not self.available:
            print("Error: requests library not available")
            return
        
        url = match.group(1)
        filename = match.group(2)
        
        try:
            response = self.requests.get(url, timeout=self.timeout, stream=True)
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {filename}")
        except Exception as e:
            print(f"Error downloading file: {e}")
    
    def set_timeout(self, match):
        """Set HTTP timeout"""
        timeout = int(match.group(1))
        self.timeout = timeout
