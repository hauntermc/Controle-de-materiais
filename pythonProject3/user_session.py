class UserSession:
    _instance = None

    @staticmethod
    def get_instance():
        if UserSession._instance is None:
            UserSession()
        return UserSession._instance

    def __init__(self):
        if UserSession._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            UserSession._instance = self
        self.username = None

    def set_user(self, username):
        self.username = username

    def get_user(self):
        return self.username
