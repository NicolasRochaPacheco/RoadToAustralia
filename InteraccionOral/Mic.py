import pyaudio

class Mic:
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    # Even if your default input is multi channel (like a webcam mic),
    # it's really important to only record 1 channel, as the STT service
    # does not do anything useful with stereo. You get a lot of "hmmm"
    # back.
    CHANNELS = 1
    # Rate is important, nothing works without it. This is a pretty
    # standard default. If you have an audio device that requires
    # something different, change this.
    RATE = 16000
    stream = None
    p = None

    def __init__(self):
        # Start a pyaudio instance
        self.p = pyaudio.PyAudio()
        # Create an input stream with pyaudio
        # self.RATE = int(self.p.get_default_input_device_info()['defaultSampleRate'])
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.CHANNELS,
                                  rate=self.RATE,
                                  input=True,
                                  frames_per_buffer=self.CHUNK)
        # Start the stream
        # self.stream.start_stream()

    def start_strem_mic(self):
        self.stream.start_stream()
        print("Mic: Start Stream")

    def get_audio(self):
        data = self.stream.read(self.CHUNK)
        return data

    def stop_mic(self):
        # Disconnect the audio stream
        self.stream.stop_stream()
        self.stream.close()
        # kill the audio device
        self.p.terminate()
        print("Mic: Stop Steam")