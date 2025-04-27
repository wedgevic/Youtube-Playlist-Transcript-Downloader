# Youtube Playlist Transcript Downloader

A simple python script to help you download the transcripts of all videos in a Youtube Playlist

## Features
- Download transcripts for YouTube videos in a playlist
- Support for multiple languages
- Multi-threaded downloading for faster performance

## Setup

1. Clone this repository and create the python venv:
   ```bash
   git clone https://github.com/yourusername/my-transcript-downloader.git
   cd my-transcript-downloader
   python3 -m venv .venv
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the script:
   ```bash
   python transcript.py --playlist_url "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
   ```

## Configuration
- `--languages`: Comma-separated list of language codes (e.g. `'en, de'`)
- `--output_dir`: Directory to save the transcripts (defaults to the playlist name)
- `--multi`: Number of threads to use for parallel downloads (default is 5)