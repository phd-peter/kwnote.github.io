---
title: "깃허브 작동방식과 내가 매일할일"
date: 2024-07-13
layout: single
comments: true
published: true
categories: [자기계발]
tags: [깃허브]


---

# 깃허브 작동방식과 내가 매일할일

- **Local files** --- **Github files**

- 연동을 잘 시키는 것이 중요하다. 보통은 Local을 수정하기 때문에, Github에 그 때 그 때 Push해야한다. 



Typora는 단순 에디터. md 파일을 수정할 수 있다. VS code를 통해서 깃허브와 소통할 수 있다.

### 깃에 올리는 방법

``` python
# 현재 상태 확인
git status

# 변경된 파일 스테이징
git add .

# 변경 사항 커밋
git commit -m "Add new blog post"

# 변경 사항 푸시
git push origin master
```



### 깃에서 내려받는 경우

```python
    # 1. 터미널 열기 (VS Code 내에서)
    # 2. 현재 상태 확인
    git status

    # 3. 원격 저장소의 변경 사항 가져오기
    git pull origin master

    # (필요 시) 충돌 해결
    # 충돌된 파일을 편집하여 해결한 후:
    git add .
    git commit -m "Resolve merge conflict"

    # 5. 로컬 변경 사항 푸시
    git push origin master

```

## 이미지 삽입 방법

1. typora에 이미지 삽입 (셋팅해놓기로는 Local 폴더에 image아래에 저장되게 해놓음)

2. VS code를 통해서 terminal에서 commit과 push를 한다.

3. **Git website에서 post를 수정한다. 앞쪽을 {{site.url}}로 수정해야함**. 검색 등을 통해서 한방에 샥~

```python
# 예시
# 기존
![timetable-example22](/Users/peter/github/kwnote.github.io/images/2024-07-12-first/timetable-example22.png)

# 변경후
![timetable-example22]({{site.url}}/images/2024-07-12-first/timetable-example22.png)

# 결국엔 이걸 치환하는 것이다.
# /Users/peter/github/kwnote.github.io 
# {{site.url}}

```

## 단순꿀팁

맥북에서는 백틱이 입력안된다.

option+₩누르거나, 영어로 바꾼다음에 ₩를 치면 백틱이 된다.
