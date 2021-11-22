## 第8章：IO库

### 8.1 IO类

为了支持不同种类的IO处理操作，除了istream和osteam之外，标准库还定义了一些IO类型；

```
iostream	isstream, wistream  从流读取
			ostream,  wostream  向流写入
			iostream, wiostream 读写流

fstream		ifstream, wifstream 从文件读取
			ofstream, wofstream 向文件写入
			fstream,  wfstream  读写文件

sstream		istringstream, wistringstream 从string读
			ostringstream, wostringstream 向string写
			stringstream,  wstringstream  读写string
```

####  8.1.1 IO对象无拷贝或赋值

不能拷贝或对IO对象赋值；

#### 8.1.2 条件状态

IO操作的一个问题是可能发生错误。一些是可恢复的，其他可能超出应用程序修正范围；

下面列出IO类所定义的一些函数和标志，帮助访问和操纵流的条件状态；

```c++
strm::iostate	strm是一种IO类型，iostate是一种机器相关的类型，提供了表达条件状态的完整功能
strm::badbit	指出流已崩溃
strm::failbit	指出一个IO操作失败了
strm::eofbit	指出流到达了文件结束
strm::goodbit	指出流未处于错误状态
s.eof()			若流s的eofbit置位，则返回true
s.fail()		若流s的failbit或badbit置位，则返回true
s.bad()			若流s的badbit置位，则返回true
s.good()		若流处于有效状态则返回true
s.clear()		将流s中所有条件状态位复位，将流的状态设置为有效
s.clear(flags)	根据给定的flags置位，将流s中对应条件状态复位。flags的类型为strm::iostate
s.setstate(flags)根据给定的flags标志位，将s中对应条件状态位置位
s.rdstate()		返回流s的当前条件状态
```

确定一个溜对象啊sing的状态的最简单的方法是将它当做一个条件来使用

```c++
while(cin>>word)
	//ok：读操作成功
```

使用good或fail是确定流的总体状态的正确方法，实际上，我们将流当做条件使用的代码就等价于!fail()；

管理条件状态：流对象的rdstate成员返回一个iostate值，对应流的当前状态。setstate操作将给定的条件位置位，表示发生了对应错误。执行clear()后，调用good会返回true；可以这样使用这些成员：

```c++
auto old_state = cin.rdstate();
cin.clear();
process_input(cin);
cin.setstate(old_state);
```

为了复位单一的条件状态位，首先用rdstate读出当前条件状态，然后用位操作将所需位复位来生成新的状态；

```c++
//复位failbit和badbit，保持其他标志位不变
cin.clear( cin.rdstate() & ~cin.failbit & ~cin.badbit );
```

#### 8.1.3 管理输出缓冲

每个输出流都管理一个缓冲区，用来保存程序读写的数据。文本串可能立即打印也可能被操作系统保存在缓冲区中，随后再打印；

刷新输出缓冲区：

```c++
endl	//换行然后刷新缓冲区
flush	//不附加任何额外字符
ends	//加一个空格，刷新缓冲区
```

如果想每次输出操作后都刷新缓冲区，可以使用unitbuf操纵符。它告诉流在接下来的每次写操作之后都进行一次flush操作。而nonunitbuf操纵符则重置流，使其恢复使用正常的系统管理的缓冲区刷新机制；

```c++
cout << unitbuf;
cout << nounitbuf;
```

当一个输入流被关联到一个输出流时，任何试图从输入流读取数据的操作都会先刷新关联的输出流；

```c++
x.tie(&o);//将流x关联到输出流o
```

### 8.2 文件输入输出

头文件fstream定义了三个类型来支持文件IO；//ifstream，ofstream，fstream

```c++
fstream fstrm;//创建一个未绑定得到文件流
fstream fstrm(s);//创建一个fstream并打开名为s的文件;
fstream fstrm(s, mode);//与前一个类似，但按指定mode打开文件
fstrm.open(s);//打开名为s的文件，并与fstrm绑定；
fstrm.close();//关闭fstrm
fstream.is_open();//指出与fstrm关联的文件是否成功打开且尚未关闭
```

#### 8.2.1 使用文件流对象

```c++
ifstream in(ifile);//构造一个ifstream并打开文件
ofstream out;//输出文件流，未关联到任何文件 
//和cin，cout是一样的
```

#### 8.2.2 文件模式

每个流都有一个关联的文件模式，用来指出如何使用文件。

```c++
in 		以读方式
out		以写方式
app		每次写操作前定位到文件末尾
ate		打开文件后立即定位到文件末尾
trunc	截断文件
binary	以二进制方式进行IO
```

- 只有当out也被设定时，才可设定trunc模式

- 只要trunc没被设定，就可以设定app模式

- 默认情况下，即使没有指定trunc，以out模式打开的文件也会被截断。为了保留out模式打开的文件的内容，我们必须同时指定app模式，只要只会将数据追加写到文件末尾；或者同时指定in模式，即打开文件同时进行读写操作；

以out模式打开文件会丢弃已有数据

```c++
//在这几条语句中，file1都被截断
ofstream out("file1");
ofstream out("file1",ofstream::out);
ofstream out("file1",ofstream::out|ofstream::trunc);
//为了保留文件内容，必须显式指定app模式
ofstream app("file2",ofstream::app);
ofstream app2("file2",ofstream::app|fstream::out);
```

每次调用open时都会确定文件模式

### 8.3 string流

```c++
sstream strm;	
sstream strm(s);//strm是一个sstream对象，保留string s的一个拷贝；这个函数是explicit的
strm.str();	//返回strm保存的string的拷贝
strm.str(s);//将string s拷贝到strm中返回void
```

#### 8.3.1 使用istringstream

当某些工作是对整行文本进行处理，而其他的一些工作是处理行内的单个单词时，通常可以使用istringstream；

#### 8.3.2 使用ostringstream

当逐步构造输出，希望最后一起打印的时候，ostringstream很有用；

​                      