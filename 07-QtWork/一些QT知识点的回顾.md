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