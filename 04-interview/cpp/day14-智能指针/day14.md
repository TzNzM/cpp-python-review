1.unique_ptr、shared_ptr、weak_ptr 分别表达什么所有权关系？
unique_ptr 是独占管理的
shared_ptr 是共享管理的
weak_ptr 是观察这个共享管理的ptr，但是他并不真正拥有，他需要判断后调用
2.为什么 unique_ptr 不能复制，但可以移动？std::move 后原指针状态如何？
unique_ptr 是独占管理的，所以不能复制，但是可以移动，用另一个指针来管理他。std::move后，原指针指向空
3.shared_ptr::use_count() 统计什么？weak_ptr 会增加它吗？
shared_ptr::use_count() 统计当前有多少个shared指针指向它，weak_ptr不会增加它
4.为什么不能直接解引用 weak_ptr？lock() 的作用是什么？
weak_ptr 不拥有对象，对象可能已销毁，因此不能直接解引用；lock() 尝试获取一个 shared_ptr，对象仍存活则成功，否则得到空 shared_ptr。
5.两个对象互相持有 shared_ptr 会发生什么问题？应如何用 weak_ptr 解决？
两个对象互相持有 shared_ptr 会形成循环引用。即使外部所有者都释放了，两个对象的引用计数仍互相保持为非零，析构函数不会执行，造成内存泄漏。应将其中不承担所有权的一端改为 weak_ptr。