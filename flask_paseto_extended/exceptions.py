class FlaskPasetoError(Exception):
    """
    Base class for all exceptions.
    """

    pass


class ConfigError(FlaskPasetoError):
    """
    An Exception occurred when the configurations are not completed.
    """

    pass


class EncodeError(FlaskPasetoError):
    """
    An Exception occurred when a PASETO encoding process failed.
    """

    pass


class DecodeError(FlaskPasetoError):
    """
    An Exception occurred when a PASETO decoding process failed.
    """

    pass
