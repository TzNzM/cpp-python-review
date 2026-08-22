#include<iostream>

// 错误的写法
// void move_zeros(int* values, int n){
//     int count = 0; 
//     for (int i = 0; i < n; i++)
//      {
//         if (values[i] == 0 && count == 0)
//         {
//             ++count;
//         }
//         if (values[i] == 0 && i+count < n && values[i+count] != 0)
//         {
//             std::swap(values[i],values[i+count]);
//         }
//         if (values[i] == 0 && i+count < n && values[i+count] == 0)
//         { 
//             ++count;
//             std::swap(values[i],values[i+count]);
//         } 
//      }
     
// }

#include <utility>

//双指针
void move_zeros(int* values, int n) {
    if (values == nullptr || n <= 0) {
        return;
    }

    int write = 0;
    for (int read = 0; read < n; read++)
    {
        if (values[read] != 0)
        {
            if (read != write)
            {
                std::swap(values[read],values[write]);
            }
            write++;          
        }
        
    }
    
}

int main(){
    // int value[] = {0,1,0,3,12};
    // int n = 5;
    // int value[] = {0,1,0,3,12,0,7,8};
    // int n = 8;
    int value[] = {0,0,1};
    int n = 3;
    move_zeros(value,n);
    for (int i = 0; i < n; i++)
    {
        std::cout << value[i] << std::endl;
    }
}