from sys import argv
from requests import get

class NoAPIKeySpecified(Exception):
    def __init__(self, argv, message="You should specify your API key first. API keys can be found at https://t.me/BotFather"):
        self.argv = argv
        self.message = message
        super().__init__(self.message)
class TooManyArgs(Exception):
    def __init__(self, argv, message="Too many arguments, please specify API key only."):
        self.argv = argv
        self.message = message
        super().__init__(self.message)
class BotNotExisting(Exception):
    def __init__(self, argv, message="Either no internet, or this bot doesn't exist. Make sure you pasted your api token correctly."):
        self.argv = argv
        self.message = message
        super().__init__(self.message)

def CheckForAPIKey():
    if len(argv)==1:
        raise NoAPIKeySpecified(argv)
    if len(argv)>2:
        raise TooManyArgs(argv)
    if len(argv)==2:
        response = get(f'https://api.telegram.org/bot{argv[1]}/getMe')
        if response.status_code==200:
            return True
        else:
            raise BotNotExisting(argv)
##testing area:
#CheckForAPIKey()

