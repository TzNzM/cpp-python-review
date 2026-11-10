# CMake 使用指南：从第一个项目到现代 CMake

> 面向已经会写基础 C++、但还不熟悉项目构建的学习者。示例以 C++17 和 CMake 3.20 作为最低版本，命令兼顾 Windows PowerShell 与常见类 Unix shell。CMake 版本和生成器会影响少数细节；遇到版本差异时，以项目要求和对应版本的官方文档为准。

## 1. CMake 解决什么问题

编译器负责把源文件编译、链接成程序，构建工具负责决定哪些命令要执行、执行顺序以及哪些文件需要重建。项目一旦包含多个 `.cpp`、头文件、库、编译选项和平台差异，手工维护编译命令就容易出错。

CMake 是构建系统生成器：开发者用 `CMakeLists.txt` 描述项目、目标及其关系，CMake 配置项目并生成适合本机的构建文件，再由 Ninja、Make 或 Visual Studio 等构建工具实际构建。

典型流程可以记成：

```text
CMakeLists.txt + 源码 + 编译器/依赖
              │ cmake -S . -B build
              ▼
     配置并生成构建系统（build/）
              │ cmake --build build
              ▼
          可执行文件/库
```

这里最重要的区别是：`cmake` 通常负责配置和生成；`cmake --build` 才调用底层构建工具来编译、链接。

## 2. 安装与确认工具链

需要准备 CMake、C++ 编译器和对应的构建工具。Windows 可以使用 Visual Studio 的 C++ 桌面开发组件；也可以单独安装 Ninja 和 GCC/Clang 等工具链。CMake 找得到不代表编译器也可用，特别是在 Windows 上，Visual Studio 的命令行环境会提供必要的编译器路径和环境变量。

```powershell
cmake --version
cmake --help
```

`cmake --help` 可以查看当前机器可用的生成器。生成器（Generator）是 CMake 输出的构建系统类型，例如 Ninja、Unix Makefiles 或 Visual Studio。某些生成器是单配置（如 Ninja），构建类型通常在配置时通过 `-DCMAKE_BUILD_TYPE=Debug` 指定；Visual Studio 等多配置生成器会在构建时通过 `--config Debug` 选择配置。

## 3. 第一个可运行项目

创建如下目录：

```text
hello-cmake/
├── CMakeLists.txt
└── main.cpp
```

`main.cpp`：

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, CMake!\n";
    return 0;
}
```

根目录 `CMakeLists.txt`：

```cmake
cmake_minimum_required(VERSION 3.20)
project(HelloCMake VERSION 1.0 LANGUAGES CXX)

add_executable(hello main.cpp)
target_compile_features(hello PRIVATE cxx_std_17)
```

逐行理解：

- `cmake_minimum_required()` 声明项目最低支持的 CMake 版本，同时设定相应的策略兼容行为。项目使用的命令或功能必须在这个版本中存在。
- `project()` 声明项目名称、版本和使用的语言。这里明确启用 C++。
- `add_executable()` 创建一个名为 `hello` 的可执行目标，并把 `main.cpp` 作为源文件。
- `target_compile_features()` 为这个目标声明需要 C++17。`PRIVATE` 表示这个要求只用于构建 `hello` 本身，不传播给依赖它的其他目标。

在项目根目录运行：

```sh
cmake -S . -B build
cmake --build build
```

`-S` 指定源码目录（Source），`-B` 指定构建目录（Build）。建议使用独立构建目录，不要把生成的缓存和中间文件写进源码目录。之后修改 CMake 文件，通常重新执行 `cmake -S . -B build` 进行重新配置，再构建。

运行程序：

```sh
# Linux/macOS 常见路径
./build/hello

# Windows PowerShell，使用 Ninja 等单配置生成器时常见路径
.\build\hello.exe

# Visual Studio 多配置生成器通常会把程序放在配置子目录
.\build\Debug\hello.exe
```

## 4. CMake 的核心模型：目标及其关系

现代 CMake 以 target（目标）为中心。目标可以是可执行文件、库或辅助任务。尽量把源文件、头文件目录、编译特性、宏定义、编译选项和链接依赖写到具体目标上，让 CMake 根据目标之间的关系传播所需配置。

常用目标命令：

| 命令 | 用途 |
| --- | --- |
| `add_executable(name ...)` | 创建可执行程序 |
| `add_library(name ...)` | 创建库；默认类型会受 `BUILD_SHARED_LIBS` 影响 |
| `target_sources(target ...)` | 为已有目标添加源文件 |
| `target_include_directories(target ...)` | 设置目标自身或使用者需要的头文件搜索目录 |
| `target_link_libraries(target ...)` | 声明目标之间的链接依赖 |
| `target_compile_definitions(target ...)` | 添加预处理宏定义 |
| `target_compile_options(target ...)` | 添加编译器选项 |
| `target_compile_features(target ...)` | 声明 C++ 等语言特性需求 |

### 4.1 PRIVATE、PUBLIC、INTERFACE

这些关键字控制配置作用于谁：

- `PRIVATE`：只应用于当前目标。
- `PUBLIC`：应用于当前目标，也传播给链接它的目标。
- `INTERFACE`：只传播给使用当前目标的其他目标，当前目标自身不使用。

例如，库的 `.cpp` 使用某个内部头文件目录，而库公开的头文件又需要依赖方能包含 `include/`：

```cmake
target_include_directories(mylib
    PRIVATE
        "${CMAKE_CURRENT_SOURCE_DIR}/src"
    PUBLIC
        "${CMAKE_CURRENT_SOURCE_DIR}/include"
)
```

如果一个公开头文件里包含了第三方库的头文件，那么这个第三方 include 需求也需要传递给使用者，通常使用 `PUBLIC` 或 `INTERFACE`。如果第三方库只在 `mylib` 的 `.cpp` 里用，则是 `PRIVATE`。

### 4.2 一个小型库项目

目录结构：

```text
sample/
├── CMakeLists.txt
├── include/
│   └── geometry/area.h
├── src/
│   ├── area.cpp
│   └── main.cpp
```

根目录 `CMakeLists.txt`：

```cmake
cmake_minimum_required(VERSION 3.20)
project(GeometryDemo VERSION 1.0 LANGUAGES CXX)

add_library(geometry src/area.cpp)
target_include_directories(geometry PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
)
target_compile_features(geometry PUBLIC cxx_std_17)

add_executable(geometry_demo src/main.cpp)
target_link_libraries(geometry_demo PRIVATE geometry)
```

这里 `geometry_demo` 链接 `geometry`，因此它能使用 `geometry` 公开的头文件路径和 C++ 特性要求。头文件目录和语言要求沿目标依赖关系传递，不需要再对每个调用者重复配置。

`$<BUILD_INTERFACE:...>` 是生成器表达式：当目标在当前源码构建树中被使用时提供该路径。要把库安装后提供给其他项目使用，还需要正确配置安装树接口；相关 `$<INSTALL_INTERFACE:...>` 和 `install(EXPORT ...)` 见“安装与包”一节。

## 5. 变量、选项与缓存

CMake 变量用于组织配置值：

```cmake
set(APP_SOURCES src/main.cpp src/util.cpp)
add_executable(my_app ${APP_SOURCES})
```

`option()` 创建一个可由用户设置的布尔开关，常用于构建功能选择：

```cmake
option(BUILD_TESTING "Build tests" ON)

if(BUILD_TESTING)
    enable_testing()
    # 添加测试目标
endif()
```

配置时可用 `-D` 设置缓存变量：

```sh
cmake -S . -B build -DBUILD_TESTING=OFF
```

缓存保存在 `build/CMakeCache.txt`。同一个构建目录通常固定对应一个生成器和一套工具链；切换编译器或生成器时，建议新建构建目录，或者清除旧构建目录后重新配置。常用诊断命令：

```sh
cmake -LA -N build      # 查看缓存变量
cmake --fresh -S . -B build  # 支持该选项的 CMake 版本可用它重新配置缓存
```

清除构建产物最简单的方式是删除整个构建目录，再重新配置。请确认路径确实是生成目录后再删除。

## 6. 选择生成器与构建配置

通常 CMake 会选择平台默认生成器。想明确指定时，在首次配置中使用 `-G`：

```sh
cmake -S . -B build-ninja -G Ninja
```

如果已经使用 Visual Studio，也可以指定相应的 Visual Studio 生成器（名称以 `cmake --help` 显示为准）。配置完成后不要在同一个 `build` 目录里换生成器。

单配置生成器（如 Ninja、Unix Makefiles）：

```sh
cmake -S . -B build-debug -DCMAKE_BUILD_TYPE=Debug
cmake --build build-debug
```

多配置生成器（如 Visual Studio）：

```powershell
cmake -S . -B build-vs -G "Visual Studio 17 2022"
cmake --build build-vs --config Debug
```

`Debug` 常包含调试信息，通常关闭较激进的优化；`Release` 通常启用优化。多配置生成器是在 build 阶段通过 `--config` 选配置；单配置生成器是在 configure 阶段通过 `CMAKE_BUILD_TYPE` 选配置。

## 7. 连接第三方依赖

### 7.1 find_package

如果依赖已经安装并提供 CMake package config，优先使用 `find_package()`，并链接其导出的目标：

```cmake
find_package(fmt CONFIG REQUIRED)

add_executable(my_app src/main.cpp)
target_link_libraries(my_app PRIVATE fmt::fmt)
```

`REQUIRED` 表示找不到依赖就配置失败；`fmt::fmt` 是带命名空间的导入目标。它通常会携带依赖的 include 路径、编译定义和链接信息。具体包名和目标名由依赖项目决定，应查该库自己的文档。

### 7.2 FetchContent

源码项目也可以用 `FetchContent` 在配置时获取。网络访问、版本和项目策略要纳入考虑；固定 tag 或 commit 比跟踪浮动分支更可复现。

```cmake
include(FetchContent)

FetchContent_Declare(
    fmt
    GIT_REPOSITORY https://github.com/fmtlib/fmt.git
    GIT_TAG        10.2.1
)
FetchContent_MakeAvailable(fmt)

target_link_libraries(my_app PRIVATE fmt::fmt)
```

大型项目也可能使用系统包管理器、子模块、预装 SDK 或工具链文件。不要把某个人电脑上的绝对 include 路径写进共享项目配置。

## 8. 添加测试

CMake 通过 CTest 运行测试。可以把测试程序本身建成 target，再用 `add_test()` 注册：

```cmake
include(CTest)

if(BUILD_TESTING)
    add_executable(area_test tests/area_test.cpp)
    target_link_libraries(area_test PRIVATE geometry)
    add_test(NAME area_test COMMAND area_test)
endif()
```

构建并运行测试：

```sh
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

Visual Studio 这类多配置生成器下，先 `cmake --build build --config Debug`，测试可通过 `ctest --test-dir build -C Debug --output-on-failure` 运行。

## 9. 安装与包的基础概念

库作者可以安装库文件和头文件，并导出 CMake target，让下游项目通过 `find_package()` 使用。安装规则示意：

```cmake
include(GNUInstallDirs)

install(TARGETS geometry
    EXPORT GeometryTargets
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
)
install(DIRECTORY include/ DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}")
install(EXPORT GeometryTargets
    NAMESPACE Geometry::
    DESTINATION "${CMAKE_INSTALL_LIBDIR}/cmake/Geometry"
)
```

真实可复用包还需要生成并安装 `GeometryConfig.cmake`（以及版本文件），并区分源码树与安装树的头文件路径，例如：

```cmake
target_include_directories(geometry PUBLIC
    "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
    "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>"
)
```

不要把开发机器的绝对路径写进安装接口，否则移动安装目录后包会失效。入门阶段理解 `install()` 的作用即可；完整包配置可参考官方 `cmake-packages(7)` 手册。

## 10. 常见问题与排查

| 现象 | 常见原因 | 检查方向 |
| --- | --- | --- |
| `CMakeLists.txt` 找不到 | `-S` 指向了错误目录，或文件名大小写/拼写错误 | 检查当前目录、源码路径和根目录文件名 |
| 找不到 C++ 编译器 | 编译器未安装，或编译器环境没有初始化 | `cmake --help`、`cmake --version`，并检查 `CXX`/Visual Studio 开发环境 |
| `Could not create named generator` | `-G` 的生成器名当前不可用或拼错 | 运行 `cmake --help` 查看本机支持列表 |
| 生成器不匹配或编译器改变后异常 | 复用了旧缓存目录 | 新建 `build` 目录，或清空旧构建目录再配置 |
| 找不到头文件 | include 路径未加到提供该头文件的 target，或传播范围设错 | 检查 `target_include_directories()` 与 `PRIVATE` / `PUBLIC` / `INTERFACE` |
| 链接时 unresolved external / undefined reference | 源文件未加入目标、实现所在库未链接，或声明与定义不一致 | 检查 `target_sources()`、`add_library()`、`target_link_libraries()` 和函数签名 |
| `find_package` 找不到库 | 依赖未安装、包配置不在搜索路径、包或目标名用错 | 查依赖官方安装说明；必要时设置包管理器或 toolchain 提供的搜索路径 |
| Windows 找不到 `cl.exe` | 从普通终端启动，VS 编译环境未准备好 | 在 Developer PowerShell / Developer Command Prompt 里运行 CMake |
| 修改 CMake 后结果没有变化 | 实际构建了另一个 build 目录，或改错源码树 | 对照 `-S`、`-B` 路径；查看 `CMakeCache.txt` 中的 `CMAKE_HOME_DIRECTORY` |

建议排查顺序：先看配置阶段的第一条错误，再确认目标和路径；之后用 `cmake --build build --verbose`（多配置时补 `--config Debug`）查看实际编译、链接命令。不要一开始就用全局路径或全局编译选项掩盖目标关系问题。

## 11. 新手常见写法误区

1. **把所有配置都设成全局的。** 优先使用 `target_*` 命令，配置应属于具体目标。
2. **混淆 include 路径和链接依赖。** include 路径解决预处理器找头文件；链接库解决符号和二进制依赖。两者作用不同。
3. **用 `link_directories()`、`include_directories()` 管整个工程。** 新代码通常把依赖写到目标上：`target_link_libraries()` 和 `target_include_directories()`。
4. **误用 `PRIVATE` / `PUBLIC` / `INTERFACE`。** 判断标准是：依赖该目标的代码是否也必须看到这项设置？
5. **以为 `cmake --build` 会自动修复所有配置问题。** 新的依赖选项、编译器和生成器通常需要重新配置；CMake 会在源码或配置变化时自动重新生成，但仍应确认用了正确构建目录。
6. **在源码目录里直接运行 `cmake .`。** 这会形成 in-source build，容易污染源码，也不利于切换配置。
7. **硬编码操作系统专属路径或编译器参数。** 优先使用 CMake 提供的目标属性、平台信息、导入目标和标准目录变量。

## 12. 建议的学习练习

按顺序完成，每题都先自己改 `CMakeLists.txt`，再配置、构建并观察结果：

1. 把第一个程序拆成 `main.cpp` 和 `math.cpp`，让 `math.cpp` 提供一个函数。
2. 把 `math.cpp` 独立构建成 `math` 库，让可执行程序通过 `target_link_libraries()` 使用它。
3. 把公开头文件放入 `include/`，比较 `PRIVATE`、`PUBLIC` 和 `INTERFACE` 的效果。
4. 添加一个 `BUILD_TESTING` 选项和一个 CTest 测试。
5. 用 Ninja 或 Visual Studio 分别配置构建；说明单配置与多配置的差别。
6. （进阶）安装库并导出 target，让另一个小项目通过 `find_package()` 使用它。

每一步复盘四件事：创建了哪些 target？目标之间有什么依赖？哪些设置会传播？CMake 配置生成后，实际执行了什么编译和链接命令？

## 13. 记忆框架

```text
描述项目：project / add_executable / add_library
配置目标：target_sources / target_include_directories / target_compile_features
连接依赖：target_link_libraries
分目录组织：add_subdirectory
获取依赖：find_package / FetchContent
测试：include(CTest) / add_test / ctest
流程：cmake -S 源码目录 -B 构建目录 -> cmake --build 构建目录
```

优先掌握“目标和依赖关系”的思路，再逐步学习安装导出、工具链文件、交叉编译、生成器表达式和自定义命令。

## 官方资料

- [CMake 官方教程](https://cmake.org/cmake/help/latest/guide/tutorial/index.html)：循序渐进的完整项目示例，覆盖库、测试、依赖等主题。
- [CMake 官方命令参考](https://cmake.org/cmake/help/latest/manual/cmake-commands.7.html)：查询命令语法和参数。
- [CMake 构建系统手册](https://cmake.org/cmake/help/latest/manual/cmake-buildsystem.7.html)：理解目标、依赖与 usage requirements。
- [CMake 生成器手册](https://cmake.org/cmake/help/latest/manual/cmake-generators.7.html)：查看生成器类型和平台支持。
- [CMake 包手册](https://cmake.org/cmake/help/latest/manual/cmake-packages.7.html)：学习安装、导出和 `find_package()` 的包配置。
- [CMake 生成器表达式手册](https://cmake.org/cmake/help/latest/manual/cmake-generator-expressions.7.html)：进阶条件配置语法 `$<...>`。
