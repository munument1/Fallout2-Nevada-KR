# 네바다 한국어 완성형 패키지

[최신 패키지 다운로드](https://github.com/munument1/Fallout2-Nevada-KR/releases/latest)

Nevada Extended용 한국어 번역, 실행 파일과 글꼴 설정을 함께 구성했습니다.

## 설치

1. 게임을 종료합니다.
2. `Fallout2-Nevada-KR-classic-complete.zip`의 내용물을 네바다 설치 폴더에 모두 덮어씁니다.
3. `Nevada.exe` 또는 `NevadaHD.exe`를 실행합니다.

한국어 설정은 미리 적용되어 있습니다. 원하면 기존 파일을 백업한 뒤 덮어쓰세요.

## 적용 내용

- 기존 한국어 번역 데이터 보존
- `Nevada.cfg` 한국어 설정
- 일반판·HD판 한국어 출력 연결
- 본문 돋움 11, 버튼 카페24 아네모네 에어 16·굵게
- 네바다 동봉 sfall의 한국어 메시지와 실행 파일 등록

[설치 및 확인 범위](docs/CLASSIC_COMPLETE_KO.md)

## 패키지 제작

완성형 패키지는 소유자의 검증된 네바다 설치 파일과 기존 번역 ZIP으로 만듭니다. 공통 글꼴 DLL은 v1.2.3과 동일하며, HD 실행 파일의 초기화 연결만 네바다 패키지에 보충합니다.

```powershell
python tools/build_classic_complete.py --game "D:\Fallout 2\Nevada" --translations translation-data.zip --output Fallout2-Nevada-KR-classic-complete.zip --engine-tools path/to/Fallout2-Korean-Text-Engine
```

빌드에는 Python과 `pefile`이 필요합니다. `--game`은 기존 공통 출력 엔진 v1.2.3을 적용한 빌드용 입력이며, 배포 ZIP을 받는 사용자는 위 설치 과정만 진행하면 됩니다. 패키지 제작 시 파일 해시, HD 패치 범위 및 ZIP 무결성을 검사합니다.

## 이전 방식과 크레딧

[기존 번역·제작자 기록](docs/LEGACY_INSTALLATION_KO.md)을 보존합니다. 공통 출력 모듈은 [Fallout2 Korean Text Engine](https://github.com/munument1/Fallout2-Korean-Text-Engine), 카페24 글꼴의 라이선스는 배포본 `fonts` 폴더에 있습니다.
