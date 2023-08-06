# Cinder 설치 그리고 Box2D

Cinder와 Box2D를 결합하면 2차원 물리모델을 구현하는데 많은 도움이 될 것입니다. Box2D는 전 페이지에서 설명한 `TinderBox-Win`를 사용하면 쉽게 프로젝트를 만들 수 있지만, 여기서는 VSCODE로 진행하고자합니다.

## 1. Box2D 설치

vcpkg 등으로 직접 설치해도 되지만, Cinder에 소스코드가 `TinderBox-Win`과 함께 내장되어있습니다. 거기서 직접 가져오는 형태를 취합니다.

저의 경로는 다음과 같습니다. `C:\c_library\Cinder\blocks\Box2D\src`

위 경로를 토대로 cmakelists.txt 파일을 수정할 수 있습니다.

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

# zlib 설정
find_package(ZLIB REQUIRED)

# Cinder 설정
set(CINDER C:/c_library/Cinder)

# Box2D cpp 파일 로딩을 위해 선언합니다.
file(GLOB BOX2D_SRC 
    ${CINDER}/blocks/Box2D/src/Box2D/Collision/*.cpp
    ${CINDER}/blocks/Box2D/src/Box2D/Collision/Shapes/*.cpp
    ${CINDER}/blocks/Box2D/src/Box2D/Common/*.cpp
    ${CINDER}/blocks/Box2D/src/Box2D/Dynamics/*.cpp
    ${CINDER}/blocks/Box2D/src/Box2D/Dynamics/Contacts/*.cpp
    ${CINDER}/blocks/Box2D/src/Box2D/Dynamics/Joints/*.cpp
    ${CINDER}/blocks/Box2D/src/Box2D/Rope/*.cpp
)

# Cinder에서 OpenGL 사용시 terminal을 사용안하기 때문에 WIN32 키워드가 필요합니다.
add_executable(
    engineer_tool WIN32
    main.cpp
    ${BOX2D_SRC}
)

# Box2D 적용
target_include_directories(
    engineer_tool PRIVATE
    ${CINDER}/include
    ${CINDER}/blocks/Box2D/src
)

target_link_libraries(
    engineer_tool PRIVATE
    ZLIB::ZLIB
    ${CINDER}/lib/msw/x64/Debug/v143/cinder.lib
)

set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)
```

## 2. Box2D 실행 확인

튜토리얼을 옮겨 봤습니다. 단, 해당 튜토리얼은 내장된 코드를 활용하였습니다. 코드를 분석할 필요는 있지만 이번 장에서 진행하진 않겠습니다.

```cpp
#pragma warning(disable : 4828)

#include <vector>

#include "cinder/app/App.h"
#include "cinder/app/RendererGl.h"
#include "cinder/gl/gl.h"

// Box2D를 사용하기 위해 선언
#include "Box2D/Box2D.h"

using namespace ci;
using namespace ci::app;
using namespace std;

const float BOX_SIZE = 10;

class CinderProjectApp : public App {
   private:
    b2World *mWorld;
    vector<b2Body *> mBoxes;

   public:
    void setup() override;
    void draw() override;
    void update() override;
    void mouseDown(MouseEvent event) override;

    void addBox(const vec2 &pos);
};

void CinderProjectApp::setup() {
    b2Vec2 gravity(0.0f, 10.0f);
    mWorld = new b2World(gravity);

    b2BodyDef groundBodyDef;
    groundBodyDef.position.Set(0.0f, getWindowHeight());
    b2Body *groundBody = mWorld->CreateBody(&groundBodyDef);

    // Define the ground box shape.
    b2PolygonShape groundBox;

    // The extents are the half-widths of the box.
    groundBox.SetAsBox(getWindowWidth(), 10.0f);

    // Add the ground fixture to the ground body.
    groundBody->CreateFixture(&groundBox, 0.0f);
}

void CinderProjectApp::addBox(const vec2 &pos) {
    b2BodyDef bodyDef;
    bodyDef.type = b2_dynamicBody;
    bodyDef.position.Set(pos.x, pos.y);

    b2Body *body = mWorld->CreateBody(&bodyDef);

    b2PolygonShape dynamicBox;
    dynamicBox.SetAsBox(BOX_SIZE, BOX_SIZE);

    b2FixtureDef fixtureDef;
    fixtureDef.shape = &dynamicBox;
    fixtureDef.density = 1.0f;
    fixtureDef.friction = 0.3f;
    fixtureDef.restitution = 0.5f;  // bounce

    body->CreateFixture(&fixtureDef);
    mBoxes.push_back(body);
}

void CinderProjectApp::mouseDown(MouseEvent event) { addBox(event.getPos()); }

void CinderProjectApp::update() {
    for (int i = 0; i < 10; ++i) mWorld->Step(1 / 30.0f, 10, 10);
}

void CinderProjectApp::draw() {
    gl::clear();

    gl::color(1, 0.5f, 0.25f);
    for (const auto &box : mBoxes) {
        gl::pushModelMatrix();
        gl::translate(box->GetPosition().x, box->GetPosition().y);
        gl::rotate(box->GetAngle());

        gl::drawSolidRect(Rectf(-BOX_SIZE, -BOX_SIZE, BOX_SIZE, BOX_SIZE));

        gl::popModelMatrix();
    }
}

CINDER_APP(CinderProjectApp, RendererGl)
```