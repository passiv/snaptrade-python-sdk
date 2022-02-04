class BaseModel:
    _gen_str_params: tuple = tuple()

    def _gen_str(self):
        params = []
        for param in self._gen_str_params:
            params.append(str(getattr(self, param)))

        return f"<{type(self).__name__}: {', '.join(params)}>"

    def __str__(self):
        return self._gen_str()

    def __repr__(self):
        return self._gen_str()
