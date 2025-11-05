import defer


@defer.apply
def make_list(value, dst=defer.deferred(list)):
    dst.append(value)
    return dst


x = make_list(4)
assert x == [4]
y = make_list(5)
assert y == [5]

output = [0]
z = make_list(6, output)
assert z == output == [0, 6]
