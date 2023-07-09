import os
from io import FileIO
from typing import Dict, List, BinaryIO, AnyStr

from pydub import AudioSegment
import openai


class OpenAIBase:

    def __init__(self, token: str = None, model: str = None):
        super(OpenAIBase, self).__init__()
        self._token = token
        if self._token is None:
            self._token = os.getenv('OPENAI_KEY', '')

        if self._token == '':
            raise ValueError(f"Unfulfilled credentials for {self.__class__.__name__} in parameters or environment.")

        openai.api_key = self._token
        self.open_ai = openai

        self.model = model


class OpenAIWhisper(OpenAIBase):
    WHISPER_MODEL = "whisper-1"
    SUPPORTED_TYPES = [
        'm4a', 'mp3', 'webm', 'mp4', 'mpga', 'wav', 'mpeg'
    ]

    def __init__(self,
                 token: str = None,
                 model: str = WHISPER_MODEL):
        super(OpenAIWhisper, self).__init__(token, model)

    def load_audio(self, filepath: str) -> BinaryIO:
        ext = filepath.split('.')[-1]
        if ext not in self.SUPPORTED_TYPES:
            raise ValueError(f'Unsupported file type : {ext}')

        file = BinaryIO(FileIO(filepath, 'rb'))
        return file

    @staticmethod
    def convert_audio(fr: str, to: str) -> None:
        AudioSegment.from_file(fr).export(to, format="mp3")

    def transcribe(self, audio_file: BinaryIO) -> Dict:
        try:
            response = self.open_ai.Audio.transcribe(
                model=self.model,
                file=audio_file,
            )
            return response
        except openai.error.OpenAIError:
            return {}


class OpenAIComplete(OpenAIBase):
    DEFAULT_MODEL = 'text-davinci-003'

    def __init__(self,
                 token: str = None,
                 model: str = DEFAULT_MODEL,
                 max_tokens: int = 1000):
        super(OpenAIComplete, self).__init__(token, model)
        self.max_tokens = max_tokens

    def call(self, x: AnyStr = None):
        try:
            response = self.open_ai.Completion.create(
                model=self.model,
                prompt=x,
                max_tokens=self.max_tokens
            )
            response_message = response['choices'][0]['text']
            return response_message
        except openai.error.OpenAIError:
            return ''
