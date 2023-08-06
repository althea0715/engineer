# ImGui With OpenGL

## 1. OpenGL 적용

Reference

- 영문판 : https://learnopengl.com/
- 한글판 : https://heinleinsgame.tistory.com/3

### 1. GLFW 설치

설치 경로 : https://www.glfw.org/download.html

Windows pre-compiled binaries에서 windows 64bit를 다운로드 받습니다.

### 2. GLAD 설치

설치 경로 : https://glad.dav1d.de/

Language : C/C++
Specification : OpenGL
gl : Version 3.3 (상위도 괜찮으나 Reference를 따르겠습니다.)
Profile : Core
Option : Generate a loader (선택해야합니다.)

나머지는 선택하지 않고 GENERATE 합니다.

glad.zip를 다운로드 받습니다.

### 3. CMakeLists.txt 설정

기본적으로 VSCODE에서 CMake: Quick Start를 했다고 가정하겠습니다.

1. 다운로드한 파일을 압축을 해제합니다.
2. 본인의 프로젝트 폴더 안의 main.cpp와 같은 곳에 glad.c를 복사합니다.(GLAD의 src 폴더에 있음)

위 상황에서 CMakeLists.txt 파일을 작성하겠습니다.

```cmake
cmake_minimum_required(VERSION 3.0.0)
project(engineer_tool VERSION 0.1.0)

# 저의 Compiler Version은 19.34.31937로 C++20 대응합니다.
# VSCODE의 기본 문서 인코딩은 utf-8입니다.
add_compile_options("/std:c++latest")
add_compile_options("/utf-8")

include(CTest)
enable_testing()

# 라이브러리 폴더 설정
set(LIB_ROOT C:/c_library)
set(GLAD ${LIB_ROOT}/glad-opengl3.3)
set(GLFW ${LIB_ROOT}/glfw-3.3.8.bin.WIN64)

# include 디렉토리 설정
include_directories(
    ${GLAD}/include
    ${GLFW}/include
)

add_executable(
    engineer_tool 
    main.cpp
    glad.c      # OpenGL용 기본 파일 설정
)

target_link_libraries(
    engineer_tool
    ${GLFW}/lib-vc2022/glfw3.lib    # OpenGL용 Static Library 설정
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```

main.cpp 파일에서 반드시 glad를 먼저 include하고 glfw를 include 해야합니다. VSCODE에서 자동으로 include 순서를 정렬할 수 있으니 정렬 옵션을 해제하시면 편합니다. (C_Cpp: Clang_format_sort Includes)

신기하게 한글 주석때문에 정상 실행되지 않는 경우가 있습니다. 참고하시면 좋습니다.

```c
// main.cpp, 예외처리는 하지 않았습니다.
#include <glad/glad.h>
#include <GLFW/glfw3.h>

// 창크기 변경될 때마다 크기 조절해주는 callback 함수 설정
void framebuffer_size_callback(GLFWwindow* window, int width, int height);

int main(int argc, char** argv) {
    glfwInit();

    // OpenGL 3.3 버전 쓸거고 Legacy한 함수는 사용안하겠다는 뜻입니다.
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    // 사용할 window 만들고 주 컨텍스트로 설정
    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGLTutorial", NULL, NULL);
    glfwMakeContextCurrent(window);

    // 렌더링할 윈도우 사이즈 초기 설정 및 윈도우 사이즈 변경시마다 자동으로 수정해줄 callback 등록
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    // glad 설정
    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    // window 종료 명령어 안나오면 계속 실행합니다.
    while (!glfwWindowShouldClose(window)) {
        glfwSwapBuffers(window);  // double buffering 실행
        glfwPollEvents();         // 이벤트 확인하여 callback 함수 실행
    }

    // 종료 함수
    glfwTerminate();
    return 0;
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}
```

실행했을 때 그냥 검은 화면이 오면 됩니다. OpenGL로 무언가 만들고 싶다면 위의 레퍼런스를 참고해주시면 됩니다. 저희는 ImGUI를 사용하기 위한 Backend로만 일단 사용하고자 합니다.

## 2. Imgui 개요 및 데모

소스코드로만 이루어진 MIT 라이센스 C++ GUI Library 입니다. 

https://github.com/ocornut/imgui

자신의 C/C++ 프로젝트 내에 파일을 직접 복사하여 개발하는 형태를 띄는데 종속성이 없고 대부분의 상황을 지원해서 인기가 꽤 있는 모양입니다. 특히 게임과 관련된 곳에서 원활이 사용되고 있습니다.

imgui의 branch로 docking이 있는데, 원래 imgui에서 widget을 docking 할 수 있는 기능이 추가됬습니다. docking 기능 있는 것이 실제로 더 유용할 것이라고 판단되므로 docking branch를 기준으로 해당 문서를 작성합니다.

이 문서는 이미 작성된 OpenGL 문서 기준에서 작성되었습니다.

### 1. ImGui Docking branch와 CMakeLists.txt

imgui docking branch를 선택하셔서 다운로드 받습니다. 

1. 다운로드 받은 폴더의 최상단에 존재하는 모든 .h와 .cpp를 미리 만들어 놓은 프로젝트의 imgui 폴더에 복사합니다.
2. 다운로드 받은 폴더의 backends 폴더에서 glfw, opengl3와 관련있는 파일들을 imgui 폴더에 복사합니다.
   - imgui_impl_opengl3_loader.h, imgui_impl_glfw.cpp,imgui_impl_glfw.h, imgui_impl_opengl3.cpp,imgui_impl_opengl3.h

OpenGL에서 추가된 CMakeLists.txt 는 아래와 같이 작성하였습니다.

```cmake
cmake_minimum_required(VERSION 3.0.0)
project(engineer_tool VERSION 0.1.0)

# 저의 Compiler Version은 19.34.31937로 C++20 대응합니다.
# VSCODE의 기본 문서 인코딩은 utf-8입니다.
add_compile_options("/std:c++latest")
add_compile_options("/utf-8")

# MSVCRT 충돌 방지 (안하면 ImPlot 진행할때 경고 발생합니다)
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /NODEFAULTLIB:MSVCRT")

include(CTest)
enable_testing()

# 라이브러리 폴더 설정
set(LIB_ROOT C:/c_library)
set(GLAD ${LIB_ROOT}/glad-opengl3.3)
set(GLFW ${LIB_ROOT}/glfw-3.3.8.bin.WIN64)

# include 디렉토리 설정
include_directories(
    ${GLAD}/include
    ${GLFW}/include
)

# ImGUI 관련 파일이 많으므로 한꺼번에 처리하기 위한 설정
file(GLOB IMGUI_SRC imgui/*.cpp)

add_executable(
    engineer_tool 
    main.cpp
    glad.c          # OpenGL용 기본 파일 설정
    ${IMGUI_SRC}    # ImGUI용 기본 파일 설정
)

target_link_libraries(
    engineer_tool
    ${GLFW}/lib-vc2022/glfw3.lib    # OpenGL용 Static Library 설정
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```

### 2. ImGui Demo 실행

Demo 에는 ImGui에서 구현할 수 있는 대부분의 widget을 구경할 수 있습니다. 데모를 실행하는 코드는 다음과 같이 작성할 수 있습니다. (기본이 되는 코드이며, 향후 수정하는 코드의 기초가 됩니다.)

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include "imgui/imgui_impl_glfw.h"
#include "imgui/imgui_impl_opengl3.h"
#include "imgui/imgui.h"

// OpenGL 강의자료에서 참조하였습니다.
const char glsl_version[] = "#version 330 core";

void framebuffer_size_callback(GLFWwindow* window, int width, int height);

int main(int argc, char** argv) {
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGLTutorial", NULL, NULL);
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    // 데모 윈도우를 열기위해 작성합니다.
    bool show_demo_window = true;

    // IMGUI 기본 설정
    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();

    // 갖은 flag 설정이 가능한데, Docking 기능을 일단 중심으로 작성하였습니다.
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;  // Enable Keyboard Controls
    io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;      // Enable Docking
    io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;    // Enable Multi-Viewport / Platform Windows

    ImGui::StyleColorsDark();  // 테마 설정 가능합니다.

    ImGuiStyle& style = ImGui::GetStyle();
    if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
        style.WindowRounding = 0.0f;
        style.Colors[ImGuiCol_WindowBg].w = 1.0f;
    }

    // OpenGL과 ImGui를 연결하기 위한 함수 설정입니다.
    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    while (!glfwWindowShouldClose(window)) {
        // ImGui 창을 열기위한 설정입니다.
        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        // 실제로 여기에 Widget을 작성하면 됩니다.
        ImGui::ShowDemoWindow(&show_demo_window);

        // ImGui를 Rendering 하기 위한 영역입니다.
        ImGui::Render();
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);  // gl 함수를 통해 화면을 청소합니다.
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        // 열려있는 창 밖으로 꺼냈을 때 동작하는 설정입니다.
        if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
            GLFWwindow* backup_current_context = glfwGetCurrentContext();
            ImGui::UpdatePlatformWindows();
            ImGui::RenderPlatformWindowsDefault();
            glfwMakeContextCurrent(backup_current_context);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    // ImGui 종료시 메모리 정리합니다.
    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();

    glfwDestroyWindow(window);  // OpenGL 정리
    glfwTerminate();
    return 0;
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}
```

### 3. ImPlot Demo 실행

ImGui third party 중에 사용하면 좋을 것 같은 library입니다. ImGui의 widget에서 Plot을 그릴 수가 있습니다. 다만, 개인적으로 vecter map(quiver)가 필요하므로 제 입장에서 한계점은 존재합니다. 역으로 직접 구현하는건 쉽지 않아 보입니다.

https://github.com/epezent/implot

다운로드 받은 모든 .h/.cpp 파일 include/imgui 폴더에 넣습니다. 동일한 경로에 넣기 때문에 CMakeLists.txt파일은 수정할 필요가 없습니다. 

implot를 위한 header 파일을 포함하여 실제로 작성되어야하는 코드는 지극히 적습니다. 

```cpp
#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include "imgui/imgui_impl_glfw.h"
#include "imgui/imgui_impl_opengl3.h"
#include "imgui/imgui.h"

#include "imgui/implot.h"

const char glsl_version[] = "#version 330 core";

void framebuffer_size_callback(GLFWwindow* window, int width, int height);

int main(int argc, char** argv) {
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGLTutorial", NULL, NULL);
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    bool show_demo_window = true;

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImPlot::CreateContext();  // ImPlot을 위한 설정이 추가됩니다.
    ImGuiIO& io = ImGui::GetIO();

    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
    io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;
    io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;

    ImGui::StyleColorsDark();

    ImGuiStyle& style = ImGui::GetStyle();
    if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
        style.WindowRounding = 0.0f;
        style.Colors[ImGuiCol_WindowBg].w = 1.0f;
    }

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    while (!glfwWindowShouldClose(window)) {
        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        ImGui::ShowDemoWindow(&show_demo_window);

        // ImPlot Demo
        ImPlot::ShowDemoWindow(&show_demo_window);

        ImGui::Render();
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
            GLFWwindow* backup_current_context = glfwGetCurrentContext();
            ImGui::UpdatePlatformWindows();
            ImGui::RenderPlatformWindowsDefault();
            glfwMakeContextCurrent(backup_current_context);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImPlot::DestroyContext();  // ImPlot을 위한 설정이 추가됩니다.
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}
```

### 4. imgui-filebrowser Demo 실행 그리고 한글 적용

ImGui github에는 몇가지 File Dialog 라이브러리가 링크되어 있습니다. 다만, OpenGL을 사용하는 한 선택에 제약이 있습니다.

<center>

|     Widget 명     | OpenGL 적용 가능 | 한글 가능 | 디자인 |
| :---------------: | :--------------: | :-------: | :----: |
|   ImFileDialog    |        X         |     -     |   O    |
|   L2DFileDialog   |        X         |     -     |   -    |
|  ImGuiFileDialog  |        O         |     X     |   O    |
| imgui-filebrowser |        O         |     O     |   -    |
| g's ImGui-Addons  |        O         |     -     |   X    |
| F's ImGui-Addons  |        O         |     -     |   X    |

</center>

ImFileDialog은 SDL에 종속이라 사용이 어려우며 ImGuiFileDialog는 한글을 인식을 못합니다. 결과적으로 선택지는 하나 밖에 없고 해당 Library를 추가로 사용법을 작성하겠습니다

두 가지 주의할 점이 있습니다.
1. 한글을 적용해야합니다. 해당 코드를 유심히 확인해주시길 바랍니다.
2. std:c++17 이상의 compiler가 필요합니다. (저희는 c++17 이상을 사용 중이므로 상관 없음)

https://github.com/AirGuanZ/imgui-filebrowser

링크를 찾아가셔서 다운로드 받으시면 옮길 파일은 imfilebrowser.h 밖에 없습니다.

ImGUI에 한글을 적용하는 방법은 `io.Fonts->AddFontFromFileTTF()` 함수를 사용하면 됩니다. 한글을 적용함과 동시에 Demo를 작성하겠습니다. 단, 한글 작성등은 잘 되지 않습니다. 이 부분은 다음 챕터에서 진행하겠습니다.

한글 적용 Reference : https://dlemrcnd.tistory.com/65

```cpp
// APIENTRY Macro 중복 Warning 제거
#pragma warning(disable : 4005)

#include <iostream>

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#include "imgui/imgui_impl_glfw.h"
#include "imgui/imgui_impl_opengl3.h"
#include "imgui/imgui.h"

#include "imgui/implot.h"
#include "imgui/imfilebrowser.h"

const char glsl_version[] = "#version 330 core";

void framebuffer_size_callback(GLFWwindow* window, int width, int height);

int main(int argc, char** argv) {
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGLTutorial", NULL, NULL);
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    bool show_demo_window = true;

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImPlot::CreateContext();
    ImGuiIO& io = ImGui::GetIO();

    // 한글 적용
    io.Fonts->AddFontFromFileTTF("C://windows/Fonts/malgun.ttf", 18.0f, NULL, io.Fonts->GetGlyphRangesKorean());

    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
    io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;
    io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;

    ImGui::StyleColorsDark();

    ImGuiStyle& style = ImGui::GetStyle();
    if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
        style.WindowRounding = 0.0f;
        style.Colors[ImGuiCol_WindowBg].w = 1.0f;
    }

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    // File Dialog를 위한 초기 설정입니다.
    ImGui::FileBrowser fileDialog;

    fileDialog.SetTitle("title");
    fileDialog.SetTypeFilters({".h", ".cpp"});

    // OpenGL Loop
    while (!glfwWindowShouldClose(window)) {
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        // ImGui Demo
        ImGui::ShowDemoWindow(&show_demo_window);

        // ImPlot Demo
        ImPlot::ShowDemoWindow(&show_demo_window);

        // File Browser Demo
        if (ImGui::Begin("dummy window")) {
            // open file dialog when user clicks this button
            if (ImGui::Button("open file dialog"))
                fileDialog.Open();
        }
        ImGui::End();

        fileDialog.Display();

        if (fileDialog.HasSelected()) {
            std::cout << "Selected filename" << fileDialog.GetSelected().string() << std::endl;
            fileDialog.ClearSelected();
        }

        ImGui::Render();
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
            GLFWwindow* backup_current_context = glfwGetCurrentContext();
            ImGui::UpdatePlatformWindows();
            ImGui::RenderPlatformWindowsDefault();
            glfwMakeContextCurrent(backup_current_context);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImPlot::DestroyContext();  // ImPlot을 위한 설정이 추가됩니다.
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}
```

## 3. IMGUI Image Viewer

IMGUI가 다각도록 빠르고 편하긴 하지만, 이미지 로딩하는 방식은 다소 번거롭습니다. IMGUI Github에 다음과 같은 예제가 있으니 따라 해 보겠습니다.

Reference : https://github.com/ocornut/imgui/wiki/Image-Loading-and-Displaying-Examples

### 1. stb_image.h 라이브러리 설치

사실 위 라이브러리는 설치랄 것도 없이 그냥 복사하면 됩니다만, 반드시 바로 상단에 `STB_IMAGE_IMPLEMENTATION` 매크로가 포함되어 있어야합니다.

Github : https://github.com/nothings/stb

상당한 유용한 라이브러리들이 많으니 향후 참조하도록 합니다.

```cpp
# 포함되어야할 예시
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
```

### 2. 최종 샘플 CMAKE

```cmake
cmake_minimum_required(VERSION 3.0.0)
project(engineer_tool VERSION 0.1.0)

# 저의 Compiler Version은 19.34.31937로 C++20 대응합니다.
# VSCODE의 기본 문서 인코딩은 utf-8입니다.
add_compile_options("/std:c++20")
add_compile_options("/utf-8")

# MSVCRT 충돌 방지 (안하면 ImPlot 진행할때 경고 발생합니다)
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} /NODEFAULTLIB:MSVCRT")

include(CTest)
enable_testing()

# 라이브러리 폴더 설정
set(LIB_ROOT C:/c_library)
set(GLAD ${LIB_ROOT}/glad-opengl3.3)
set(GLFW ${LIB_ROOT}/glfw-3.3.8.bin.WIN64)
set(STB ${LIB_ROOT}/stb)

# include 디렉토리 설정
include_directories(
    ${GLAD}/include
    ${GLFW}/include
    ${STB}
)

# ImGUI 관련 파일이 많으므로 한꺼번에 처리하기 위한 설정
file(GLOB IMGUI_SRC imgui/*.cpp)

add_executable(
    engineer_tool 
    main.cpp
    glad.c          # OpenGL용 기본 파일 설정
    ${IMGUI_SRC}    # ImGUI용 기본 파일 설정
)

target_link_libraries(
    engineer_tool
    ${GLFW}/lib-vc2022/glfw3.lib    # OpenGL용 Static Library 설정
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```

### 3. 최종 샘플 코드

실제로 사용하기엔 함수화 시켜야할 것들이 많지만 IMGUI+OpenGL의 기본 양식으로 쓸 수 있습니다.

```cpp
// APIENTRY Macro 중복 Warning 제거
#pragma warning(disable : 4005)

#include <iostream>

#include <glad/glad.h>
#include <GLFW/glfw3.h>

#define STB_IMAGE_IMPLEMENTATION
#include <stb_image.h>

#include "imgui/imgui_impl_glfw.h"
#include "imgui/imgui_impl_opengl3.h"
#include "imgui/imgui.h"

#include "imgui/implot.h"
#include "imgui/imfilebrowser.h"

using namespace std::string_literals;

const char glsl_version[] = "#version 330 core";

void framebuffer_size_callback(GLFWwindow* window, int width, int height);

int main(int argc, char** argv) {
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);

    GLFWwindow* window = glfwCreateWindow(800, 600, "OpenGLTutorial", NULL, NULL);
    glfwMakeContextCurrent(window);
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);

    gladLoadGLLoader((GLADloadproc)glfwGetProcAddress);

    bool show_demo_window = true;

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImPlot::CreateContext();
    ImGuiIO& io = ImGui::GetIO();

    // 한글 적용
    io.Fonts->AddFontFromFileTTF("C://windows/Fonts/malgun.ttf", 18.0f, NULL, io.Fonts->GetGlyphRangesKorean());

    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;
    io.ConfigFlags |= ImGuiConfigFlags_DockingEnable;
    io.ConfigFlags |= ImGuiConfigFlags_ViewportsEnable;

    ImGui::StyleColorsDark();

    ImGuiStyle& style = ImGui::GetStyle();
    if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
        style.WindowRounding = 0.0f;
        style.Colors[ImGuiCol_WindowBg].w = 1.0f;
    }

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    // File Dialog를 위한 초기 설정입니다.
    ImGui::FileBrowser fileDialog;

    fileDialog.SetTitle("title");
    fileDialog.SetTypeFilters({".h", ".cpp"});


    // 이미지 로딩을 위한 처리, Reference와 다르게 그냥 함수화 하진 않았습니다.
    int image_width = 0;
    int image_height = 0;

    // 원본 이미지는 Debug 폴더에 넣어놨기 때문에 실행 파일과 위치가 같습니다.
    unsigned char* image_data = stbi_load("container.jpg", &image_width, &image_height, NULL, 4);

    GLuint image_texture;
    glGenTextures(1, &image_texture);
    glBindTexture(GL_TEXTURE_2D, image_texture);

    // 이미지 실제 크기를 줄이느냐 늘이느냐에 따른 처리 방법 예제
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE);

    // 실제로 이미지 OpenGL에서 읽어들이기
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data);
    stbi_image_free(image_data);    // 메모리에 올라가 있는 것은 메모리 정리

    // OpenGL Loop
    while (!glfwWindowShouldClose(window)) {
        glClearColor(0.2f, 0.3f, 0.3f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        // ImGui Demo
        ImGui::ShowDemoWindow(&show_demo_window);

        // ImPlot Demo
        ImPlot::ShowDemoWindow(&show_demo_window);

        // File Browser Demo
        if (ImGui::Begin("dummy window")) {
            // open file dialog when user clicks this button
            if (ImGui::Button("open file dialog"))
                fileDialog.Open();
        }
        ImGui::End();

        // 한글 사용 사례
        ImGui::Begin("한글 좋아!");
        ImGui::End();

        fileDialog.Display();

        if (fileDialog.HasSelected()) {
            std::cout << "Selected filename" << fileDialog.GetSelected().string() << std::endl;
            fileDialog.ClearSelected();
        }

        // 이미지 처리 예제
        ImGui::Begin("OpenGL Texture Text");
        ImGui::Text("pointer = %p", image_texture);
        ImGui::Text("size = %d x %d", image_width,image_height);
        ImGui::Image((void*)(intptr_t)image_texture, ImVec2(image_width, image_height));
        ImGui::End();

        // UI 렌더링
        ImGui::Render();
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        if (io.ConfigFlags & ImGuiConfigFlags_ViewportsEnable) {
            GLFWwindow* backup_current_context = glfwGetCurrentContext();
            ImGui::UpdatePlatformWindows();
            ImGui::RenderPlatformWindowsDefault();
            glfwMakeContextCurrent(backup_current_context);
        }

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImPlot::DestroyContext();  // ImPlot을 위한 설정이 추가됩니다.
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}

void framebuffer_size_callback(GLFWwindow* window, int width, int height) {
    glViewport(0, 0, width, height);
}
```
