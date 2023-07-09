import time
import wave

import pyaudio


class AudioMechanic:

    def __init__(self, filename: str = 'output.wav'):
        self.filename = filename
        self.is_recording = False

        self.chunk = 1024
        self.channels = 1
        self.fs = 44100
        self.record_seconds = 3
        self.sample_format = pyaudio.paInt16

    def record(self):
        audio = pyaudio.PyAudio()
        print(f'Recording Start: {time.time()}')
        stream = audio.open(
            format=self.sample_format,
            channels=self.channels,
            rate=self.fs,
            input=True,
            input_device_index=0,
            frames_per_buffer=self.chunk)

        frames = []
        for i in range(0, int(self.fs / self.chunk * self.record_seconds)):
            data = stream.read(self.chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        audio.terminate()

        # Save the recorded data as a WAV file
        wf = wave.open(self.filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(audio.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(frames))
        wf.close()

        print(f'Recording Finished {time.time()}')