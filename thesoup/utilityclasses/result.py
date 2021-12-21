class Result:
    """
    This class is supposed to be similar in principle to Rust's Result.
    """
    @classmethod
    def success(cls, value) -> 'Result':
        """
        This returns a success object with `val` set o `value`
        :param value:
        :return: A success `Result` object.
        """
        res = Result()
        res.is_success = True
        res.val = value
        return res

    @classmethod
    def err(cls, err_val) -> 'Result':
        """
        This returns a error object with `err` set o `err_val`
        :param err_val:
        :return: A failure `Result` object.
        """
        res = Result()
        res.is_success = False
        res.err = err_val
        return res

    def __call__(self, *args, **kwargs):
        if self.is_success:
            return self.val
        else:
            return self.err

    def __bool__(self):
        return self.is_success
