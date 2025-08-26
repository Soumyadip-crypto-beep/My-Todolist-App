import os
import tempfile
import re
from flask import Response, jsonify

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

class YouTubeDownloader:
    def __init__(self):
        self.yt_dlp = yt_dlp
    
    def is_available(self):
        return self.yt_dlp is not None
    
    def get_video_info(self, url):
        """Extract video information without downloading"""
        if not self.yt_dlp:
            return {
                'success': True,
                'title': 'Demo Video - yt-dlp not installed',
                'thumbnail': 'https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg',
                'formats': [
                    {'quality': '720p', 'size': '~25 MB', 'format': 'mp4', 'format_id': 'demo_720p'},
                    {'quality': '480p', 'size': '~15 MB', 'format': 'mp4', 'format_id': 'demo_480p'},
                    {'quality': 'Audio Only', 'size': '~3 MB', 'format': 'mp3', 'format_id': 'demo_audio'}
                ],
                'video_id': 'demo'
            }
        
        try:
            ydl_opts = {'quiet': True, 'no_warnings': True}
            
            with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                formats = []
                seen_qualities = set()
                
                # Get video formats
                for f in info.get('formats', []):
                    if f.get('vcodec') != 'none' and f.get('height'):
                        quality = f"{f['height']}p"
                        if quality not in seen_qualities and f.get('filesize'):
                            formats.append({
                                'quality': quality,
                                'size': f"{f['filesize'] / (1024*1024):.1f} MB",
                                'format': f.get('ext', 'mp4'),
                                'format_id': f['format_id']
                            })
                            seen_qualities.add(quality)
                
                # Add audio-only option
                audio_formats = [f for f in info.get('formats', []) if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                if audio_formats:
                    best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
                    size_mb = best_audio.get('filesize', 0) / (1024*1024) if best_audio.get('filesize') else 3
                    formats.append({
                        'quality': 'Audio Only',
                        'size': f"{size_mb:.1f} MB",
                        'format': 'mp3',
                        'format_id': best_audio['format_id']
                    })
                
                # Fallback formats if none found
                if not formats:
                    formats = [
                        {'quality': '720p', 'size': '~25 MB', 'format': 'mp4', 'format_id': 'best[height<=720]'},
                        {'quality': '480p', 'size': '~15 MB', 'format': 'mp4', 'format_id': 'best[height<=480]'},
                        {'quality': 'Audio Only', 'size': '~3 MB', 'format': 'mp3', 'format_id': 'bestaudio'}
                    ]
                
                return {
                    'success': True,
                    'title': info.get('title', 'Unknown Title'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'formats': formats[:4],
                    'video_id': info.get('id', '')
                }
                
        except Exception as e:
            return {'success': False, 'error': f'Failed to analyze video: {str(e)}'}
    
    def download_file(self, url, format_id):
        """Download video/audio file and return Flask Response"""
        if not self.yt_dlp:
            return jsonify({
                'success': False,
                'error': 'yt-dlp not installed',
                'redirect_url': url,
                'message': 'Please install yt-dlp: pip install yt-dlp'
            })
        
        try:
            temp_dir = tempfile.mkdtemp()
            
            # Format selection
            format_selector = self._get_format_selector(format_id)
            
            # Configure yt-dlp with merging support
            ydl_opts = {
                'format': format_selector,
                'outtmpl': os.path.join(temp_dir, 'download.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
                'merge_output_format': 'mp4',  # Force merge to MP4
            }
            
            # Add audio extraction for audio-only downloads
            if 'audio' in format_id or format_id == 'bestaudio':
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '128',
                }]
            
            # Download
            with self.yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Find downloaded file
            files = os.listdir(temp_dir)
            if not files:
                return jsonify({'success': False, 'error': 'No file downloaded'})
            
            file_path = os.path.join(temp_dir, files[0])
            
            # Read file content
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Cleanup
            os.remove(file_path)
            os.rmdir(temp_dir)
            
            # Prepare response
            mime_type = self._get_mime_type(files[0])
            safe_filename = self._sanitize_filename(files[0])
            
            return Response(
                file_data,
                mimetype=mime_type,
                headers={
                    'Content-Disposition': f'attachment; filename="{safe_filename}"',
                    'Content-Length': str(len(file_data)),
                    'Accept-Ranges': 'bytes'
                }
            )
            
        except Exception as e:
            return jsonify({'success': False, 'error': f'Download failed: {str(e)}'})
    
    def _get_format_selector(self, format_id):
        """Get appropriate format selector with video+audio merging"""
        if format_id.startswith('demo_'):
            if 'audio' in format_id:
                return 'bestaudio'
            elif '720p' in format_id:
                return 'best[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]'
            elif '480p' in format_id:
                return 'best[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]'
            else:
                return 'best[ext=mp4]+bestaudio[ext=m4a]/best'
        else:
            # For real format IDs, ensure video+audio merge
            if 'audio' not in format_id and format_id != 'bestaudio':
                return f'{format_id}+bestaudio/best'
            return format_id
    
    def _get_mime_type(self, filename):
        """Get MIME type based on file extension"""
        file_ext = os.path.splitext(filename)[1].lower()
        mime_types = {
            '.mp4': 'video/mp4',
            '.webm': 'video/webm',
            '.mkv': 'video/x-matroska',
            '.mp3': 'audio/mpeg',
            '.m4a': 'audio/mp4',
            '.ogg': 'audio/ogg'
        }
        return mime_types.get(file_ext, 'application/octet-stream')
    
    def _sanitize_filename(self, filename):
        """Sanitize filename for HTTP headers"""
        base_name = os.path.splitext(filename)[0]
        file_ext = os.path.splitext(filename)[1]
        
        safe_base = re.sub(r'[^\w\s-]', '', base_name).strip()[:50]
        safe_base = re.sub(r'[-\s]+', '-', safe_base)
        
        if not safe_base:
            safe_base = 'download'
        
        return f"{safe_base}{file_ext}"