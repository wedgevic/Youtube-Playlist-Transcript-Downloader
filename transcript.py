import os
import yt_dlp
import re
import time
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from youtube_transcript_api._errors import VideoUnavailable, VideoUnplayable, NoTranscriptFound
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm


ytt_api = YouTubeTranscriptApi()
ydl_opts = {'quiet': True, 'extract_flat': True}


def parse_args():
    parser = argparse.ArgumentParser(description='Simple Youtube Playlist Transcript Downloader')
    parser.add_argument('playlist_url', type=str, help='The URL of the YT Playlist')
    parser.add_argument('--languages', type=str, default='all', help='Comma separated list of language codes (e.g. \'en, de\'). Downloads all available by default')
    parser.add_argument('--output_dir', type=str, help='Output folder for transcripts. Named after the playlist by default')
    parser.add_argument('--multi', type=int, default=5, help='Amount of simultaneous downloads. 5 by default')
    return parser.parse_args()

def get_playlist_videos_title(playlist_url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)
        video_urls = [entry['url'] for entry in info['entries']]
        playlist_title = info.get('title', 'Untitled Playlist')
        return video_urls, playlist_title

        
def process_video(video_id, lang, output_dir):    
    try:
        if 'all' in lang:
            available_languages = ytt_api.get_available_languages(video_id)
            transcript = ytt_api.fetch(video_id, languages=available_languages)
        else:
            transcript = ytt_api.fetch(video_id, languages=lang)
        info = yt_dlp.YoutubeDL(ydl_opts).extract_info(f'https://www.youtube.com/watch?v={video_id}', download= False)
        title = re.sub(r'[\\/*?:"<>|]', '', info['title'])

        with open(f'./{output_dir}/{title}.txt', 'w', encoding='utf-8') as txt:
            txt.write(TextFormatter().format_transcript(transcript))
        print(f'Saved: {title}.txt')    
        time.sleep(1.2)

    except (VideoUnavailable, VideoUnplayable, NoTranscriptFound) as e:
        print(f'Skipping video {video_id}: {e}')
    except Exception as e:
        print(f'Unknown error for {video_id}: {e}')

def main():
    args = parse_args()
    lang = args.languages.split(',')
    urls, playlist_title = get_playlist_videos_title(args.playlist_url)
    if not args.output_dir:
        args.output_dir = f'./{playlist_title}'
    os.makedirs(args.output_dir, exist_ok=True)
    sanitized = [item.replace('https://www.youtube.com/watch?v=', '') for item in urls]

    try:
        with ThreadPoolExecutor(max_workers=args.multi) as executor: # multithreading, yipee!
            with tqdm(total=len(sanitized), desc="Downloading Transcripts", unit="video") as pbar:
                futures = []
                for video_id in sanitized:
                    future = executor.submit(process_video, video_id, lang, args.output_dir)
                    futures.append(future)

                for future in as_completed(futures):
                    future.result()
                    pbar.update(1) 
        print('\nAll transcripts successfully downloaded')

    except KeyboardInterrupt:
        print('\nProcess Interrupted by User. Exiting...')
if __name__ == '__main__':
    main()