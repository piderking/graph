class ShapeNotFound(Exception):
    def __init__(self, _type: str, *args: object) -> None:
        print("{}: Shape not found!".format(_type))
        super().__init__(*args)

class NoURLSpecified(Exception):
    def __init__(self, _type: str, *args: object) -> None:
        print("{}: No URL Specified for Shape, data structures can be used without a URL but transformations cannot!".format(_type))
        super().__init__(*args)