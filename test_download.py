#!/usr/bin/env python3
import yt_dlp
import tempfile
import os

def test_download(url):
    """Test function to verify yt-dlp works"""
    try:
        # Create temp directory
        temp_dir = tempfile.mkdtemp()
        print(f"Using temp directory: {temp_dir}")
        
        # Configure yt-dlp
        ydl_opts = {
            'format': 'best[height<=480]',  # Low quality for testing
            'outtmpl': os.path.join(temp_dir, '%(title)s.%(ext)s'),
            'quiet': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print("Extracting info...")
            info = ydl.extract_info(url, download=False)
            print(f"Title: {info.get('title')}")
            print(f"Duration: {info.get('duration')} seconds")
            
            print("Starting download...")
            ydl.download([url])
            
            # Check if file exists
            files = os.listdir(temp_dir)
            if files:
                print(f"Downloaded: {files[0]}")
                file_path = os.path.join(temp_dir, files[0])
                file_size = os.path.getsize(file_path)
                print(f"File size: {file_size / (1024*1024):.1f} MB")
                
                # Cleanup
                os.remove(file_path)
                os.rmdir(temp_dir)
                return True
            else:
                print("No file downloaded")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    # Test with a short video
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Roll (short video)
    print("Testing yt-dlp download...")
    success = test_download(test_url)
    print(f"Test {'PASSED' if success else 'FAILED'}")