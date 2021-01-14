class DevelopmentConfig():
    TESTING = False
    WTF_CSRF_ENABLED = False


class TestingConfig():
    TESTING = True
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False
