import webview
import threading
import os

def save_file_dialog(window):
    import time
    time.sleep(5)
    result = window.create_file_dialog(
        webview.FOLDER_DIALOG, directory='/')
    print(result)


if __name__ == '__main__':
    window = webview.create_window(
        'Save file dialog', 'https://pywebview.flowrl.com/hello')
    print(os.getcwd())
    webview.start(save_file_dialog, window)
    