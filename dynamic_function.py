import types
import ast

def create_function(body, *arg_names):
    function_body = ast.parse(body).body
    args = [ast.arg(arg_name, ast.Name(arg_name, ast.Load(), lineno=1, col_offset=0)) for arg_name in arg_names]
    function_ast = ast.FunctionDef(
        name='',
        args=ast.arguments(args=args, defaults=[], kwonlyargs=[], kw_defaults=[]),
        body = function_body,
        decorator_list=[],
        lineno=1,
        col_offset=0
    )
    module = compile(ast.Module(body=[function_ast]), "<string>", "exec")
    function_code = next(c for c in module.co_consts if isinstance(c, types.CodeType))
    return types.FunctionType(function_code, globals())

code = """
print(a)
print(b)
return(a + b)
"""
f = create_function(code, 'a', 'b')
print(f(5, 6))
