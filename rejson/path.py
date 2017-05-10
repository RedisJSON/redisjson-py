class Path(object):
    strPath = ''

    @staticmethod
    def rootPath():
        return '.'

    def __init__(self, path):
        self.strPath = path