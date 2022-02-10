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

    def display_as_dict(self):
        import json

        return json.loads(json.dumps(self, default=lambda o: o.__dict__))

    @property
    def class_name(self):
        return type(self).__name__
