class Session:
    __instance = None
    username = None
    events = None

    @staticmethod
    def getInstance():
        if Session.__instance == None:
            Session()
        return Session.__instance

    def __init__(self):
        if Session.__instance != None:
            raise Exception("You can't reinstantiate a Session")
        Session.__instance = self

    def reset():
        Session.__instance = None
        Session.username = None
        Session.events = None