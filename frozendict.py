class _pair(tuple):
    def __new__(cls, key, value):
        return super().__new__(cls, (key, value))

    def __hash__(self):
        return hash(self[0])


class _matcher:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, rhs):
        key, value = rhs
        if self.key == key:
            self.value = value
            return True
        return False


class frozendict(super):
    __slots__ = ()

    def __init__(self, base={}, /, **kwargs):
        super().__init__(
            frozenset,
            frozenset(_pair(key, value) for key, value in dict(base, **kwargs).items()),
        )

    def __repr__(self):
        name = type(self).__name__
        if self:
            return f'{name}({dict(self)!r})'
        else:
            return f'{name}()'

    def __contains__(self, key):
        return _matcher(key) in super().__self__

    def __len__(self):
        return len(super().__self__)

    def __eq__(self, rhs):
        return super().__self__ == rhs

    def __hash__(self):
        return hash(frozenset(self.items()))

    def __getitem__(self, key):
        m = _matcher(key)
        if m in super().__self__:
            return m.value
        raise KeyError

    def get(self, key, default=None):
        m = _matcher(key, default)
        m in super().__self__
        return m.value

    def __iter__(self):
        it = iter(super().__self__)
        return (key for key, _ in it)

    def keys(self):
        return iter(self)

    def values(self):
        it = iter(super().__self__)
        return (value for _, value in it)

    def items(self):
        it = iter(super().__self__)
        return (tuple(pair) for pair in it)

    def __or__(self, rhs):
        return type(self)(dict(self) | rhs)

    def __ror__(self, lhs):
        return type(self)(lhs | dict(self))

    __self__ = None
    __self_class__ = None
    __thisclass__ = None


if __name__ == '__main__':
    empty_dict = frozendict()
    assert str(empty_dict) == repr(empty_dict) == 'frozendict()'
    assert len(empty_dict) == 0
    assert list(empty_dict) == []
    assert 'key' not in empty_dict
    assert empty_dict.get('key') is None
    assert empty_dict.get('key', 'default') == 'default'
    assert set(empty_dict.keys()) == set()
    assert list(empty_dict.values()) == []
    assert list(empty_dict.items()) == []
    assert empty_dict == empty_dict
    assert empty_dict == frozendict()
    assert hash(empty_dict) == hash(frozendict())

    fdict = frozendict({'key': 'value', 3: (4, 5, 6)})
    assert str(fdict) in ["frozendict({'key': 'value', 3: (4, 5, 6)})", "frozendict({3: (4, 5, 6), 'key': 'value'})"]
    assert str(dict) == repr(dict)
    assert len(fdict) == 2
    assert set(fdict) == {'key', 3}
    assert 'key' in fdict
    assert ('key', 'value') not in fdict
    assert 'other' not in fdict
    assert fdict['key'] == 'value'
    assert fdict[3] == (4, 5, 6)
    assert fdict.get('key') == 'value'
    assert fdict.get('key', 'default') == 'value'
    assert fdict.get('other') is None
    assert fdict.get('other', 'default') == 'default'
    assert set(fdict.keys()) == {'key', 3}
    assert set(fdict.values()) == {'value', (4, 5, 6)}
    assert set(fdict.items()) == {('key', 'value'), (3, (4, 5, 6))}
    assert fdict == fdict
    assert fdict == frozendict({3: (4, 5, 6)}, key='value')
    assert fdict == frozendict({'key': 'value', 3: (4, 5, 6)})
    assert fdict == frozendict({3: (4, 5, 6), 'key': 'value'})
    assert fdict != frozendict({3: None, 'key': None})
    assert fdict != frozendict({3: (4, 5, 6)})
    assert fdict != empty_dict
    assert hash(fdict) == hash(frozendict({'key': 'value', 3: (4, 5, 6)}))
    assert hash(fdict) == hash(frozendict({3: (4, 5, 6), 'key': 'value'}))
    assert hash(fdict) != hash(frozendict({3: None, 'key': None}))

    zdict = {fdict: 0}
    assert zdict == {fdict: 0}
    assert zdict != {fdict: 1}
    assert zdict != {empty_dict: 0}

    assert isinstance(fdict | {}, frozendict)
    assert fdict | {} == fdict
    assert isinstance(fdict | {'other': None}, frozendict)
    assert fdict | {'other': None} == frozendict({'key': 'value', 3: (4, 5, 6), 'other': None})

    assert repr(list(frozendict(a=0))) == "['a']"
    assert repr(tuple(frozendict(a=0))) == "('a',)"
    assert repr(set(frozendict(a=0))) == "{'a'}"
    assert repr(frozenset(frozendict(a=0))) == "frozenset({'a'})"
    assert repr(dict(frozendict(a=0))) == "{'a': 0}"

    assert frozendict(a=0).__self__ is None
    assert frozendict(a=0).__self_class__ is None
    assert frozendict(a=0).__thisclass__ is None
