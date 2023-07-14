from enum import IntEnum


class ErrorCode(IntEnum):
    Success = 0
    JobObjectCreationFailed = 1
    CompletionPortCreationFailed = 2
    FailedToAssociateJobWithCompletionPort = 3
    ProcessCreationFailed = 4

    @classmethod
    def of(cls, code: int):
        if code not in tuple(cls):
            return None
        return ErrorCode(code)

    @property
    def message(self):
        if self == ErrorCode.Success:
            return None
        return self.name


class WinJobsterCallFailedException(Exception):
    ERROR_CODES = tuple(ErrorCode)

    def __init__(self, error_code):
        self.error_code_value = error_code
        self.error_code = ErrorCode.of(error_code)
        self.message = self.get_error_message()
        super(WinJobsterCallFailedException, self).__init__(self.message, self.error_code, self.error_code_value)

    def get_error_message(self):
        if self.error_code == ErrorCode.Success:
            return "WinJobster call succeeded"

        if self.error_code is None:
            message = "UnknownError({})".format(self.error_code_value)
        else:
            message = self.error_code.message

        return "WinJobster call failed: '{}'".format(message)
