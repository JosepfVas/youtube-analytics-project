import os
from googleapiclient.discovery import build


class VideoIdError(Exception):
    pass


class Video:

    API_KEY = 'AIzaSyCcewIqkMw786Rey_TH2XGxGNlFVgg2_Eg'

    def __init__(self, video_id):

        self.video_id = video_id
        self.api_key = self.API_KEY
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
        self.title = None
        self.view_count = None
        self.like_count = None
        self.comment_count = None

        if video_id:
            try:
                video_response = self.youtube.videos().list(
                    part='snippet,statistics,contentDetails,topicDetails',
                    id=video_id
                ).execute()

                self.title: str = video_response['items'][0]['snippet']['title']
                self.view_count: int = video_response['items'][0]['statistics']['viewCount']
                self.like_count: int = video_response['items'][0]['statistics']['likeCount']
                self.comment_count: int = video_response['items'][0]['statistics']['commentCount']

            except (KeyError, IndexError):
                raise VideoIdError("Неверная ссылка на видео")

    def __str__(self):
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id='', playlist_id=''):
        super().__init__(video_id)
        self.playlist_id = playlist_id

        if playlist_id:  # Выполнять запрос только при наличии playlist_id
            playlists_response = self.youtube.playlistItems().list(
                part='snippet',
                playlistId=playlist_id
            ).execute()

            self.video_items = playlists_response.get('items', [])

    def __str__(self):
        return f"{super().__str__()}"