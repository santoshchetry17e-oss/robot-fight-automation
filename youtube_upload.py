import os
import glob
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

VIDEO_FOLDER = "videos"

creds = Credentials.from_authorized_user_file(
    "token.json",
    ["https://www.googleapis.com/auth/youtube.upload"]
)

youtube = build("youtube", "v3", credentials=creds)

videos = glob.glob(os.path.join(VIDEO_FOLDER, "*.mp4"))

if videos:
    video = videos[0]

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Epic AI Robot Fight 🤖🔥",
                "description": "Daily AI Robot Fight Shorts!",
                "tags": ["Robot Fight", "AI Robots", "Shorts"],
                "categoryId": "24"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(video, resumable=True)
    )

    request.execute()
    print("YouTube upload successful!")
else:
    print("No video found!")
