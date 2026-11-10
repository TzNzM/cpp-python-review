# 1.QWidget的继承调用
//NoWheelSpinBox
//       ↓ 继承
//   QSpinBox
//       ↓ 继承
//    QWidget

//我要创建 NoWheelSpinBox
//        ↓
//先构造它的父类 QSpinBox
//        ↓
//调用 QSpinBox(pParent)
//        ↓
//再执行 NoWheelSpinBox 构造函数体
//        ↓
//{
//}
NoWheelSpinBox::NoWheelSpinBox(QWidget *pParent)
    : QSpinBox(pParent)
{

}
# 2.Connect函数的调用
//connect(发送信号的对象, 信号, 接收信号的对象, 槽函数);
//& 用来取得“成员函数的地址”，更准确说是成员函数指针
connect(pBrowseFileButton,&QPushButton::clicked,this,&MainWidget::OnBrowseFileClicked);

## 跨线程使用的案例
**可以。子线程发出信号，主线程可以执行对应的槽函数。** 这也是 Qt 中后台任务更新界面的常见方式。

关键在于：**接收对象属于哪个线程，以及使用什么连接方式。**

例如，你的 Worker 在后台线程，MainWidget 在主线程：

```cpp
connect(pWorker, &ReliableSenderWorker::SignalSendProgress,
        this, &MainWidget::OnSendProgressChanged);
```

后台线程发送进度：

```cpp
emit SignalSendProgress(10, 100);
```

主线程执行槽函数并更新界面：

```cpp
void MainWidget::OnSendProgressChanged(int completed, int total)
{
    m_pSendProgressBar->setMaximum(total);
    m_pSendProgressBar->setValue(completed);
}
```

这里的过程是：

```text
后台线程 emit 信号
        ↓
把槽调用及参数放入主线程的事件队列
        ↓
主线程事件循环处理这个事件
        ↓
主线程执行槽函数，更新 UI
```

**不同连接方式决定槽在哪里执行：**

| 连接方式 | 执行方式 |
|---|---|
| `Qt::AutoConnection`，默认 | 发出信号的当前线程与接收对象所属线程相同，就直接调用；不同就排队调用 |
| `Qt::DirectConnection` | 立即在发出信号的当前线程中执行槽 |
| `Qt::QueuedConnection` | 排队，由接收对象所属线程的事件循环执行槽 |

因此，跨线程更新界面时，也可以明确指定：

```cpp
connect(pWorker, &ReliableSenderWorker::SignalSendProgress,
        this, &MainWidget::OnSendProgressChanged,
        Qt::QueuedConnection);
```

此处 `this` 是主线程中的 MainWidget，所以槽会在主线程执行。**不要使用 `DirectConnection` 让后台线程执行操作 UI 的槽。**

还有两点要注意：

- 接收线程必须有正在运行的事件循环。主线程如果被耗时操作或 `wait()` 卡住，排队的槽就暂时无法执行。
- 信号槽连接可以安排跨线程调用，但普通函数调用不会自动切换线程：

  ```cpp
  pWorker->SomeFunction(); // 在调用这行代码的线程中执行
  ```

对于你的项目，就是 **Worker 在后台处理文件发送，通过信号把日志、进度和结果交给主线程显示**。

## 信号槽机制的底层实现方式
Qt 信号槽的底层主要由**元对象系统、moc 生成的代码、连接记录和事件队列**共同实现。我核对了你本机 Qt 5.14.2 的源码，可以按“一次信号如何到达槽函数”来理解。

**1. 编译时，moc 为类生成额外代码**

你在类中写：

```cpp
class ReliableSenderWorker : public QObject
{
    Q_OBJECT

signals:
    void SignalSendProgress(int completed, int total);
};
```

`Q_OBJECT` 配合 Qt 的元对象编译器 `moc`，生成：

- 类名、信号和槽等元信息。
- 信号函数的实现。
- 根据方法编号调用成员函数的辅助代码。

所以信号通常只需要声明，函数实现由 moc 生成。

你项目里就有实际生成的 [moc_mainwidget.cpp](</D:/Qt test/MyServer/build-upload-check/debug/moc_mainwidget.cpp:107>)，里面可以看到类似：

```cpp
switch (_id)
{
    // ……
    case 6:
        _t->OnSendProgressChanged(/* 从参数数组中取出两个 int */);
        break;
}
```

这是元对象系统调用槽的一种路径。新式成员函数指针连接还可以通过 Qt 保存的可调用对象直接调用目标函数。

**2. `connect()` 保存连接关系**

例如：

```cpp
connect(pWorker, &ReliableSenderWorker::SignalSendProgress,
        pMainWidget, &MainWidget::OnSendProgressChanged);
```

Qt 会建立一条连接记录，保存：

```text
发送对象：pWorker
信号标识：SignalSendProgress
接收对象：pMainWidget
调用目标：OnSendProgressChanged
连接方式：AutoConnection
```

这些记录按发送对象及信号组织起来。一个信号可以对应多个连接，因此发出一次信号，可以触发多个槽。

**`connect()` 做的是登记，槽不会在连接时执行。**

**3. `emit` 实际上是在调用信号函数**

当你写：

```cpp
emit SignalSendProgress(10, 100);
```

`emit` 在通常配置下是一个空宏，主要让代码更易读。因此实际执行的是：

```cpp
SignalSendProgress(10, 100);
```

这个由 moc 生成的信号函数，会把参数交给：

```cpp
QMetaObject::activate(...);
```

Qt 随后查找该信号的连接列表，逐条决定怎样调用接收方。这个分发过程可以在 [qobject.cpp](</D:/Qt/5.14.2/Src/qtbase/src/corelib/kernel/qobject.cpp:3750>) 中看到。

**4. 直接连接：当前线程直接调用槽**

对于 `DirectConnection`，Qt 找到目标后，直接执行槽函数：

```text
调用信号函数
     ↓
遍历连接记录
     ↓
执行槽函数
     ↓
槽返回
     ↓
信号函数返回
```

因此槽执行期间，发出信号的代码要等待它返回。这条路径不需要把调用放进事件队列。

**5. 排队连接：把“调用槽”变成一个事件**

对于 `QueuedConnection`，Qt 会：

1. 创建 `QMetaCallEvent`。
2. 保存调用目标，并复制需要传递的参数。
3. 调用 `QCoreApplication::postEvent()`，将事件投递给接收对象。
4. 由接收对象所属线程的事件循环处理事件。
5. 在该线程中执行槽函数。

对应的 [queued_activate() 实现](</D:/Qt/5.14.2/Src/qtbase/src/corelib/kernel/qobject.cpp:3689>) 中，可以看到参数复制和事件投递。

你项目的跨线程进度通知就是：

```text
后台线程
  emit SignalSendProgress(10, 100)
             ↓
  创建事件，保存参数 10、100
             ↓
  投递到主线程的事件队列
             ↓
主线程事件循环取出事件
             ↓
  执行 OnSendProgressChanged(10, 100)
```

所以**跨线程通信的关键，是事件投递和接收线程的事件循环**。后台线程不必等待 UI 槽执行完毕，就可以继续工作。

即使信号参数写成：

```cpp
const QString &strMessage
```

普通排队连接仍会保存一份 `QString` 参数副本，供稍后使用。但如果参数是指针，复制的只是指针值，所指对象的生命周期仍需要你管理。

**6. 默认的 `AutoConnection` 怎样选择？**

Qt 在**每次发出信号时**比较：

```text
当前发出信号的线程
          与
接收对象所属的线程
```

- 相同：直接调用。
- 不同：排队调用。

这里比较的是实际执行 `emit` 的线程，不能只看发送对象的线程归属。

这些机制解释了你前面问的两个现象：主线程可以处理后台线程的信号；但如果主线程被阻塞，事件队列里的槽调用就暂时得不到执行。

## 信号转信号
可以，Qt 支持把一个信号连接到另一个信号，这通常用于转发通知。

你的代码：
connect(
    pWorker, &ReliableReceiverWorker::SignalLogMessage,
    this, &ReliableTransferManager::SignalLogMessage);
含义是：Worker 发出日志信号时，Manager 随之发出自己的日志信号，并传递相同的参数。

例如 Worker 执行：
emit SignalLogMessage(QStringLiteral("接收连接已断开。"));
消息就会沿着这条链传递：
Worker 的日志信号
    → Manager 的日志信号
        → 连接 Manager 日志信号的界面槽函数
这样，界面只需要连接 Manager，不必逐个连接动态创建的 Worker：
connect(
    pManager, &ReliableTransferManager::SignalLogMessage,
    this, &MainWidget::OnLogMessage);
而且，信号转发也遵循线程连接规则：这里 Worker 在接收线程，Manager 在主线程，默认的 Qt::AutoConnection 通常会采用队列方式，等主线程处理事件时再发出 Manager 的日志信号。

## “保护指针”的用法
`pGuard` 是一个**观察 `pThread` 是否还存在的指针**，变量名表示“保护指针”。

```cpp
const QPointer<QThread> pGuard(pThread);
```

拆开来看：

- `QPointer<QThread>`：指向 `QThread` 对象的 Qt 弱引用指针。
- `pGuard(pThread)`：让它观察 `pThread` 指向的那个对象。
- 当那个 `QThread` 对象被删除时，`pGuard` **自动变为空**。

普通指针不会这样：

```cpp
QThread *pThread = new QThread;

QPointer<QThread> pGuard(pThread);

delete pThread;

//pThread 仍保存原来的地址，已经是悬空指针。
//pGuard 已自动变为空。
```

所以后面的回调可以安全地判断：

```cpp
if (pGuard.isNull())
{
    return; //对象已经被其他清理流程删除了。
}
```

在你的代码中，`StopListening()` 可能已经删除了线程对象，而主线程稍后才处理排队的 `finished` 回调。`pGuard` 就用于让这个回调发现对象已经不存在，避免再次访问它。

注意：**它观察的是 `QThread` 对象是否被删除，不是后台线程是否停止。** 线程运行结束，但 `QThread` 对象还没删除时，`pGuard` 仍然非空。

这里的 `const` 只是限制你主动修改这个指针变量，不影响对象删除后 Qt 自动将它置空。

### 为啥不直接判断pThread呢？
因为 **`delete pThread` 不会自动把 `pThread` 变成 `nullptr`**。

例如：

```cpp
QThread *pThread = new QThread;

delete pThread;

if (pThread != nullptr)
{
    //仍然会进入！它还保存着原来的地址，
    //但该地址上的对象已经被删除了。
}
```

所以，判断普通指针非空，只能说明“保存的地址不是零”，**不能证明对象还活着**。

你可能会想到删除后手动置空：

```cpp
delete pThread;
pThread = nullptr;
```

但你的 lambda 捕获的是指针的**副本**：

```cpp
[this, pThread]()
{
    //这里保存的是另一个指针变量。
}
```

外面的指针被置空，不会改变 lambda 中保存的地址。

`QPointer` 则会跟踪 QObject 的销毁：

```cpp
[this, pGuard]()
{
    if (pGuard.isNull())
    {
        return;
    }
}
```

即使捕获的是 `QPointer` 的副本，它也能在目标对象被删除后自动变为空，因此适合这里延后执行的回调。

## 一条连接对应一个 Worker 和一个接收线程
Manager 所在线程
    ├─ ReliableTcpServer：接受连接
    └─ QThread 对象：管理后台线程

接收线程
    └─ ReliableReceiverWorker
        └─ QTcpSocket：在 AcceptConnection() 中创建
QThread 对象本身仍属于 Manager 所在线程；Worker 经过 moveToThread() 后，其线程归属才是接收线程。

线程名称中的编号只是连接编号，不是 laneIndex。具体属于哪个数据通道，要收到 Metadata 后才知道。
## 为什么用 lambda 调用 AcceptConnection()？
QThread::started 不携带连接描述符，所以通过：
[pWorker, nSocketDescriptor]()
保存 Worker 指针和描述符的副本。以 pWorker 作为连接的上下文对象，确保这里的接管操作在接收线程执行。

## 为什么分别清理 Worker 和 QThread
Worker 负责 socket 和会话关联，在线程结束时通过 deleteLater() 清理。

QThread 对象负责管理线程，需要回到 Manager 所在线程，从列表移除后再释放。两者是不同对象，各自有清理步骤。

## 分片报告的问题
**如果 A 自己接收了 100 个，B 自己接收了 101 个，那总数确实是 201 个。** 你这个理解没错。

我前面的表述容易让人误会。这里的区别是：**两个 Worker 报告的都是整个文件的总进度，而不是各自接收了多少。**

同一个文件的两个 Worker，共用同一个 Session：

```text
Worker A ─┐
          ├→ 同一个 Session → m_nReceivedPacketCount
Worker B ─┘                   整个文件已接收的分片数
```

举个具体例子：

| 时刻 | A 实际接收数量 | B 实际接收数量 | Session 中的总数 |
|---|---:|---:|---:|
| 最初 | 60 | 39 | 99 |
| A 又收到一个分片 | 61 | 39 | 100 |
| B 又收到一个分片 | 61 | 40 | 101 |

此时：

- A 发出进度通知：**“整个文件已经收到 100 个分片。”**
- B 发出进度通知：**“整个文件已经收到 101 个分片。”**

这是同一个总数在两个时刻的快照，所以不能相加。

如果 B 的通知先被主线程处理，A 的通知后被处理，就会出现：

```text
界面先显示：101
随后收到旧通知：100
```

因此 Manager 使用 `qMax()` 保留 `101`，避免进度倒退。

**真正的累计操作已经在 Session 接收新分片时完成了；Manager 只是转发累计结果，不再累加一次。**

这里最关键的是：Worker 报告的是整个共享会话的已接收数量，不是自己这个通道的数量，所以不能把不同 Worker 的数字相加。

例如两个接收线程先后取得了共享进度：
线程 A：已接收 100 个分片
线程 B：已接收 101 个分片
但它们发送通知的时间可能交错，主线程可能先处理 101，再处理 100。如果直接转发，界面进度就会倒退。因此用：
nLatestCompletedCount =
    qMax(nLatestCompletedCount, nCompletedPacketCount);
始终保留最大的完成数量。

而 m_setCompletedSessions 有两个用途：避免重复的完成请求让界面多次收到“完成”；忽略完成之后才到达的旧进度通知。

这两个 lambda 都以 this 为上下文，正常情况下会在 Manager 所在线程执行，因此这些进度记录也统一由 Manager 所在线程访问。

# 3. QSHaredPointer
`QSharedPointer<T>` 是 Qt 提供的**共享智能指针**：多个地方可以共同持有同一个对象，最后一个持有者释放它时，对象会自动销毁。

你可以先理解为：**帮你管理对象生命周期，避免到处手动判断什么时候 `delete`。**

**1．创建一个共享指针**

你目前的代码：

```cpp
QSharedPointer<QAtomicInt> m_pStopFlag;
```

这里只声明了指针，尚未创建 `QAtomicInt` 对象，默认是空的。

创建对象：

```cpp
m_pStopFlag = QSharedPointer<QAtomicInt>(
    new QAtomicInt(0));
```

也可以在定义时直接创建：

```cpp
QSharedPointer<QAtomicInt> pStopFlag(
    new QAtomicInt(0));
```

此时：

```text
pStopFlag ──→ 一个值为 0 的 QAtomicInt 对象
```

**2．复制指针，共享同一个对象**

```cpp
QSharedPointer<QAtomicInt> pAnotherFlag = pStopFlag;
```

这一步**没有复制 `QAtomicInt` 对象**，只是多了一个共同持有者：

```text
pStopFlag    ──┐
               ├──→ 同一个 QAtomicInt 对象
pAnotherFlag ──┘
```

通过任意一个指针修改，另一个都能访问到同一个对象：

```cpp
pAnotherFlag->storeRelease(1);

const int nValue = pStopFlag->loadAcquire();
//nValue 为 1，因为访问的是同一个原子整数。
```

`->` 的用法与普通指针一样：

```cpp
pStopFlag->storeRelease(1);
```

表示调用它所指对象的成员函数。

**3．它什么时候自动删除对象？**

靠的是**引用计数**，可以理解为“当前还有几个共享指针持有这个对象”。

```cpp
QSharedPointer<QAtomicInt> pFirst(new QAtomicInt(0));
//持有者数量：1

{
    QSharedPointer<QAtomicInt> pSecond = pFirst;
    //持有者数量：2

} //pSecond 离开作用域，持有者数量变回 1。
  //对象还在，因为 pFirst 仍然持有它。

pFirst.clear();
//最后一个持有者释放对象，自动删除 QAtomicInt。
//pFirst 自身变为空指针。
```

所以，**一个共享指针销毁，不代表对象马上销毁；最后一个共享指针释放时才销毁。**

常见操作：

| 写法 | 作用 |
|---|---|
| `pPointer->SomeFunction()` | 调用所指对象的方法 |
| `pPointer.isNull()` | 判断是否为空 |
| `pPointer.clear()` | 放弃自己对对象的持有 |
| `pPointer.data()` | 取得普通指针；不会转移所有权 |

**4．为什么我们的 Store 和 Session 要用它？**

因为停止标记需要被多个对象共同持有：

```text
Store.m_pStopFlag     ──┐
Session A.m_pStopFlag ──┼──→ 同一个停止标记
Session B.m_pStopFlag ──┘
```

构造 Session 时：

```cpp
ReliableReceiveSession::ReliableReceiveSession(
    const SReliableFileMetadata &stMetadata,
    const QString &strOutputDirectory,
    const QSharedPointer<QAtomicInt> &pStopFlag)
    : m_pStopFlag(pStopFlag)
{
    //……
}
```

关键就是：

```cpp
m_pStopFlag(pStopFlag)
```

它复制共享指针，让这个 Session 也成为停止标记的持有者。

即使 Store 先释放了自己的那份指针，只要 Session 仍然持有，停止标记就不会提前销毁。

同理：

```cpp
QSharedPointer<ReliableReceiveSession> m_pSession;
```

让多个连接共同持有同一个文件会话。某个连接断开并释放指针，其他连接仍然可以继续使用这个 Session。

**最后记住两个注意点：**

- 对象交给 `QSharedPointer` 管理后，不要再手动 `delete pPointer.data()`。
- 共享的是生命周期，**不会自动保护对象内部的数据**。Session 的位图和计数仍然需要互斥锁；停止标记能安全跨线程读写，是因为它本身是 `QAtomicInt`。

# 4. expilict修饰词的作用

`explicit` 用来**阻止构造函数被用于隐式类型转换**，要求你明确地构造对象。

例如：

```cpp
class Number
{
public:
    Number(int nValue)
    {
    }
};
```

没有 `explicit` 时，这样也能写：

```cpp
Number oNumber = 10;
```

编译器会通过 `Number(int)`，把整数 `10` 隐式转换成一个 `Number` 对象。

加上后：

```cpp
explicit Number(int nValue)
{
}
```

就必须明确构造：

```cpp
Number oNumber(10);    //可以
Number oNumber{10};    //可以

Number oNumber = 10;   //报错，不允许隐式转换
```

你现在的代码：

```cpp
explicit ReliableTcpServer(QObject *pParent = nullptr);
```

表示：**不能把一个 `QObject*` 隐式转换成 `ReliableTcpServer` 对象。** 正常创建对象不受影响：

```cpp
ReliableTcpServer oServer;       //可以，使用默认参数 nullptr
ReliableTcpServer oServer(this); //可以，明确传入父对象

auto pServer = new ReliableTcpServer(this); //也可以
```

所以这里加 `explicit`，主要是在表达接口意图：**传入父对象指针是在创建服务器对象，不应该被当成普通的自动类型转换。**

