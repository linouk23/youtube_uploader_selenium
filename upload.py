import argparse
from youtube_uploader_selenium import YouTubeUploader
from typing import Optional


def main(video_path: str, metadata_path: Optional[str] = None, thumbnail_path: Optional[str] = None):
    uploader = YouTubeUploader(video_path, metadata_path, thumbnail_path)
    was_video_uploaded, video_id = uploader.upload()
    assert was_video_uploaded


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video",
                        help='Path to the video file',
                        required=True)
    parser.add_argument("-t",
                        "--thumbnail",
                        help='Path to the thumbnail image',)
    parser.add_argument("--meta", help='Path to the JSON file with metadata')
    args = parser.parse_args()
    main(args.video, args.meta, args.thumbnail)
