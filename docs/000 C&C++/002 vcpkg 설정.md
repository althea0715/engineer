# vcpkg 설정 및 사용 사유

기본적으로 C/C++을 개발함에 있어서 google에서 사용한다는 라이브러리들을 적용하려다가 결국 실패해서 vcpkg를 만져보게 되었습니다.

1. googletest
2. abseil
3. protobuf

- 1번은 쉽게 CMAKE + MVSC 환경에서 쉽게 Build가 가능합니다.
- 2번은 ...너무 어렵습니다. 잘 안됩니다. 일단 어느 홈페이지도 믿을 수 없습니다.
- 3번은 build 되어있는 압축 파일을 다운로드 받는 것이 신상에 이롭습니다. (잘 build 되지 않음. 종속성 맞추기 힘듬)

그래서 원래 선호하지 않았지만 vcpkg를 사용해보니 위 3개의 라이브러를 쉽게 설치할 수 있는 것으로 보였습니다. 또한 CMAKE 적용해도 용이하니 해당 내용을 정리합니다.

## 2. vcpkg 다운로드

직접 다운로드 받거나 git clone을 활용하여 다운로드 받도록 합니다. git clone을 통하여 다운로드 받는 것이 아니면 향후 git pull 같은 명령어로 업데이트를 할 수가 없습니다.

Github : https://github.com/Microsoft/vcpkg

단, 한국어 설명어 페이지가 있습니다. 반드시 참조하도록 합니다.

한국어 Manual : https://github.com/microsoft/vcpkg/blob/master/README_ko_KR.md

## 3. Build

.\vcpkg\bootstrap-vcpkg.bat

명령어 치시면 설치가 진행됩니다. 다만 편의를 위해 환경 변수를  설치가 된 폴더(vcpkg.exe 파일이 있는 경로) 등록해줍니다.

## 4. x64-windows vs x64-windows-static

C/C++ Build시 MD, MT를 구분하여 Build 해야합니다. 그래야 종속성이 깨지지 않습니다.

- /MD (Multi-Threaded DLL) : 동적(Dynamic)으로 연결되며 바이너리 파일 배포시 dll 파일을 같이 첨부해야합니다. 
- /MT (Multi-Threaded) : 정적(Static)으로 연결되며 바이너리 파일만 배포하면 됩니다. 단, 용량이 큽니다.

vcpkg에서 설치할 때는 아래와 같이 적용하면 됩니다.

- x64-windows : MD build 지원
- x64-windows-static : MT build 지원

예를 들어 googletest를 설치하겠다 하면 다음과 같이 입력하면 됩니다.

```shell
vcpkg install gtest:x64-windows
```

뒤에 `x64-windows`가 없으면 자동으로 설치될 것이므로 편의상 한개로 죽 밀고 나가는 것이 좋습니다. 여기서 저는 MD를 밀기로 하였으므로 MD로 진행하겠습니다.

## 5. vcpkg + MSVC 연동

`vcpkg integrate install` 명령어를 기입하면 MSVC와 연동된다는데 효용 가치는 아직 잘 모르겠으나 아래와 같은 정보를 출력해줍니다.

```
Applied user-wide integration for this vcpkg root.
CMake projects should use: "-DCMAKE_TOOLCHAIN_FILE=C:/c_library/vcpkg/scripts/buildsystems/vcpkg.cmake"

All MSBuild C++ projects can now #include any installed libraries. Linking will be handled automatically. Installing new libraries will make them instantly available.
```

## 6. find_package 그리고 CMAKE 예제

vcpkg를 사용하면 cmake에 아래와 같은 명령어를 가급적 상단에 기입했을 때 find_package 기능을 사용할 수 있습니다.

```cmake
# 저는 x64-windows를 기본적으로 사용합니다.
set(VCPKG_TARGET_TRIPLET x64-windows)

# 제 vcpkg.cmake 경로는 다음과 같습니다.
include(C:/c_library/vcpkg/scripts/buildsystems/vcpkg.cmake)
```


지금까지 언급했던 내용들을 모두 종합하여 CMakeLists.txt을 다음과 같이 작성할 수 있습니다.

```cmake
cmake_minimum_required(VERSION 3.0.0)
project(engineer_tool VERSION 0.1.0)

# 저의 Compiler Version은 19.34.31937로 C++20 대응합니다.
# 좀 더 있어보이는 설정법으로 변경하였습니다.
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# VSCODE의 기본 문서 인코딩은 utf-8입니다.
add_compile_options("/utf-8")

# vcpkg 설정을 합니다.
set(VCPKG_TARGET_TRIPLET x64-windows)
include(C:/c_library/vcpkg/scripts/buildsystems/vcpkg.cmake)

# 테스트 설정, CTest는 대부분의 Test를 지원합니다.
include(CTest)
enable_testing()

add_executable(
    engineer_tool 
    main.cpp
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```
