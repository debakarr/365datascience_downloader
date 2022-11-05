import json
import string
from pathlib import Path

import requests
import yt_dlp

from course_model import CourseModel
from video_model import VideoModel


def normalize_name(name: str) -> str:
    return name.translate(str.maketrans("", "", string.punctuation))


def download_video_from_stream_url(video_stream_url: str, filepath: str, quality: str) -> None:
    """Download a video from stream url
    :param video_stream_url: stream url
    :param filepath: file path where to download
    :param quality: quality to select
    """
    ydl_opts = {
        "format": f"bestvideo[height<={quality[:-1]}]+bestaudio/best[height<={quality[:-1]}]/best",
        "concurrent_fragment_downloads": 15,
        "outtmpl": f"{filepath}.%(ext)s",
        "postprocessors": [{"key": "FFmpegFixupM3u8"}],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_stream_url)


def request_365datascience_api(course_slug: str, authorization_token: str) -> CourseModel:
    course_api_url = f"https://api.365datascience.com/courses/{course_slug}/player"
    headers_for_365datascience = {
        "authority": "api.365datascience.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
        "Authorization": f"Bearer {authorization_token}",
    }
    response = requests.get(course_api_url, headers=headers_for_365datascience)
    return CourseModel.parse_raw(response.text)


def request_brightcove_api(video_id: str, policy_key: str) -> VideoModel:
    header_for_brightcove = {
        "authority": "edge.api.brightcove.com",
        "accept": f"application/json;pk={policy_key}",
        "accept-language": "en-US,en;q=0.9",
        "origin": "https://learn.365datascience.com",
        "referer": "https://learn.365datascience.com/",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26",
    }

    video_api_url = f"https://edge.api.brightcove.com/playback/v1/accounts/6258000438001/videos/{video_id}"
    response = requests.get(video_api_url, headers=header_for_brightcove)
    return VideoModel.parse_raw(response.text)


def download_course(course_url: str, authorization_token: str, policy_key: str, quality: str) -> None:
    course_slug = course_url.strip("/").split("/").pop()
    course_data = request_365datascience_api(course_slug, authorization_token)

    for i, section in enumerate(course_data.sections, start=1):
        for j, asset in enumerate(section.assets, start=1):
            if asset.type == "lesson":
                file_path = (
                    Path(Path.home() / "Downloads")
                    / "365DataScience"
                    / normalize_name(course_data.info.name)
                    / f"{i} - {normalize_name(section.name)}"
                    / f"{j} - {normalize_name(asset.name)}"
                )
                video_data = request_brightcove_api(asset.video.ext_id, policy_key)
                source = video_data.sources.pop(0)
                master_m3u8_url = source.src
                download_video_from_stream_url(master_m3u8_url, file_path, quality)


if __name__ == "__main__":
    input_file = Path(__file__).parent / "input.json"
    input_data = json.loads(input_file.read_text())
    course_url = input_data.get("course_url")
    authorization_token = input_data.get("authorization_token")
    policy_key = input_data.get("policy_key")
    quality = input_data.get("quality")
    download_course(
        course_url=course_url, authorization_token=authorization_token, policy_key=policy_key, quality=quality
    )
