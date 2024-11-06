import lmql


@lmql.query(model="chatgpt")
def tell_joke():
    '''lmql
    """A great good dad joke. A indicates punch line
    Q:[JOKE]
    A:[PUNCHLINE]""" where STOPS_AT(JOKE, "?") and \
                            STOPS_AT(PUNCHLINE, "\n")
    '''


print(tell_joke())
