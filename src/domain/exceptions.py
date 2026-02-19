class DocumentReaderError(Exception):
    pass


class DocumentReadError(DocumentReaderError):
    pass


class LLMError(Exception):
    pass


class LLMConnectionError(LLMError):
    pass


class LLMResponseError(LLMError):
    pass
