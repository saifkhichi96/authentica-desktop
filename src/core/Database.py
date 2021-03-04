import os
import shutil
import cv2


class Database:
    """Database to store the data of registered users.

    Stored data includes details of users, paths of training signatures, and
    learned models, among other things.
    """

    def __init__(self, data_path):
        """Creates a new Database instance.
        """
        self.__root = data_path
        if not os.path.exists(self.__root):
            os.makedirs(self.__root)

    def root(self):
        return self.__root

    def add(self, uid, signatures):
        """Adds a new user to database.

        Saves the given signatures as training samples for the new user. If a
        user with given uid already exists, signatures are saved as additional
        training samples for existing user.

        Parameters:
            uid (str): A unique id for the new user.
            signatures (list): List of reference signature images for this user.
        """
        user_dir = os.path.join(os.path.join(self.__root, uid), 'Ref')
        if not os.path.exists(user_dir):
            os.makedirs(user_dir)

        n_existing = len(os.listdir(user_dir))
        for i, signature in enumerate(signatures):
            outfile = os.path.join(user_dir, "R%03d.png" % (i + n_existing))
            cv2.imwrite(outfile, signature)

    def contains(self, uid):
        # type: (str) -> bool
        """
        Checks if the database contains a user.

        Parameters:
            uid (str): The id of the user to check.

        Returns:
            True if user with given id exists in database, else False.
        """
        return os.path.exists(os.path.join(self.__root, uid))

    def get(self, uid):
        user_dir = os.path.join(os.path.join(self.__root, uid), 'Ref')
        return [os.path.join(user_dir, i) for i in sorted(os.listdir(user_dir))]

    def get_all(self):
        """Returns a list of all saved users.
        """
        return [i for i in os.listdir(self.__root) if os.path.exists(os.path.join(os.path.join(self.__root, i), 'Ref'))]

    def remove(self, uid):
        # type: (str) -> bool
        """Deletes a user from the database.

        Parameters:
            uid (str): The id of the user to delete.

        Returns:
            True if deletion successful, else False.
        """
        if not self.contains(uid):
            return False

        shutil.rmtree(os.path.join(self.__root, uid))
        return True

    def clear(self):
        """Deletes all users from the database.
        """
        shutil.rmtree(self.__root)
        if not os.path.exists(self.__root):
            os.makedirs(self.__root)
