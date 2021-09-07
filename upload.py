import argparse
from youtube_uploader_selenium import YouTubeUploader, YouTubeVideo
from typing import Optional


def main(video_path: str, metadata_path: Optional[str] = None):
    youtube_video = YouTubeVideo.from_file(
        video_path=video_path, 
        metadata_path=metadata_path
    )
    uploader = YouTubeUploader(youtube_video=youtube_video)
    was_video_uploaded, video_id = uploader.upload()
    assert was_video_uploaded


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--video",
        help='Path to the video file',
        required=True
    )
    parser.add_argument(
        "--meta", 
        help='Path to the JSON file with metadata'
    )
    args = parser.parse_args()
    main(args.video, args.meta)
