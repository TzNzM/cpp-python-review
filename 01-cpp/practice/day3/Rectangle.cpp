#include"Rectangle.h"



Rectangle::Rectangle(int width, int height)
    : m_nwidth(width), m_nheight(height) {//初始化列表
}

int Rectangle::area() const{
    return m_nheight * m_nwidth;
}

int Rectangle::perimeter() const{
    return 2 * (m_nheight + m_nwidth);
}

bool Rectangle::resize(int width, int height){
    if (width <= 0 || height <= 0)
    {
        return false;
    }else{
        m_nwidth = width;        
        m_nheight = height;
        return true;
    }
    
}


