class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class GeneratorError(Error):
    """
    Exception raised for generator errors

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class GeneratorConfigError(Error):
    """
    Exception raised for generator configuration errors

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class TemplateError(Error):
    """
    Exception raised for template errors

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message
