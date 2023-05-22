class InputTimeoutError(Exception):
    pass
def interrupted(signum, frame):
    raise InputTimeoutError
