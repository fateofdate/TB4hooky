from hooky.Hooker import CodeHooker


def hello(arg):
    print("Hello world")


@CodeHooker(_f=hello)
def hello_world(): ...


if __name__ == "__main__":
    hello_world("Hello World.")

