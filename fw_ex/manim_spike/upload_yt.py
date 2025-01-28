import os
import argparse
import google.auth
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
from google.auth.transport.requests import Request

# pyright: reportMissingImports=false

# YouTube API scopes
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_FILE = "token.pickle"
CREDENTIALS_FILE = "client_secrets.json"


def authenticate_youtube_web():
    # Authenticate and get credentials
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    credentials = flow.run_console()
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


def authenticate_youtube():
    """Use the"""
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secrets.json", ["https://www.googleapis.com/auth/youtube.upload"]
    )
    credentials = flow.run_local_server(port=0)  # Opens browser for login
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


def authenticate():
    """Authenticate to YouTube API and return the service instance."""
    credentials = None

    # Load credentials from the pickle file if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            credentials = pickle.load(token)

    # If credentials are invalid or do not exist, authenticate the user
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        # Save the credentials to the pickle file for future use
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)

    # Build the YouTube API client
    youtube = build("youtube", "v3", credentials=credentials)
    return youtube


def upload_video(
    youtube,
    file_path,
    title,
    description,
    tags,
    category_id="22",
    privacy_status="public",
):
    # Configure video upload details
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags.split(",") if tags else [],
            "categoryId": category_id,
        },
        "status": {
            "privacyStatus": privacy_status,
        },
    }

    # Upload the video
    media = MediaFileUpload(file_path, chunksize=-1, resumable=True)
    response = (
        youtube.videos()
        .insert(
            part="snippet,status",
            body=request_body,
            media_body=media,
        )
        .execute()
    )

    print(f"Video uploaded successfully! Video ID: {response['id']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload a video to YouTube.")
    parser.add_argument("--file", required=True, help="Path to the video file")
    parser.add_argument("--title", required=True, help="Title of the video")
    parser.add_argument("--description", required=True, help="Description of the video")
    parser.add_argument("--tags", help="Comma-separated tags for the video")
    parser.add_argument(
        "--privacy",
        default="public",
        choices=["public", "private", "unlisted"],
        help="Privacy status",
    )
    args = parser.parse_args()

    if not os.path.exists("client_secrets.json"):
        print("Error: 'client_secrets.json' file is missing.")
        exit(1)

    youtube = authenticate()
    upload_video(
        youtube=youtube,
        file_path=args.file,
        title=args.title,
        description=args.description,
        tags=args.tags,
        privacy_status=args.privacy,
    )
