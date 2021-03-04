import os

import cv2
from core import Client
# from .Scanner import scan_image


class CLIClient(Client):
    def __init__(self):
        super().__init__(feature_model='../../db/models/signet.pth',
                         canvas_size=(150, 220),
                         segmentation_model='../../db/models/versign_segment.pkl',
                         data_path='../db/app_data/')

    def on_register_selected(self):
        print("REGISTER NEW USER")
        user_id = input("User ID (must be unique): ")
        if self.contains_user(user_id):
            print("ERROR. User ID already exists.")
            return

        # Get image from scanner
        # prompt = "Put signature specimen paper in scanner and hit [Enter]"
        # input(prompt)
        # filename = scan_image(outfile=userId)
        filename = "/Volumes/MAXTOR/Work/Research/Signature Verification/Research Material/Datasets/Collected/Signatures/Raw/0000-SH2-G.png"
        if not os.path.exists(filename):
            print("FILE NOT FOUND")
            return

        # Open and crop the image
        ref_signs = cv2.imread(filename, 0)
        h, w = ref_signs.shape
        x, y = int(0.025 * w), int(0.025 * h)
        w, h = w - 2 * x, h - 2 * y
        ref_signs = ref_signs[y:y + h, x:x + w]

        if self.register(user_id, signature_grid=ref_signs):
            print("Enrollment successful")
        else:
            print("ERROR. User ID already exists.")

    def on_verify_selected(self):
        print("VERIFY SIGNATURE")
        user_id = input("User ID: ")
        if not self.contains_user(user_id):
            print("ERROR. No such user.")
            return

        # prompt = "Put the bank cheque in scanner and hit [Enter]"
        # input(prompt)
        # filename = scanImage(outfile=userId)
        filename = "../../db/datasets/Segmentation/TestSet/CHECK_10.jpg"

        if self.test(user_id, image=cv2.imread(filename, 0), is_check=True):
            print("Verification Result: GENUINE")
        else:
            print("Verification Result: FORGED")

    def run(self):
        print("VERSIGN: AUTOMATIC SIGNATURE VERIFICATION SYSTEM")
        options = ["1", "2", "0"]
        prompt = "\
        Select an option (0 to end):\n \
        \t1: Register new customer\n \
        \t2: Verify a signature\n \
        \t\t? "
        choice = str(input(prompt))
        while choice != "0":
            if choice in options:
                if choice == "1":
                    self.on_register_selected()
                elif choice == "2":
                    self.on_verify_selected()
            else:
                print("Invalid choice. Please select again.")
            choice = str(input(prompt))


def main():
    client = CLIClient()
    client.run()


if __name__ == "__main__":
    main()
