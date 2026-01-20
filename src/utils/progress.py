"""
Progress bar utility for file transfers
"""

import sys
import time

class ProgressBar:
    """Terminal progress bar with upload/download tracking"""
    
    def __init__(self, total, description="Progress", bar_length=40):
        self.total = total
        self.description = description
        self.bar_length = bar_length
        self.current = 0
        self.start_time = time.time()
        
    def update(self, current):
        """Update progress bar"""
        self.current = current
        
        # Calculate percentage
        percent = (current / self.total) * 100
        
        # Calculate filled length
        filled = int(self.bar_length * current / self.total)
        bar = '█' * filled + '░' * (self.bar_length - filled)
        
        # Calculate speed and ETA
        elapsed = time.time() - self.start_time
        if elapsed > 0 and current > 0:
            speed = current / elapsed
            eta = (self.total - current) / speed if speed > 0 else 0
            eta_str = self._format_time(eta)
            speed_str = f"{speed:.1f} packets/s"
        else:
            eta_str = "--:--"
            speed_str = "-- packets/s"
        
        # Print progress bar
        sys.stdout.write(f'\r{self.description}: |{bar}| {percent:.1f}% | {speed_str} | ETA: {eta_str}')
        sys.stdout.flush()
    
    def finish(self):
        """Complete progress bar"""
        elapsed = time.time() - self.start_time
        elapsed_str = self._format_time(elapsed)
        
        filled_bar = '█' * self.bar_length
        sys.stdout.write(f'\r{self.description}: |{filled_bar}| 100.0% | Completed in {elapsed_str}\n')
        sys.stdout.flush()
    
    def _format_time(self, seconds):
        """Format seconds to MM:SS"""
        if seconds < 0:
            return "--:--"
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"