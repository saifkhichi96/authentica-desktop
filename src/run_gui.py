from core import Client
from gui import SplashScreen
from gui.core import App
# from .Scanner import scan_image


class GUIClient(Client):
    def __init__(self):
        super().__init__(feature_model='../../db/models/signet.pth',
                         canvas_size=(150, 220),
                         segmentation_model='../../db/models/versign_segment.pkl',
                         data_path='../db/app_data/')

        self.app = App('Authentica')
        self.app.setResourcesPath('../res/')
        self.app.client = self

    def run(self):
        self.app.startApp(SplashScreen())


def main():
    client = GUIClient()
    client.run()


if __name__ == "__main__":
    main()
