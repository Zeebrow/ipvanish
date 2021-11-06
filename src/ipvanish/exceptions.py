
class InvalidConfigurationError(Exception):
    """
    Raise when the app fails to initialize, and prevents 
    normal usage in a non-recoverable way.

    For recoverable errors, us InvalidConfigurationWarning
    """
    pass


class InvalidConfigurationWarning(Exception):
    """
    Raise when app configuration deviates from what the user defined,
    but the app is able to continue running.

    This should always print a message to the console, or resultin a pop-up window.
    """
    pass
