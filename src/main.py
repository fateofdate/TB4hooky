import dis
import types

def ee(code):
    return eval(code)


# print(add.__code__.co_code)
# code_lst = add.__code__.co_code
#
# print(add.__code__.co_code[0])
# print(opcode.opname[code_lst[0]])
# print(opcode.opname[151])

def add(*args, **kwargs): ...

eval_code = getattr(ee.__code__, "co_code")
# eval_code = compile(ee)
a = ee.__code__
print(eval_code)
co = types.CodeType(
    a.co_argcount,
    a.co_kwonlyargcount,
    a.co_nlocals,
    a.co_stacksize,
    a.co_flags,
    eval_code,
    a.co_consts,
    a.co_names,
    a.co_varnames,
    a.co_filename,
    a.co_name,
    a.co_firstlineno,
    a.co_lnotab,
    a.co_freevars
    )


setattr(add, "__code__", co)
print(type(add))
add("print('hello word')")
print(dis.dis(add))

