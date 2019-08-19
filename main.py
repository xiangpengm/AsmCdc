import threading
import time
import sys
import random
from package import Template, load
import webview
from page import html


class Api:
    def __init__(self):
        self.cancel_heavy_stuff_flag = False

    def init(self, params):
        response = {
            'message': 'Hello from Python {0}'.format(sys.version)
        }
        return response

    def getRandomNumber(self, params):
        response = {
            'message': 'Here is a random number courtesy of randint: {0}'.format(random.randint(0, 100000000))
        }
        return response

    def doHeavyStuff(self, params):
        # sleep to prevent from the ui thread from freezing for a moment
        time.sleep(0.1)
        now = time.time()
        self.cancel_heavy_stuff_flag = False
        for i in range(0, 1000000):
            _ = i * random.randint(0, 1000)
            if self.cancel_heavy_stuff_flag:
                response = {'message': 'Operation cancelled'}
                break
        else:
            then = time.time()
            response = {
                'message': 'Operation took {0:.1f} seconds on the thread {1}'.format((then - now), threading.current_thread())
            }
        return response

    def cancelHeavyStuff(self, params):
        time.sleep(0.1)
        self.cancel_heavy_stuff_flag = True

    def sayHelloTo(self, params):
        response = {
            'message': 'Hello {0}!'.format(params)
        }
        return response

    def getFile(self, params):
        file_types = ('Image Files (*.bmp;*.jpg;*.gif)', 'All files (*.*)')
        result = window.create_file_dialog(
            webview.OPEN_DIALOG, 
            allow_multiple=True,
            file_types=file_types
        )
        if result is None:
            return {"message": "error"}
        else:
            return {"message": result}



if __name__ == '__main__':
    api = Api()
    window = webview.create_window(
        'CDC Assembly Client', 
        html=html, 
        js_api=api,
        min_size=(500, 400)
    )
    webview.start()