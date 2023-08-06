# Rust With Jupyter

Jupyter에서 Rust를 동작시킬 수 있습니다. 다만 조금 느리긴 합니다. 또한 인터넷에는 전부 Conda로 설치하라고 되어있는데 저는 Conda가 싫고 그냥 VSCODE로 개발 할 것이므로 설정했던 사항들을 정리하는 차원에서 이 글을 작성합니다.

## 1. install evcxr_jupyter 

```shell
cargo install evcxr_jupyter # 라이브러리 추가
evcxr_jupyter --install # jupyter에 rust 등록
```

설치하는데 시간이 조금 걸립니다. 여유롭게 기다리도록 합니다.

## 2. Jupyter 설정

Conda로 실행해보질 않아서 Rust와 연계성이 얼마나 좋은지는 잘 모르겠습니다.
위에 설명한 것처럼 설치한 이후에 아래 명령어를 입력하면 Rust를 실행시킬 수 있는 
jupyter notebook을 열 수 있습니다.

```shell
python -m pip install jupyter notebook # jupyter 설치
jupyter-notebook # 버젼에 따라 jupyter notebook 일 수도 있습니다.
```

오른쪽 상단에 kernel 설정하는 데서 Rust를 선택할 수 있다는 것을 알 수 있습니다.
그러나 이 jupyter는 어떤 링크에서 열리는 형태이며 기나긴 token이 있는 것을 알 수 있습니다.
심지어 jupyter 실행할 때마다 저 token은 변경됩니다.

token을 고정시켜보겠습니다.

```shell
# 상황에 따라 jupyter notebook 일 수도 있습니다.
jupyter-notebook --generate-config
```

위 명령어를 기입하면 사용자 폴더 내 `jupyter_notebook_config.py`와 같은 파일이 만들어지며
이 파일을 수정하면 됩니다. 경로는 위 generate명령어를 통해 cmd 창에서 확인할 수 있습니다.

`c.NotebookApp.token = '<generated>'` 을 `c.NotebookApp.token = 'jupyter'` 로 변경하였습니다.

다시 jupyter를 실행해보겠습니다.

```shell
# 상황에 따라 jupyter notebook 일 수도 있습니다.
jupyter-notebook --generate-config
```

그럼 이제 토큰이 숨겨져있습니다. 우리는 이미 수동으로 토큰을 설정했으니 토큰을 알고 있습니다.
적당한 이름의 ipynb 파일을 만들면 kernel을 선택하는 곳에 아래와 같은 uri를 입력하면 됩니다.

`http://127.0.0.1:8888/?token=jupyter`

다만, VSCODE에 따라 저 uri를 입력 못할 수 도 있는데 `ctrl+shift+p` 명령어를 통해 
`Jupyter: Specify Jupyter Server for Connections`를 기입하여 입력할 수 있습니다.
해당 명령어는 deprecated 된다고 되어있는데 회사에서는 이 명령어를 통해 사용할 수 있었습니다 (230512)

jupyter 실행하면 계속 자동으로 브라우저가 열리니 귀찮으니 끄는 설정까지 해놓겠습니다.

`c.NotebookApp.open_browser = True`에서 `c.NotebookApp.open_browser = False`로 변경합니다.