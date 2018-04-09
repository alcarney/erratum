from functools import wraps


class Annotater:
    """Annotates exception messages with a URL so users can find out more
    about the particular error.
    """

    def __init__(self, url):
        self.url = "More info --> " + url

    def __enter__(self):
        return self

    def __exit__(self, err_type, err, traceback):

        if err is None:
            return

        args = err.args
        print(len(args))

        if len(args) == 0:
            new_args = tuple([self.url])

        if len(args) == 1:
            new_args = tuple(["{}\n{}".format(args[0], self.url)])

        if len(args) > 1:
            new_args = tuple([*args, self.url])

        err.args = new_args


class Error:
    """This is the definition of an error, it consists of

    - A url to point people in the direction to possibly fix their issue.
    - A description on how to fix it.
    - Methods for annotating exceptions with this info.
    """

    url = ""

    @classmethod
    def annotate(cls):

        def decorator(f):

            @wraps(f)
            def wrapper(*args, **kwargs):

                with Annotater(cls.url):
                    return f(*args, **kwargs)

            return wrapper

        return decorator
