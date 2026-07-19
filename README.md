# Fallout 2 Nevada Korean Translation

Fallout 2: Nevada의 대화문, 기록, UI 텍스트 등을 한국어로 번역한 파일입니다.

---

## 한글 적용 방법

1. Fallout 2 본편을 설치합니다.
2. [Fallout Nevada Extended 버전](https://www.nma-fallout.com/threads/fallout-nevada-extended.207311/)을 설치합니다.
3. 이 저장소의 한국어 번역 데이터를 Fallout 2 본편 폴더 내 Nevada Mod (Extended)에 덮어씁니다. 배포물에는 한글 Sfall `ddraw.dll`, `LangFont.ini`, `fonts` 폴더가 포함되어 있습니다.
4. `Nevada.cfg` 파일을 열고 `[system]` 섹션에서 아래와 같이 수정합니다.

```ini
[system]
language=korean
```
5. sfall의 버전이 다르기 때문에 창 조절은 SF-configurator.exe로 가능합니다.

`Nevada.cfg`의 다른 값과 기존 `ddraw.ini`, `sfall.dat`는 설치 환경별 설정이므로 유지하십시오. 이미 `language=` 줄이 있다면 새 줄을 추가하지 말고 그 값만 변경합니다.

---

## 주의사항

* 이 자료는 Fallout 2: Nevada용 한국어 번역 데이터입니다.
* Fallout 2 본편 및 Fallout Nevada 원본 파일은 포함되어 있지 않습니다.

---

## Credits

* Fallout 2: Nevada 개발진
* Fallout Nevada Extended 제작진
* Korean translation: `munument1`
* * SFall 제작진 - (한글호환패치 [소스코드](https://github.com/munument1/Unofficial-KR-Sfall))
