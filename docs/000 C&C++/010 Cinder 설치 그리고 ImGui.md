# Cinder 설치 그리고 ImGui

이 라이브러리는 이름만 알고 있었는데, OpenGL로 여러가지 그림을 그릴 수 있는 라이브러리인 것을 알게 되어 설치를 해보았습니다. 이 라이브러리에는 ImGui가 내장되어 있으며 그에 따라 이전에 작성했던 내용을 그대로 적용할 수 있기에 해당 라이브러리를 적극 공부하여 프로그램을 만들어보는 것으로 방향을 정했습니다.

또한, 이 라이브러리는 drawVector 함수를 통해 vector를 그리는 것을 지원하므로 제가 원하는 것에 거의 근접합니다. 

## 1. 설치 방법

이 라이브러리는 vcpkg를 지원하지 않으므로, 직접 설치해야합니다. 또한 반드시 --recursive 명령을 통해 다른 종속성 라이브러리도 다운로드 받도록 합니다. 이 라이브러리는 종속성이 너무 많아서 vcpkg에서 지원하지 않는 것 같으며, ImGui를 Docking 버젼으로 치환은 좀 어려운 것 같습니다.

`git clone --recursive https://github.com/cinder/Cinder.git`

vcpkg의 x64-windows 명령을 통해서 쉽게 MD 버젼의 build를 진행했다면, 이 라이브러리는 상당히 번거롭습니다. cmake tool을 활용하여 일단 configure를 만들어줍니다. (보통 build 폴더에 *.sln 파일이 만들어집니다.) 저는 MSVC를 사용하므로 visual studio 2022을 실행하여 build 옵션을 조정해 줄겁니다.

cinder solution의 property에서

1. Advancded - Preferred Build Toll Architecture
    - 64-bit 으로 변경
2. Advancded - Charactor Set
    - Use Multi-Byte Charactor Set 으로 변경
3. C/C++ - Code Generation - Runtime Library
    - /MDd 혹은 /MD 으로 변경

일단 이렇게 3개를 변경하겠습니다.

## 2. visual studio 2022를 활용하여 개발하기

Cinder 폴더에 들어가면 tools란 폴더에 TinderBox라는 것이 있습니다.

저의 경로는 다음과 같습니다. `C:\c_library\Cinder\tools\TinderBox-Win`

저 경로의 TinderBox.exe를 실행하여 적당히 선택하시여 넘어가면 자동으로 프로젝트 파일을 만들어 줍니다. 이것을 이대로 사용하면 됩니다.

당연하게도 Runtime Library를 재설정해줘야합니다. 여기서는 /MDd 혹은 /MD로 하시면 되겠습니다.


## 3. visual studio code를 활용하여 개발하기

모든 삽질의 시작입니다. 혹여라도 저와 같은 환경에서 개발하시는 분은 삽질은 안했으면 하는 바람입니다.

평범하게 CMake:Quick Start로 프로젝트를 만들었다고 가정하겠습니다. 당연히 필요한 것은 include 폴더와 lib 파일인데, lib 파일은 제 기준에 아래와 같은 경로에 있습니다.

`C:\c_library\Cinder\lib\msw\x64\Debug\v143\cinder.lib`

저 경로로 가는 길에 만나는 몇개의 dll과 lib파일은 무시해도 됩니다. 또한 OpenGL, GLFW, GLAD를 활용하는 라이브러리 답게 모든 것은 이미 포함되어 있으니 다른건 다 잊어도 됩니다. 모두 포함되어 있다는 점이 매력이 있어 이 라이브러리를 사용하겠다고 마음 먹게 되었습니다.

단! 반드시 zlib를 cmakelists.txt에 포함하여야합니다. 해당 라이브러리 종속성을 한꺼번에 해결하지 못했습니다. protobuf니 등등 vcpkg로 라이브러리 설치했을때 자연스래 설치가 되어있는 것이니 그냥 가져다 사용하도록 하겠습니다. 이를 정리하여 cmakelists.txt 파일을 만들면 다음과 같습니다.

```cmake
# CMakelists 중간 정리 참조

cmake_minimum_required(VERSION 3.0.0)
project(cinder_project VERSION 0.1.0)

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

# zlib 설정
find_package(ZLIB REQUIRED)

# Cinder 설정
set(CINDER C:/c_library/Cinder)

# Cinder에서 OpenGL 사용시 terminal을 사용안하기 때문에 WIN32 키워드가 필요합니다.
add_executable(
    cinder_project WIN32
    main.cpp
)

target_include_directories(
    cinder_project PRIVATE
    ${CINDER}/include
)

target_link_libraries(
    cinder_project PRIVATE
    ZLIB::ZLIB
    ${CINDER}/lib/msw/x64/Debug/v143/cinder.lib
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```

## 4. ImGui

ImGui가 편입됬기 때문에 간단한 cpp 예시 하나 작성하겠습니다. 기존의 ImGui를 사용하셧던 분이라면 앞단의 귀찮은 선언부분이 싹다 날아간것을 확인하실 수 있으십니다. 그렇지만 기존 방식대로 UI를 구성할 수 있습니다.


```cpp
#include "cinder/app/App.h"
#include "cinder/app/RendererGl.h"
#include "cinder/gl/gl.h"

// ImGui 사용하기 위해 선언
#include "cinder/CinderImGui.h"

using namespace ci;
using namespace ci::app;
using namespace std;

class CinderProjectApp : public App {
   public:
    void setup() override;
    void mouseDown(MouseEvent event) override;
    void update() override;
    void draw() override;
};

void CinderProjectApp::setup() {
    // 이렇게만 선언하면 귀찮은 선언부분을 한꺼번에 해결해줍니다.
    ImGui::Initialize();

    // 한글 적용
    ImGuiIO& io = ImGui::GetIO();
    io.Fonts->AddFontFromFileTTF("C://windows/Fonts/malgun.ttf", 18.0f, NULL, io.Fonts->GetGlyphRangesKorean());
}

void CinderProjectApp::mouseDown(MouseEvent event) {}

void CinderProjectApp::update() {}

void CinderProjectApp::draw() {

    // 임의의 예시 이미지
    gl::clear();
    vec2 center = getWindowCenter();
    float r = 100;

    gl::color(Color(1, 0, 0));  // red
    gl::drawSolidCircle(center + vec2(-r, r), r);
    gl::color(Color(0, 1, 0));  // green
    gl::drawSolidCircle(center + vec2(r, r), r);
    gl::color(Color(0, 0, 1));  // blue
    gl::drawSolidCircle(center + vec2(0, -0.73 * r), r);

    // 기존 방식 그대로
    ImGui::Begin("연습!");
    ImGui::End();
}

CINDER_APP(CinderProjectApp, RendererGl)
```