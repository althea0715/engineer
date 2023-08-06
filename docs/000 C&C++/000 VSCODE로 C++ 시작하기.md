# VSCODE로 C++ 시작하기

기본적으로 C/C++, Python, Rust는 어느정도 다를 수 있다는 전제조건으로 작성된 문서입니다. 또한 VSCODE도 어느정도 사용하실 수 있는 전제로 이 문서를 작성합니다.

빈 폴더를 VSCODE로 열어 CMake: Quick Start를 하면 다음과 같은 `CMakeLists.txt` 파일이 만들어집니다.

```cmake
cmake_minimum_required(VERSION 3.0.0)
project(engineer_tool VERSION 0.1.0)

# 저의 Compiler Version은 19.34.31937로 C++20 대응합니다.
# VSCODE의 기본 문서 인코딩은 utf-8입니다.
add_compile_options("/std:c++latest")
add_compile_options("/utf-8")

include(CTest)
enable_testing()

add_executable(engineer_tool main.cpp)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```

MSVC + VSCODE + CMake 조합으로 개발하면 여러가지 면으로 불편한 점이 많은데 이를 극복해가는 과정이라고 보셔도 되겠습니다. 

저는 향후 설치할 모든 라이브러리는 편의상 기본적으로 `C:/c_library` 폴더에 저장하겠습니다. 또한 가급적 다른 프로그램을 설치하게 되더라도 `C`드라이브에 설치합니다.