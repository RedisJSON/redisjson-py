class Path(object):
    """
    This class represents a path in a JSON value
    """
    strPath = ''

    @staticmethod
    def rootPath():
        "Returns the root path's string representation"
        return '.'

    def __init__(self, path):
        """
        Make a new path based on the string representation in `path`
        """
        self.strPath = path