from websocket._abnf import ABNF
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
import websocket
import configparser
import argparse
import base64
import json
import time

class S2TThread(QThread):
    sendSTTSignal = pyqtSignal(str)
    stoppedSpeakingSignal = pyqtSignal(str)
    wsReadySignal = pyqtSignal(bool)

    def __init__(self):
        super(S2TThread, self).__init__()

        self.running = False
        self.wsReady = False

        headers = {}
        userpass = ":".join(self.get_auth())
        headers["Authorization"] = "Basic " + base64.b64encode(
            userpass.encode()).decode()
        url = ("wss://stream.watsonplatform.net//speech-to-text/api/v1/recognize"
               "?model=es-ES_BroadbandModel")

        self.ws = websocket.WebSocketApp(url,
                                    header=headers,
                                    on_message=self.on_message,
                                    on_error=self.on_error,
                                    on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.ws.args = self.parse_args()
        self.messageShow = ""

    def run(self):
        self.running = True
        while self.running:
            time.sleep(0.01)
            try:
                self.ws.run_forever()
            except Exception as e:
                print("S2TThread: Error externo: %s" % str(e))
                self.wsReady = False

    def stop(self):
        self.ws.close()
        self.running = False

    def on_message(self, ws, msg):
        data = json.loads(msg)
        print("S2TThread: msg = ", self.msg)
        if "results" in data:
            message = data['results'][0]['alternatives'][0]['transcript']
            print("S2TThread: Message = ", message)
            self.sendSTTSignal.emit(self.messageShow + message)
            if data['results'][0]['final']:
                self.stoppedSpeakingSignal.emit(message)
                lastWord = message.split(' ')[-2]
                print("S2TThread: lastWord = ", lastWord)
                if lastWord != "fin":
                    self.messageShow += message
                else:
                    self.messageShow = ""

    def on_error(self, ws, error):
        print("S2TThread: Error = " + str(error))

    def on_close(self, ws):
        print('S2TThread: Close')
        self.wsReady = False

    def on_open(self, ws):
        data = {
            "action": "start",
            "content-type": "audio/l16;rate=%d" % 16000,
            "continuous": True,
            "interim_results": True,
            "inactivity_timeout": -1,
            "word_confidence": True,
            "timestamps": True,
            "max_alternatives": 3
        }
        ws.send(json.dumps(data).encode('utf8'))
        self.wsReady = True
        print("S2TThread: Open")

    def get_auth(self):
        config = configparser.RawConfigParser()
        #config.read('Core/S2T/speech.cfg')
        config.read('speech.cfg')
        user = config.get('auth', 'username')
        password = config.get('auth', 'password')
        return (user, password)

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Transcribe Watson text in real time')
        parser.add_argument('-t', '--timeout', type=int, default=-1)
        args = parser.parse_args()
        return args

    @pyqtSlot(bytes)
    def slot_receive_stream(self, data):
        try:
            if self.wsReady:
                self.ws.send(data, ABNF.OPCODE_BINARY)
        except Exception as e:
            print("S2TThread: Error: %s" % str(e))
