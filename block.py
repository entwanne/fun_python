import ast
import inspect
import itertools
import textwrap
from functools import partial


class _Stop(Exception):
    pass


class _BlockArguments:
    def __iter__(self):
        raise _Stop


class _Block:
    def __init__(self, exit_callable=None):
        self.exit_callable = exit_callable

    def __enter__(self):
        caller_frame_info = inspect.stack()[1]

        for module_frame_info in inspect.stack()[1:]:
            if module_frame_info.function == '<module>':
                break

        source = inspect.getsource(module_frame_info.frame)
        source_lines = source.splitlines()

        first_line = caller_frame_info.lineno
        block_lines = []

        (block_def,) = ast.parse(source_lines[first_line - 1].strip() + ' pass').body
        assert isinstance(block_def, ast.With)
        (block_item,) = block_def.items
        block_args = block_item.optional_vars
        assert isinstance(block_args, ast.Tuple)
        self.block_arg_names = [name.id for name in block_args.elts]

        for i in itertools.count(first_line):
            try:
                line = source_lines[i]
            except IndexError:
                break
            code = textwrap.dedent('\n'.join(block_lines + [line]))
            if code.startswith(' '):
                break
            block_lines.append(line)

        block_source = textwrap.dedent('\n'.join(block_lines))

        self._code = compile(block_source, '<block>', 'exec')

        return _BlockArguments()

    def __exit__(self, exc_type, exc_val, exc_tb):
        ret = exc_type and issubclass(exc_type, _Stop)
        if ret and self.exit_callable is not None:
            self.exit_callable(self)
        return ret

    def __call__(self, *args, **kwargs):
        loc = locals() | kwargs | dict(zip(self.block_arg_names, args))
        exec(self._code, locals=loc)


class Block(_Block):
    def __init__(self):
        super().__init__()

    @staticmethod
    def call(func, /, *args, **kwargs):
        return _Block(partial(func, *args, **kwargs))


def range_each(start, stop, block):
    for i in range(start, stop):
        block(i)


with Block.call(range_each, 0, 10) as (i,):
    print(i, '!')


with Block.call(range_each, 0, 0) as (i,):
    print(i, '?')


with (block1 := Block()) as ():
    print('block1 - foo')
    print('block1 - bar')


def get_block():
    with (block := Block()) as ():
        print('block2 - foo')
        print('block2 - bar')
    return block


block2 = get_block()

print('tests')
block2()
block1()
block2()
