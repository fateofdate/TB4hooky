import inspect


class Inspect(object):
    """Inspect function type"""
    @staticmethod
    def check_function_type(_obj):
        if not inspect.isfunction(_obj) and not inspect.ismethod(_obj):
            raise TypeError(f"Error type is {type(_obj)} should be 'function'.")

    @staticmethod
    def check_string_type(_obj):
        if not isinstance(_obj, str):
            raise TypeError(f"Error type is {type(_obj)} should be 'str' because you use the remote hook.")

