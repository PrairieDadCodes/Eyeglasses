from construct import *


class ErrorMessage(Construct):

    def __init__(self, message):
        super().__init__()
        self.message = message
        self.flagbuildnone = True

    def _parse(self, stream, context, path):
        raise ExplicitError("Error field was activated during parsing: " + self.message, path=path)

    def _build(self, obj, stream, context, path):
        raise ExplicitError("Error field was activated during building: " + self.message, path=path)

    def _sizeof(self, context, path):
        raise SizeofError("Error does not have size, because it interrupts parsing and building: " + self.message,
                          path=path)


class ValidatorWarning(SymmetricAdapter):
    r"""
    Outputs a warning instead of raising an exception when validation fails.
    """

    def __init__(self, subcon, validator):
        super().__init__(subcon)
        self._validate = lambda obj, ctx, path: validator(obj, ctx)

    def _decode(self, obj, context, path):
        if not self._validate(obj, context, path):
            print(context)
            print(f"WARNING: object ({path}) failed validation: {obj}")
        return obj

    def _validate(self, obj, context, path):
        raise NotImplementedError


Unused = lambda num_bytes: ValidatorWarning(Bytes(num_bytes), lambda obj, ctx: set(obj) == {0})

CheckedFlag = ValidatorWarning(Flag, lambda obj, ctx: obj in {0, 1})

CheckedEnum = lambda T: ValidatorWarning(T, lambda obj, ctx: int(obj) in T.decmapping)


def check_flags(obj, ctx):
    for flag in obj:
        if obj[flag] and flag.startswith("UNUSED"):
            return False
    return True


CheckedFlagsEnum = lambda T: ValidatorWarning(T, lambda obj, ctx: check_flags(obj, ctx))
