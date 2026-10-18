# 네바다 한국어 번역 — 공통 출력 엔진 방식

## 기존 설치 폴더에 바로 설치 (v1.2.1)

게임을 종료한 뒤 **Steam을 포함한 기존 게임·모드 설치 폴더**를 선택하세요. 시험용 전체 복사본 준비는 선택 사항입니다. 번역 ZIP을 먼저 적용하고 [한국어 출력 엔진 최신 정식 설치기](https://github.com/munument1/Fallout2-Korean-Text-Engine/releases/latest)를 실행하세요. 변경되는 원본 파일만 `korean_engine_backup_v2`에 자동 백업하며 같은 폴더에서 복구할 수 있습니다.

기준: **Nevada Extended 기존 번역 (정확한 원본 태그 미확정)**. 이번 변경은 기존 번역의 출력 방식 전환이며 원본 모드 버전 업그레이드가 아니다.

한국어 번역 데이터는 이 저장소에서, 출력 모듈·글꼴·설치 도구는 [Fallout2 Korean Text Engine](https://github.com/munument1/Fallout2-Korean-Text-Engine)에서 관리한다. 한국어로 수정한 sfall `ddraw.dll`을 덮어쓰는 방식에서 공식 sfall과 별도 한국어 모듈을 사용하는 방식으로 전환한다.

## 새로운 독립형 출력 엔진 (v1.2.1)

기존 번역문의 MSG ID와 본문은 그대로 유지합니다. 이제 게임별 프로필, 중국어 수정 EXE, 중국어 글꼴 DLL을 요구하지 않습니다. [최신 정식 설치기](https://github.com/munument1/Fallout2-Korean-Text-Engine/releases/latest)는 선택한 게임 폴더 안의 호환 Fallout 2 실행 파일을 내부 구조로 자동 인식합니다. 핵심 ABI 자체가 변경된 파일은 무리하게 패치하지 않습니다.

**설치 순서:** 번역 ZIP을 먼저 적용한 뒤 설치기를 실행하세요. 설치기가 한국어 언어 설정까지 자동으로 적용합니다.

전체 게임을 중복으로 백업하지 않습니다. EXE가 수정되므로 원상복구에 필요한 원본 파일 한 벌만 설치기가 보관합니다. 엔진은 최신 정식판이며, 게임별 긴 대화·전투·저장/불러오기를 전수 검증했다는 뜻은 아닙니다.

## 현재 상태

과거 공통 엔진의 시험 기록은 남아 있으나 새 독립형 엔진에서는 모드 동봉 Extended sfall을 유지한 채 짧은 기동 검증을 마쳤다. 전체 UI·장시간 플레이 또는 미래 sfall 버전의 검증을 뜻하지 않는다. 첫 실행 종료는 같은 설정 재실행에서 재현되지 않았으며 원인은 미확정이다.

기존 릴리스와 태그는 보존한다. 새 방식은 이 PR의 구성과 GitHub Actions에서 생성한 `korean-classic-data` 산출물을 기준으로 확인한다. 새 방식의 정식 릴리스가 발행됐다고 표시하지 않는다.

## 설치

1. 번역 버전과 일치하는 원본 모드를 준비합니다. 대상 위치는 **Nevada.exe와 NevadaHD.exe가 있는 폴더**입니다.
2. 번역 ZIP을 **먼저** 적용합니다. GitHub Actions의 korean-classic-data 산출물을 받거나 아래 빌드 명령으로 생성한 ZIP을 게임 폴더에 풀어 data/text/korean 등을 추가합니다. 번역 ZIP에는 게임 EXE, sfall DLL, DAT, INT가 들어가지 않습니다.
3. [최신 독립형 설치기](https://github.com/munument1/Fallout2-Korean-Text-Engine/releases/latest)의 Fallout2-Korean-Native-Setup.exe를 실행하고 게임 폴더만 지정합니다. 게임 종류나 --profile 선택, 중국어 CJK EXE 및 DLL은 필요 없습니다.
4. 설치가 끝나면 기존 게임 실행기로 실행합니다.
5. 한글 표시와 대화, 메뉴, 저장/불러오기를 확인하세요. 되돌릴 때는 같은 설치기의 복구 기능을 사용합니다.

**모드별 주의:** Nevada의 Extended sfall 4.3.0.2와 고해상도 설정을 보존하세요. 일반 sfall 4.5.1 DLL만 덮으면 고해상도 패치 충돌이 재현됩니다. 독립형 엔진은 기존 DLL은 유지하고 필요한 CRC만 설정에 추가합니다.

[자세한 안내](docs/NEW_ENGINE_KO.md) · [구형 설치 방식 기록](docs/LEGACY_INSTALLATION_KO.md)

## 번역 파일과 패키지

기존 MSG의 `{ID}{음성}{본문}` 구조와 번역을 유지한다. CP949 파일을 일괄 재변환하지 않는다. UTF-8 한국어 텍스트가 있으면 클래식 ZIP 생성 시에만 CP949로 엄격 변환한다. 표현할 수 없는 문자는 `?`로 바꾸지 않고 빌드를 중단한다. 원본 파일은 변경하지 않는다.

```shell
python tools/build_translation.py --output dist/korean-classic-data.zip
```

패키지에 포함한 파일 해시와 변환 목록은 `translation-manifest.json`에 들어간다. RPU의 mods 내 한국어 폴더는 배포 ZIP에서 data 아래에 합쳐 로드 순서 설정의 누락을 피한다. 게임 데이터의 언어를 중국어나 일본어로 바꾸지 않는다.

## 이전 배포 방식과 크레디트

[이전 안내와 크레디트](docs/LEGACY_INSTALLATION_KO.md)는 이력 확인용이다. 원본 게임·원본 모드 파일은 포함하지 않는다. 기존 번역자와 원본 모드·sfall·글꼴 제작자의 기여를 유지한다.
