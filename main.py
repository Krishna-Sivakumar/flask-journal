from app import app
import webview


if __name__ == '__main__':
    webview.create_window("Journal", app)
    webview.start()