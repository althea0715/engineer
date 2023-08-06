# vcpkg 라이브러리 설치

위 라이브러리들은 상당히 유명한 라이브러리들로 사용하기로 마음을 먹은 라이브러리 들입니다. 필요하신분은 따라해주시면 되겠습니다.

## 1. Googletest 설치

몇가지 TDD 라이브러라기 있으나 googletest를 활용하여 개발해보겠습니다. 우리는 vcpkg가 있으니 googletest는 해당 패키지 관리자로 사용하겠습니다.

`vcpkg install gtest:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 정상적으로 완료되면 아래와 같이 사용하라고 가이드가 나옵니다.

```cmake
find_package(GTest CONFIG REQUIRED)
target_link_libraries(main PRIVATE GTest::gtest GTest::gtest_main GTest::gmock GTest::gmock_main)
```

## 2. Abseil 설치

Abseil에서 제공하는 status 라이브러리에 관심이 생겨서 진행하려던 중에 결과적으로 StatusOr 는 정상적으로 사용할 수 없다는 것을 확인하였습니다. 그러나 갖가지 라이브러리 총체이긴해서 일단 설치합니다.

`vcpkg install abseil[cxx17]:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 정상적으로 완료되면 아래와 같이 사용하라고 가이드가 나옵니다. abseild이 c++17 이상으로 build 해야한다고 다들 추천하기 때문에 해당 cxx17이 포함된 옵션으로 진행하였습니다.

```cmake
find_package(absl CONFIG REQUIRED)
# note: 171 additional targets are not displayed.
target_link_libraries(main PRIVATE absl::any absl::log absl::base absl::bits)
```

## 3. Protobuf 설치

구글 라이브러리를 사용하겠다고 결정해놓고 사용 안하면 아쉬운 protobuf를 설치합니다.

`vcpkg install protobuf[zlib]:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 정상적으로 완료되면 아래와 같이 사용하라고 가이드가 나옵니다. zlib를 설치안하면 몇개의 함수가 동작안하기 때문에, 설치하도록 합니다.

```cmake
find_package(protobuf CONFIG REQUIRED)
target_link_libraries(main PRIVATE protobuf::libprotoc protobuf::libprotobuf protobuf::libprotobuf-lite)
```

protobuf를 사용하기 위해선 proto 파일을 변활할 실행 파일이 필요합니다. 이는 vcpkg 설치된 폴더에 있습니다. 저의 경우엔 아래와 같습니다.

`C:\c_library\vcpkg\installed\x64-windows\tools\protobuf`

경로에 `protoc.exe` 파일이 있습니다. 그러므로 위의 경로를 환경변수로 등록하는 것이 편합니다.

## 4. gRPC 설치

protobuf와 마찬가지로 사용 안하면 아쉬운 gRPC를 설치합니다.

`vcpkg install grpc:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 정상적으로 완료되면 아래와 같이 사용하라고 가이드가 나옵니다. 조금 많은 라이브러리들이 설치되는데 기다려줍니다.

```cmake
find_package(gRPC CONFIG REQUIRED)
# note: 7 additional targets are not displayed.
target_link_libraries(main PRIVATE gRPC::gpr gRPC::grpc gRPC::grpc++ gRPC::grpc++_alts)
```

gRPC를 사용할 때 protobuf를 반드시 사용해야하는데, protobuf로 gRPC 문서를 만들기 위해선 --grpc_out 명령어를 추가로 해야합니다. 그리고 plugin을 추가해야하는데 이는 gRPC 설치된 폴더에서 찾을 수 있습니다. 저의 경우엔 아래와 같습니다.

`C:\c_library\vcpkg\installed\x64-windows\tools\grpc`

즉, test.proto가 있다고 했을 때 명령창에 아래와 같이 작성해볼 수 있습니다.

```terminal
protoc test.proto --grpc_out=. --plugin=protoc-gen-grpc=C:/c_library/vcpkg/installed/x64-windows/tools/grpc/grpc_cpp_plugin.exe
```

## 5. Eigen

수학 계산을 위해 설치하는 라이브러리입니다. 수 많은 라이브러리 중에 왜 사용 했는지는 후반부에 작성해놓은 비교 문서를 확인해보시면 됩니다. 다만, 비교문서에는 직접 설치하는 방법이 설명되어있습니다.

`vcpkg install eigen3:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. eigen 라이브러리는 사실 build가 되지 않아서 include만 하면 되는 함수이긴 하지만 vcpkg로 설치하는 것이 편하므로 이 방법을 권장합니다.

```cmake
find_package(Eigen3 CONFIG REQUIRED)
target_link_libraries(main PRIVATE Eigen3::Eigen)
```

## 6. POCO

다양한 기능을 제공하는 라이브러리로써 http request를 위해 설치를 하였습니다. 다양한 사용 방법이 있는 것 같은데 잘 정리해두겠습니다. Poco 라이브러리는 github에 예제 파일을 제공하니 반드시 사용할 때 참고하시기 바랍니다.

`vcpkg install poco:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 아래 작성되는 cmake 코드는 저렇게 바로 사용하면 안됩니다.

```cmake
find_package(Poco REQUIRED [COMPONENTS <libs>...])
target_link_libraries(main PRIVATE Poco::<libs>)
```

만약 내가 POCO 라이브러리의 Net을 사용하겠다고하면 다음과 같이 작성할 수 있습니다.

```cmake
find_package(Poco REQUIRED COMPONENTS Net)
target_link_libraries(main PRIVATE Poco::Net)
```

## 7. glfw

초반에 설명에는 glfw를 직접 다운로드 받아서 진행하는 방식을 취했습니다. 하지만 glfw도 vcpkg로 다운로드 받을 수 있어서 기록해둡니다.

`vcpkg install glfw3:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. glad를 설치해야하는 것은 어쩔수 없으므로 glad는 따로 다운로드 받도록 합니다.

```cmake
# this is heuristically generated, and may not be correct
find_package(glfw3 CONFIG REQUIRED)
target_link_libraries(main PRIVATE glfw)
```

## 8. stb

이 라이브러리 또한 IMGUI 설명할 때 이미지를 읽어들이기 위한 라이브러리였습니다. 이 또한 vcpkg에서 지원하여 기록해둡니다.

`vcpkg install stb:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 이 라이브러리는 헤더만 있는 라이브러리로써 기존에는 link를 했어야하는데 이 라이브러리는 include를 하면 됩니다.

```cmake
find_package(Stb REQUIRED)
target_include_directories(main PRIVATE ${Stb_INCLUDE_DIR})
```

## 9. tinyxml2

Poco에서 XML과 SAX를 둘 다 지원해서 써보려고 하였지만, 너무 가독성이 떨어지고 어렵습니다. 그냥 tinyxml2을 사용하는 것이 속편합니다.

`vcpkg install tinyxml2:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다.

```cmake
# this is heuristically generated, and may not be correct
find_package(tinyxml2 CONFIG REQUIRED)
target_link_libraries(main PRIVATE tinyxml2::tinyxml2)
```

## 10. bullet3

3D 물리 엔진이며, 결국 저의 목표가 3D 물리 시뮬레이션이기 때문에 설치방법을 작성합니다. NVIDIA에서 만든 Physx 라이브러리가 있지만, 대체적으로 게임을 위한 라이브러리라고 좀 더 연산이 간소화되어있다고 하여 사용하지 않기로 결정하였습니다. 또한 github star에 의존하는 저로써는 github star가 더 많은 것을 해야겠다고 생각하게 되었습니다.

`vcpkg install bullet3:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 코멘트로 static만 설치된다고 하던데, 사용하는데 별 지장은 없습니다.

```cmake
find_package(Bullet CONFIG REQUIRED)
target_link_libraries(main PRIVATE ${BULLET_LIBRARIES})
```

## 11. Dataframe

파이썬의 pandas와 비슷한 라이브러리이지만 상당히 제약적인 기능을 갖추고 있습니다. 다만 그와 유사한 어느 라이브러리도 존재하지 않기 때문에 이 라이브러리가 그나마 꿀같은 라이브러리입니다.

`vcpkg install dataframe:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 

```cmake
# this is heuristically generated, and may not be correct
find_package(DataFrame CONFIG REQUIRED)
target_link_libraries(main PRIVATE DataFrame::DataFrame)
```

## 12. glm

OpenGL을 사용하게 되면 필연적으로 연산에 필요한 라이브러리입니다.

`vcpkg install glm:x64-windows`를 기입하면 다운로드 & Build가 진행됩니다. 

```cmake
# this is heuristically generated, and may not be correct
find_package(glm CONFIG REQUIRED)
target_link_libraries(main PRIVATE glm::glm)
```