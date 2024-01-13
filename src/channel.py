from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    API_KEY = 'AIzaSyCcewIqkMw786Rey_TH2XGxGNlFVgg2_Eg'

    def __init__(self, channel_id: str) -> None:
        self.channel_id = channel_id
        self.api_key = self.API_KEY
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # Получаем данные о канале
        channel_data = self.get_channel_data()
        self.id = channel_data.get('id')
        self.title = channel_data.get('snippet', {}).get('title')
        self.description = channel_data.get('snippet', {}).get('description')
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(channel_data.get('statistics', {}).get('subscriberCount', 0))
        self.video_count = int(channel_data.get('statistics', {}).get('videoCount', 0))
        self.view_count = int(channel_data.get('statistics', {}).get('viewCount', 0))

    def print_info(self) -> None:
        channel_data = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel_data, indent=2))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.API_KEY)

    def get_channel_data(self) -> dict:
            request = self.youtube.channels().list(id=self.channel_id,part='snippet,statistics')
            response = request.execute()
            return response['items'][0] if response.get('items') else {}

    def to_json(self, filename: str) -> None:
        channel_data = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'url': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(channel_data, file, ensure_ascii=False, indent=2)

    def __str__(self):
        return f'{self.title}("{self.url}")'

    def __add__(self, other):
        self.subscriber_count += other.subscriber_count

    def __sub__(self, other):
        self.subscriber_count -= other.subscriber_count
        other.subscriber_count -= self.subscriber_count

    def __gt__(self, other):
        self.subscriber_count > other.subscriber_count

    def __ge__(self, other):
        self.subscriber_count >= other.subscriber_count

    def __lt__(self, other):
        self.subscriber_count > other.subscriber_count

    def __le__(self, other):
        self.subscriber_count >= other.subscriber_count






