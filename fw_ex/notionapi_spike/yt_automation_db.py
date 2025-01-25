# ruff: noqa: F841
# pyright: reportMissingImports=false

import os
from notion_client import Client
from rich import print
from bs4 import BeautifulSoup
import requests
from googleapiclient.discovery import build

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
client = Client(auth=NOTION_TOKEN)


def get_page_shared():
    results = client.search().get("results")
    # print(len(results))
    ids = []
    for data in results:
        ids.append(data["id"])
    return ids, results[0]


def create_database_schema():
    database_properties = {
        "Title": {"title": {}},
        "Video ID": {"rich_text": {}},
        "Channel Name": {"rich_text": {}},
        "Channel ID": {"rich_text": {}},
        "Published Date": {"date": {}},
        "Description": {"rich_text": {}},
        "URL": {"url": {}},
        "Tags": {"multi_select": {}},
        "Duration": {"number": {"format": "number"}},
        "View Count": {"number": {"format": "number"}},
        "Thumbnail": {"files": {}},
    }
    return {
        "title": [{"type": "text", "text": {"content": "ChannelDB"}}],
        "properties": database_properties,
    }


def fetch_youtube_videos_and_load_to_notion(channel_id, database_id):
    # Initialize YouTube Data API client
    youtube = build("youtube", "v3", developerKey=os.environ["YOUTUBE_API_KEY"])
    print("Youtube API Accessed")

    channel_response = (
        youtube.channels().list(id=channel_id, part="id,snippet").execute()
    )
    print(channel_response)
    # Get channel ID and name
    channel = channel_response["items"][0]
    channel_id = channel["id"]
    channel_name = channel["snippet"]["title"]
    print(f"Fetching videos for channel: {channel_name}")

    # Fetch videos from the channel
    videos = []
    next_page_token = None

    while True:
        playlist_response = (
            youtube.search()
            .list(
                channelId=channel_id,
                part="id,snippet",
                maxResults=50,
                pageToken=next_page_token,
            )
            .execute()
        )

        for item in playlist_response["items"]:
            if item["id"]["kind"] == "youtube#video":
                videos.append({
                    "title": item["snippet"]["title"],
                    "video_id": item["id"]["videoId"],
                    "published_date": item["snippet"]["publishedAt"],
                    "description": item["snippet"]["description"],
                    "thumbnail": item["snippet"]["thumbnails"]["default"]["url"],
                    "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                })

        next_page_token = playlist_response.get("nextPageToken")
        if not next_page_token:
            break

    # Add videos to Notion database
    for idx, video in enumerate(videos):
        try:
            client.pages.create(
                parent={"database_id": database_id},
                properties={
                    "Title": {"title": [{"text": {"content": video["title"]}}]},
                    "Video ID": {
                        "rich_text": [{"text": {"content": video["video_id"]}}]
                    },
                    "Published Date": {"date": {"start": video["published_date"]}},
                    "Description": {
                        "rich_text": [{"text": {"content": video["description"]}}]
                    },
                    "URL": {"url": video["url"]},
                    "Thumbnail": {
                        "files": [
                            {
                                "name": "Thumbnail",
                                "external": {"url": video["thumbnail"]},
                            }
                        ]
                    },
                },
                cover={
                    "type": "external",
                    "external": {
                        "url": f"https://i.ytimg.com/vi/{video['video_id']}/maxresdefault.jpg"
                    },
                },
            )
            print(f"Added video: {video['title']}")
        except Exception as e:
            print(f"Failed to add video: {video['title']}. Error: {e}")
            # if idx == 2:
            # break


def main():
    page_id = ""
    database_id = "18684ade-96ac-8154-b1a9-d985db796e3d"
    # try:
    #     shared_ids, page_result = get_page_shared()
    #     page_id = shared_ids[0]
    # except Exception as e:
    #     print(f"❌ Error: {str(e)}")
    # try:
    #     # Create the database
    #     response = client.databases.create(
    #         parent={
    #             "type": "page_id",
    #             "page_id": page_id,
    #         },  # Replace with your page ID
    #         **create_database_schema(),
    #     )

    #     database_id = response["id"]
    #     print(f"✅ YT Database created successfully with ID: {database_id}")
    # except Exception as e:
    #     print(f"❌ Error: {str(e)}")
    try:
        # Create sample tasks
        create_yt_vids(database_id, channel_url)
        print("✅ Sample videos created successfully")
    except Exception as e:
        print(f"❌ YT Error: {str(e)}")


def get_channel_id(channel_url):
    response = requests.get(channel_url)
    soup = BeautifulSoup(response.text, "html.parser")
    script = soup.find(
        "script", string=lambda text: "externalId" in text if text else False
    )
    if script:
        start = script.text.find('"externalId":"') + len('"externalId":"')
        end = script.text.find('"', start)
        return script.text[start:end]
    return None


def clear_notion_database(database_id):
    # Query all pages in the database
    query = client.databases.query(database_id=database_id)
    for page in query["results"]:
        # Delete each page by its ID
        client.blocks.delete(page["id"])
        print(f"Deleted page: {page['id']}")


if __name__ == "__main__":
    # after DB is created, the below won't work
    # ids, result = get_page_shared()
    # print(f"Selected id is: {ids[0]}")
    # print(
    #     f"Selected page is: {result['properties']['title']['title'][0]['text']['content']}"
    # )
    # main()
    # Example usage
    database_id = "18684ade-96ac-8154-b1a9-d985db796e3d"
    # channel_url = "https://www.youtube.com/@insightbuilder"
    channel_url = "https://www.youtube.com/@bestbinauralbeats"
    channel_id = get_channel_id(channel_url)
    print(f"Channel ID: {channel_id}")
    fetch_youtube_videos_and_load_to_notion(channel_id, database_id)
    # clear_notion_database(database_id)
