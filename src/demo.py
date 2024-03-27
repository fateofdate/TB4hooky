from hooky.Hooker import CodeHooker


def local_hook(arg1, arg2):
    print("hello world\n")
    print("arg1:", arg1)
    print("arg2:", arg2)


@CodeHooker(_f=local_hook)
def target_function(): ...


if __name__ == "__main__":
    target_function("Create by", "Tuzi")