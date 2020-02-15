
def get_token():
    try:
        file = open('token.txt', "r")
        return file.read()

    except FileNotFoundError:
        return "No Token.txt file"


greetings = ["Greetings", "hello", "Wassap", "Hi", "Howdy", "Good day", ("What a day we're having, eh,", "?"), "suh"]

token = get_token()
