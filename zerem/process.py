
def process(func):
    def processed():
        return func

    return processed