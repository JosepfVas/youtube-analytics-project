from googleapiclient.discovery import build
import json
import os



class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.api_key: str = os.getenv('YOUTUBE-API')
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_data = self.youtube.channels().list(id=self.channel_id,part='snippet,statistics').execute()
        print(json.dumps(channel_data, indent=2))






