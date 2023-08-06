# mkdocs 설정

mkdocs를 사용하여 문서화를 하겠다고 마음 먹었습니다. 그런데 mkdocs.yml 설정하는 방법이 산재되어 있어서 간단하게 기록해둡니다.

## 1. mkdocs.yml

python 자동 문서 및 latex 작성이 가능한 설정법입니다.

```yml
# 해당 문서 예시
site_name: Engineer For Programing

theme : material
use_directory_urls: true

markdown_extensions:
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.inlinehilite
  - pymdownx.snippets
  - pymdownx.superfences

plugin:
  - search
  - mkdocstring

extra_javascript:
  - javascripts/mathjax.js
  - https://polyfill.io/v3/polyfill.min.js?features=es6
  - https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js


nav:
  - Home: index.md
  - C&C++: 
    - 000 C&C++/000 VSCODE로 C++ 시작하기.md
    - 000 C&C++/001 ImGui With OpenGL.md
    - 000 C&C++/002 vcpkg 설정.md
    - 000 C&C++/003 vcpkg 라이브러리 설치.md
    - Cinder 설치 그리고:
      - ImGui: 000 C&C++/010 Cinder 설치 그리고 ImGui.md
      - Box2D: 000 C&C++/011 Cinder 설치 그리고 Box2D.md
      - Bullet: 000 C&C++/012 Cinder 설치 그리고 Bullet.md
```

## 2. 주석

mkdocs는 google, numpy 등 몇개를 지원한다고 하는데 google을 잘 지원하니 google 형태를 사용하도록 합니다.