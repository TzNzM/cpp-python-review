class Rectangle {
private:
    int m_nwidth;
    int m_nheight;

public:
    Rectangle(int width, int height);

    int area() const;
    int perimeter() const;

    bool resize(int width, int height);
};