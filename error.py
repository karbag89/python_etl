# ----------------------------------------------------------------------------
# Python library dependency
# ----------------------------------------------------------------------------

from flask import json


# ----------------------------------------------------------------------------
# Description :
# The Error class getting error data (error_code, error_message), creating and
# returning error log message in JSON body.
# ----------------------------------------------------------------------------
class Error:
    '''Takes error code and error message values, returns error log message.'''
    # -------------------------------------------------------------------------
    # Description :
    # This function getting error code and error message data, creating and
    # returning error log message in JSON body.
    #
    # Parameters :
    #     error_code      Error code value.
    #     error_message   Error message text value.
    #
    # Return :
    #     data            Error log message in JSON format.
    #
    # -------------------------------------------------------------------------
    def errorMessage(error_code, error_message) -> json:
        '''Creating error log message in JSON body.'''
        data = {"code": error_code,
                "message": error_message}
        return data
