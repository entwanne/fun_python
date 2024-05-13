#import ast
import inspect
import itertools
import textwrap
#from contextlib import ExitStack


class Stop(Exception):
    pass


class Catch:
    def __enter__(self):
        return self

    def __exit__(self, cls, exc, tb):
        if cls and issubclass(cls, Stop):
            return True


class Block:
    def __enter__(self):
        #print(inspect.stack())
        #print(inspect.trace())
        #print(inspect.currentframe())
        #print(inspect.getouterframes(inspect.currentframe()))
        #print(inspect.getsource(inspect.currentframe()))
        #print('---')

        caller_frame_info = inspect.stack()[1]
        global_frame_info = inspect.stack()[-1]
        source = inspect.getsource(global_frame_info.frame)
        source_lines = source.splitlines()
        #print(source)

        #print(caller_frame_info)
        #print(caller_frame_info.lineno)
        first_line = caller_frame_info.lineno
        #print(source_lines[first_line])
        block_lines = []

        for i in itertools.count(first_line):
            line = source_lines[i]
            code = textwrap.dedent('\n'.join(block_lines + [line]))
            if code.startswith(' '):
                break
            block_lines.append(line)

        #print(block_lines)
        block_source = textwrap.dedent('\n'.join(block_lines))
        #print(block_source)

        #tree = ast.parse(block_source)
        #from pprint import pprint
        #pprint(ast.dump(tree))
        self._code = compile(block_source, '<block>', 'exec')

        raise Stop

    def __exit__(self, *_):
        return

    def __call__(self, *args, **kwargs):
        exec(self._code)

#with Catch(), Block() as b1:
with Catch(), (b1 := Block()):
    print('test')
    print('test2')


def f():
    with Catch(), (b2 := Block()):
        print('foo')
        print('bar')
    return b2

block2 = f()
print('end')

block2()
b1()
