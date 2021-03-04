import os
import cv2

from versign import VerSign
from .Database import Database
from .segment import extract_from_grid, extract_from_check


class Client:
    """An Authentica client.
    """

    def __init__(self, feature_model, canvas_size, segmentation_model, data_path):
        # type: (VerSign, str, bool) -> None
        """Creates a new Client instance.

        Parameters:
            feature_model (str): Path of the trained writer-independent feature extractor.
            canvas_size (tuple): Input size for the feature extractor.
            segmentation_model (str): Path of the document segmentation model.
            data_path (str): Path for saving the user database.
        """
        self.__v = VerSign(feature_model, canvas_size)
        self.__db = Database(data_path)
        self.__segmentation_model = segmentation_model

    def enroll(self, uid, specimens):
        """Enrolls a new user in the system.

        Enrollment fails if the given uid is not unique, or no signatures can be
        found in the given specimens image.

        Parameters:
            uid (str): A unique id for the new user.
            specimens (np.array): An image of the specimen paper with new user's signatures.

        Returns:
            True if enrollment successful, else False.
        """
        if self.__db.contains(uid):
            return False

        signatures = extract_from_grid(specimens)
        if len(signatures) == 0:
            return False

        # todo: augment signatures to generate more samples

        self.__db.add(uid, signatures)
        return True

    def unenroll(self, uid):
        """Removes an enrolled user from the system.

        Parameters:
            uid (str): The id of the user to remove.
        """
        self.__db.remove(uid)

    def is_enrolled(self, uid):
        """Checks if a user is enrolled in the system.

        Parameters:
            uid (str): The id of the user to check.

        Returns:
            True if the user exists, else False.
        """
        return self.__db.contains(uid)

    def verify_author(self, uid, signature, is_check=False):
        """Verifies that a signature belongs to a user.

        User must be enrolled in the system to successfully verify.

        Parameters:
            uid (str): The id of the claimed author of the signature.
            signature (str): Path of image of the questioned signature.
            is_check (bool): Set True if input image is a bank check instead of
                             extracted signature. Default is False.

        Returns:
            True if signature belongs to user, else False.
        """
        if not self.is_enrolled(uid):
            return None

        # Train a WD classifier on reference signatures
        x_train = self.__db.get(uid)
        self.__v.fit(x_train)

        # Match the questioned signature with trained model to determine its authenticity
        if is_check:
            signature = extract_from_check(signature, self.__segmentation_model)

        user_dir = os.path.join(os.path.join(self.__db.root(), uid), 'Questioned')
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        outfile = os.path.join(user_dir, 'Q001.png')
        cv2.imwrite(outfile, signature)

        x_test = [outfile]
        y_pred = self.__v.predict(x_test)

        return y_pred[0] == 1
