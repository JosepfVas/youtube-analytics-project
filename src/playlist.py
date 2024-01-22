import datetime
from googleapiclient.discovery import build
import isodate


class PlayList:

    API_KEY = 'AIzaSyCcewIqkMw786Rey_TH2XGxGNlFVgg2_Eg'

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.api_key = self.API_KEY
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.playlist_data = self.get_playlist_data()

    def get_playlist_data(self):
        playlist_response = self.youtube.playlists().list(
            part='snippet',
            id=self.playlist_id
        ).execute()

        return playlist_response['items'][0]['snippet']

    @property
    def title(self):
        return self.playlist_data['title']

    @property
    def url(self):
        return f"https://www.youtube.com/playlist?list={self.playlist_id}"

    @property
    def total_duration(self):
        video_ids = self.get_video_ids()
        video_durations = self.get_video_durations(video_ids)
        total_seconds = sum(video_durations)
        return datetime.timedelta(seconds=total_seconds)

    def get_video_ids(self):
        playlist_items_response = self.youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
            maxResults=50
        ).execute()

        return [item['contentDetails']['videoId'] for item in playlist_items_response.get('items', [])]

    def get_video_durations(self, video_ids):
        durations = []

        for video_id in video_ids:
            video_response = self.youtube.videos().list(
                part='contentDetails',
                id=video_id
            ).execute()

            duration_iso8601 = video_response['items'][0]['contentDetails']['duration']
            duration_seconds = isodate.parse_duration(duration_iso8601).total_seconds()
            durations.append(duration_seconds)

        return durations

    def show_best_video(self):
        playlist_items_response = self.youtube.playlistItems().list(
            part='snippet,contentDetails',
            playlistId=self.playlist_id,
            maxResults=50
        ).execute()

        videos = playlist_items_response['items']

        best_video = max(videos, key=lambda item: int(item['snippet']['position']))

        return f"https://youtu.be/{best_video['snippet']['resourceId']['videoId']}"

