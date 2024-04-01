# TB4hooky
![](https://img.shields.io/badge/python-v3.7.16-1E90FF.svg) ![GitHub repo file or directory count](https://img.shields.io/github/directory-file-count/fateofdate/TB4hooky) ![GitHub Repo stars](https://img.shields.io/github/stars/fateofdate/TB4hooky) ![GitHub watchers](https://img.shields.io/github/watchers/fateofdate/TB4hooky) ![GitHub forks](https://img.shields.io/github/forks/fateofdate/TB4hooky)

### 简介
> TB4hooky 是一个由python编写的代码hook框架，支持```remote hook```和```local hook``` 
> 支持自定义序列化协议，支持远程导入包模块，开箱即用。
### 使用场景
> 1. 持续集成, 对于经常更新的核心算法，核心函数等等可以进行```remote hook``` 并且将核心代码放在远程服务器上，当远程代码变动或者更新时，本地函数将在缓存次数耗尽后，自动拉取远程服务器的代码进行热更新。
> 2. 核心算法保护，以及动态校验算法，即利用```remote hook``` 机制去实现核心校验函数，本地并不实现核心函数，并且将远程服务器上的实现代码进行动态变化，就可以做到动态算法校验， 从而实现提高逆向难度的效果。
> 3. 接口稳定性，依赖倒置，使得编码依赖于抽象而不依赖于底层实现，与实现解耦合，利用```local hook```机制对于接口类进行hook, 即可以在不使用继承，组合的情况下对实现类方法，并且接口类的抽象具有稳定性，不会因为底层代码的变化影响到，高层的设计。
> 4. 分布式计算，通过```remote hook```机制中心服务器下发运算任务给计算节点，计算节点不停的从中心服务器去抓取算法字节码。
>5. 量化交易，当多个交易机需要同步热更新控制机上的交易策略时可以通过```remote hook```机制实时运行新的策略。
### 安装
```pip install TB4hooky```
### 动态导入原理
>```mermaid
>   graph TB
>       BulitinImport(Builtin importer) --> |find| bReturn(return pkg)
>   BulitinImport(Builtin importer) -.not find.-> frozenImport(Frozen importer)
>   frozenImport(Frozen importer) --> |find| fReturn(return pkg)
>   frozenImport(Frozen importer) -.not find.->CustomImporter(Custom Importer)
>    CustomImporter(Custom Importer) ==req==> RemoteImportServer[Remote import server]
>   RemoteImportServer[Remote import server] ==resp==> CustomImporter(Custom Importer) 
>    CustomImporter(Custom Importer) --> |find| creturn(return pkg)
>    CustomImporter(Custom Importer) -.not find.-> sysexcept(Sys.ExceptionGlobalHook)
>   sysexcept(Sys.ExceptionGlobalHook) --> handle(Exception handle funcion)
>   handle(Exception handle funcion) --> filehandle(FileHandle object)
>   filehandle(FileHandle object) ==req==> RemoteImportServer[Remote import server]
>   RemoteImportServer[Remote import server] ==resp==> filehandle(FileHandle object)
>    filehandle(FileHandle object) ==resp==>handle(Exception handle funcion)
>   handle(Exception handle funcion) --> |find| freturn(return pkg)
>   handle(Exception handle funcion) -.not find.-> raiseImprotError(raise ImportError)
> ```

### 快速入门
> ```local hook```
> 将本地实现函数的字节码替换到hook的函数中使其实现本地函数的功能  
 ### 普通函数的hook
> ```python
> from hooky.Hooker import CodeHooker  
> 
> def local_hook(arg1, arg2):
>     print("hello world\n")
>     print("arg1:", arg1)
>     print("arg2:", arg2)
>   
> @CodeHooker(_f=local_hook)
> def target_function(): ...
> 
> if __name__ == "__main__":
>     target_function("Create by", "Tuzi")
> ```
> **运行结果**
> ```
> $> hello world
>    Create by Tuzi
> ``` 
 
### 类方法的HOOK
>```python
> from hooky.Hooker import CodeHooker
>
># 接口实现类
>class Trait(object):
>    @staticmethod
>    def local_sign(*args, **kwargs):
>        print("123456")
>
>    @staticmethod
>    def local_init(cls, *args, **kwargs):
>        print('class method verify')
>        return cls()
>
># 接口类
>class Spider(object):
>    @classmethod
>    @CodeHooker(_f=Trait.local_init)
>    def local_init(cls): ...
>
>
>    @CodeHooker(_f=Trait.local_sign)
>    def local_sign(self): ...
>
>    def use(self):
>        print("use load")
>        self.local_sign()
>
>    @staticmethod
>    @CodeHooker(_f=Trait.local_sign)
>    def llocal_sign(*args, **kwargs): ...
># classmethod hook
>spider = Spider.local_init()
># method hook
>spider.local_sign()
># normal call instance method
>spider.use()
># staticmethod hook
>Spider.llocal_sign()
>
>
> ```
> **运行结果**
> ```
> $> class method verify
>    123456
>    123456
>    use load
>    123456
>```
### 远程hook
> ```remote hook``` 将远程服务器上的方法字节码拉到本地后进行hook。
>
>这里我们先定义一个```远程服务端```，这里我们使用Flask 搭建
> ```python
>from flask import Flask
>from hooky.Hooker import CodeHooker
>from netLoader.DaynamicImport import register
>
>app = Flask(__name__)
>
># 这里我们定义一个远程包导入服务器并且安装模块
>register("http://127.0.0.1:9000")
>
>
># 实现一个远程函数
>
>def sign(flags):
>   print(f"It's a sign function, flag is {flags}")
>
># 实例化序列化类
>serializer = CodeHooker.serialize_init(sign)
>
># 设置远程缓存数为3并且获取反序列化结果
>serialize_result = serializer.serialize_func(3)
>
>
># 定义一个路由用于接收请求
>@app.route("/sign")
>def get_sign():
>   return serialize_result
>
># 启动服务
>app.run(debug=True, host="0.0.0.0", port=8000)
>
>```
> 现在我们开始进行```remote hook```
> 
>```python 
># 导入CodeHooker
>from hooky.Hooker import CodeHooker
>
># remote 地址为我们启动的服务器地址并且为sign接口
>@CodeHooker(_f="http://127.0.0.1:8000/sign", remote=True)
>def local_sign(): ...
>
>
>local_sign('hello world')
> 
>```
> **运行结果**
>```
>$> It's a sign function, flag is hello world
>```
> 远程hook同样可以进行```classmethod``` 和 ```staticmethod``` 的hook同```local hook``` 一样,这里就不再演示了, 不过值得注意的是，```remote hook```的时候远程服务端不可以直接在函数内部进行实例化，我们拥有如下的解决方案，
需要利用到远程导入库，此时需要再准备一台服务端作为包导入端并且启动web服务，并且在客户端与服务端安装远程钩子， 可以将写好的类代码放到包导入端中，然后在服务端的函数中进行导入后使用。
>
>```python
># 方式一
>from netLoader.DaynamicImport import(   
>   register,   
> )
>
># 注册远程包导入服务器地址
>register("http://127.0.0.1:9000")
>
>
>"""
> 客户端代码或者服务端代码
> example:
> # 服务端
> def sign():
>   import fib # 这是自己实现的类
>   f = fin()  # 实例化
>   f.count()  # 调用实例化方法
># 实例化序列化类
>serializer = CodeHooker.serialize_init(sign)
>
># 设置远程缓存数为3并且获取反序列化结果
>serialize_result = serializer.serialize_func(3)
>
># 后面的步骤就和上面一样了，定义接口返回序列化以后的值即可
>"""
>
># 卸载钩子
>unload("http://127.0.0.1:9000")
>
># 方式二
>str = """
>class Sign():
>   def sign(self):
>       print("it's sign method in class Sign.")
>
>"""
># 远程端定义如下函数
>def sign():
>   cp_obj = complie(str, "", "exec")
>   exec(cp_obj)
>
># 不过这种方式作者认为不够优雅还是建议使用第一种远程导入的模块.
>```
>
### 本地实例方法HOOK
> 上面我们用```local hook```hook 类方法，实例方法，静态方法，但是实现函数上我们用，静态函数，函数等进行的实现，现在我们将引入一个新的对象，```InstanceCodeHooker```来帮助我们进行实例方法实现hook对象的修改。
>
>```python
># 导入InstanceCodeHooker
>from hooky.Hooker import InstanceCodeHooker
>
>class LocalMethod(object):
>
>   def __init__(self):
>       self.flag = 'hello world'
>
>   def sign(self, flag):
>       print(self.flag)
>       self.flag = flag
>
>   def chg(self, flag):
>       print(self.flag)
>       self.flag = flag
>
>
>ins = LocalMethod()
>
>@InstanceCodeHooker(_f='sign', instance=ins)
>def sign():...
>
>@InstanceCodeHooker(_f='chg', instance=ins)
>def another_sign():...
>
># 调用方法
>sign("hello")
>another_sign("world")
>print(ins.flag)
>```
>**运行结果**
>```
>$> hello world
>    hello
>    world
>```
### 远程导入包
> 由于python包导入机制过于复杂，导致在导入一些比较大的库的时候，```hook_meta```没法很好的兼容其导入方式，所以添加了辅助函数 ```remote_import ```,来尽量调和该问题可以尝试通过```try except```来捕捉相关异常然后通过
> ```remote_import```来显示的导入该包,该函数接收一个字符串，在这之前需要进行注册```register```，如果在这之前没有注册则什么都不会执行.
>
> ```python
> # 导入netLoader
>  from TB4hooky.netLoader.DaynamicImport import register, remote_import, unload
> # 注册包中心
> register("http://127.0.0.1:9000")
>
> # 尝试导入
> try:
>   import torch
> except Exception as _:
> # 显示导入
>   remote_import('torch')
> # 卸载钩子
> unload("http://127.0.0.1:9000") 
>```

>#### 更新日志
> * 28.03.2024 - v0.1.5 - alpha
>
>   * \- remote/local hook
> * 29.03.2024 - v0.1.6a
>   * \- fix bug remote import 
> * 29.03.2024 - v0.1.7a
>   * \- fix bug remote import 
> * 01.04.2024 - v0.1.8a
>   * \- add remote import API ```remote_import```
> * 01.04.2024 - v0.1.8b
><hr>
### Create by Tuzi 