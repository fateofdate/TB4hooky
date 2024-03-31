### [netLoader](https://github.com/fateofdate/TB4hooky/tree/main/TB4hooky/netLoader)
> 负责远程导入和网络交互的组件包
##### 基类

* ```class```<a name="BaseConnection">  **BaseConnection**</a>
>**Code source: [TB4hooky/netLoader/RemoteControl.py](https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/RemoteControl.py)**  



>* **instance method** ```__init__()->None``` 
>初始化方法，实现的时候需要重写方法可以初始化一些，有关远程调用的对象
>example
>```python
>class ImplementBaseConnection(BaseConnection):
>     def __init__():
>         # 初始化基于http的session对象
>         self.session = requests.Session()
>
>```
>*  **instance method** ```__enter__()->None```  
>BaseConnection 的子类实需要实现python ```context protocol``` 以确保IO流的正确运行，以及调用结束后的正确关闭.
>* **instance method** ```__exit__(exc_type, exc_cal, *args, **kwargs)->None```  
>BaseConnection 的子类需要实现此方法，以将在 ```__init__```方法中存入的IO流对象正确的关闭.
>* **instance method** ```get_remote_f(self, remote_addr: str, *args, **kwargs)->Any```   
>BaseConnection的子类需要实现此方法，用于获取远程函数信息.
>* **instance method** ```get_remote_package(self, remote_addr: str, *args, **kwargs)->Any```
>BaseConnection的子类需要实现此方法，用于获取远程包信息



##### netLoader 对象

* ```class``` **ConnectionRemote**

>**Code source: [TB4hooky/netLoader/RemoteControl.py](https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/RemoteControl.py)**



>* **instance method** ```get_remote_f(self, remote_addr, *args, **kwargs)->requests.Response```
>
>  ```remote_addr```为远程```url```地址, 基于HTTP协议实现的远程字节码获取方法，返回一个```requests.Response```对象.
>
>* **instance method** ```get_remote_package(self, remote_addr, *args, **kwargs) -> Any```
>
>  ConnectionRemote类中不实现，由ConnectionRemotePackage子类实现。

* ```class``` **ConnectionRemotePackage**

> **Code source: [TB4hooky/netLoader/RemoteControl.py](https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/RemoteControl.py)**



> * **instance method** ```def get_remote_package(self, remote_addr, *args, **kwargs) ->requests.Response:```
>
>   ```remote_addr```为远程```url```地址, 基于HTTP协议实现的远程包获取方法，返回一个```requests.Response```对象.



### [netLoader.AdapterConnectionRemote][https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/AdapterConnectionRemote.py]

> **Code source: [TB4hooky/netLoader/AdapterConnectionRemote.py][https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/AdapterConnectionRemote.py]**

* ```class``` **AdapterConnectionRemote(ConnectionRemote)**

> 如果需要自定义传输协议可以在此处重写```__exit__```, ```__enter__```,``` __init__```,``` get_remote_f``` 方法 ,具体参考**BaseConnection** <a href="#BaseConnection">**reference:  BaseConnection**</a> 
>
> ```
> For modify the method 'get_remote_f' should
> override method '_get_remote_f' and '__exit__', '__enter__' method
> you can save the IO object(example save the process buffer object) in 'self._session'
> or implement you own protocol.
> ```

* ```class``` **AdapterConnectionRemotePackage(ConnectionRemotePackage)**

> 如果需要自定义远程包传输的协议，可以在此处重写```__exit__```, ```__enter__```,``` __init__```,``` get_remote_f``` 方法 。



### [netLoader.DaynamicImport][https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/DaynamicImport.py]

> **Code source: [TB4hook/netLoader/DaynamicImport][https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/DaynamicImport.py]**



> **function** ```register(endpoint: str) -> None:```
>
> ```endpoint```: 远程服务器地址. 
>
> 注册包导入服务器远程服务器
>
> 
>
> **function** ```def unload(endpoint: str) -> None:```
>
> ```endpoint```: 远程服务器地址. 
>
> 从```sys.metapath```中卸载指定远程服务器

### [hooky][https://github.com/fateofdate/TB4hooky/tree/main/TB4hooky/hooky]

> 主要HOOK 逻辑实现

##### 基类

* ```abstract class``` **MetaCodeHooker**

> **Code source: [TB4hooky/hooky/Hooker.py][https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/hooky/Hooker.py]**

> hooker的核心方法抽象类 MetaCodeHooker
>
> 1. local hook
> 2. remote hook
>
> 如果要实现CodeHooker应该实现抽象类中以下的方法:
>
> 
>
> **staticmethod abstact method** ```def extract_co_code(*args, **kwargs): ...```
>
> 主要用于提取```co_code```对象
>
> 
>
> **abstract method** ```def swap_code_info(self, *args, **kwargs): ...```
>
> 用于交换```_f```和```_hook_obj```的```co_code```属性

### [hooky.Hooker.CodeHooker][https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/hooky/Hooker.py]

* ```class``` **CodeHooker**

> HOOK的核心类， 当我们需要在远程端调用的时候需要对函数进行序列化时可以使用```serialize_init(cls, func)-> CodeHooker```获得用于序列化函数的对象
>
> #### Local hooker example
>
> ```python
> from TB4hook.hooky.Hooker import CodeHooker
> 
> def test(a):
>     print("it's test.", a)
>     
> @CodeHooker(_f=test)
> def a(): ...
> 
> if __name__ == "__main__":
>     a("hello world")
>     
> # $> it's test.hello world
> ```
>
> #### Remote hooker example
>
> ```python
> from TB4hook.hooky.Hooker import CodeHooker
> 
> ##### remote server runing at http://127.0.0.1:8000
> # web api ''/test'
> def test(a, b):
>     print(a, b)
> 
> serialize = CodeHooker.serialize_init(test)
> # set count and get serialize result
> serialize_result = serialize.serialize_func(3)
> 
> # here is web server for return the serialize result ...
> 
> ##### client
> 
> @CodeHooker(_f="http://127.0.0.1:8000/test", remote=True)
> def client(): ...
>  
> if __name__ == "__main__":
>     client(1, 2)
>   
> # $> 12
> ```
>
> 
>
> **class method** ```serialize_init(cls, func) ->CodeHooker```
>
> ```func```: 远程调用时需要序列化的函数,或者静态方法，类方法，不可以是实例方法, 如果要用到实例的方法需要在函数内部导入```import```,并且在所有导入前方注册```register```然后导入包后进行实例化再使用，可以参考<a href="https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/netLoader/DaynamicImport.py">DaynamicImpoer.register</a>方法。
>
> 接收```func```获取可生成序列化字符串的```CodeHooker```对象。
>
> 
>
> **staticmethod method** ```def serialize_func(self, count: int) -> str:```
>
> ```count```: 设置远程端缓存数，即设置其声明周期。
>
> **返回值**: 序列化后的字符串

### [hooky.Hooker.InstanceHooker][https://github.com/fateofdate/TB4hooky/blob/main/TB4hooky/hooky/Hooker.py]

* ```class``` **InstanceHooker**

> 实例方法的hooker
>
> #### Instance method hook example
>
> ```python
> # 导入InstanceCodeHooker
> from hooky.Hooker import InstanceCodeHooker
> 
> class LocalMethod(object):
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
> ins = LocalMethod()
> 
> @InstanceCodeHooker(_f='sign', instance=ins)
> def sign():...
> 
> @InstanceCodeHooker(_f='chg', instance=ins)
> def another_sign():...
> 
> # 调用方法
> sign("hello")
> another_sign("world")
> print(ins.flag)
> 
> # $> hello world
> #    hello
> #    world
> ```



