import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import datetime

api_version = "v3"
api_service_name = "youtube"

def get_authenticated_service():
    # 使用OAuth 2.0客户端ID文件获取身份验证
    scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
    api_key = "AIzaSyD8xppUVmR5x6kr9mbXpX89yc4EMAXGW8c"

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

    return youtube

def get_channel_videos(channel_id, youtube):
    print("获取频道视频中...")
    videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type='video'
        )
        response = request.execute()
        videos.extend(response['items'])

        next_page_token = response.get('nextPageToken')
        if next_page_token is None:
            break

    return [video['id']['videoId'] for video in videos]

def get_video_durations(video_ids, youtube):
    print("获取视频时长中...")
    durations = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part="contentDetails",
            id=','.join(video_ids[i:i+50])
        )
        response = request.execute()
        durations.extend(response['items'])

    return [item['contentDetails']['duration'] for item in durations]

def calculate_total_duration(durations):
    print("计算总时长中...")
    total_duration = datetime.timedelta()

    for duration in durations:
        time_components = datetime.datetime.strptime(duration[2:], "%H:%M:%S")
        delta = datetime.timedelta(hours=time_components.hour, minutes=time_components.minute, seconds=time_components.second)
        total_duration += delta

    return total_duration

def main():
    youtube = get_authenticated_service()
    channel_id = input("请输入YouTube博主的channel ID：")

    video_ids = get_channel_videos(channel_id, youtube)
    durations = get_video_durations(video_ids, youtube)
    total_duration = calculate_total_duration(durations)

    print(f"博主的所有视频总时长为：{total_duration}")

if __name__ == "__main__":
    main()
