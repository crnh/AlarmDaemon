import voluptuous as vol
from voluptuous.schema_builder import Required


class X:
    def __init__(self, a: int, b: int) -> None:
        self.a = a
        self.b = b


# x = vol.Schema(vol.Object())
y = vol.Schema(vol.Object({vol.Required("a"): int, vol.Optional("b"): int}))

p = y(dict(dict(a=1, b=10)))

print(p)
