# AI 업무 개선 요청 분석 Assistant

Main Quest 2 · Python / Streamlit / Gemini 기반 단일 업무 분석 Agent.

현업 업무 요청을 입력하면 AS-IS, 주요 문제, 개선 목적, TO-BE 제안, 비개발 대안을 포함한 개선 후보, 추가 질문(최대 10개)을 보고서로 생성합니다. 확인된 항목에는 원문 인용을 표시합니다. 자동 승인·실행은 하지 않습니다.

## Windows에서 실행

Python 3.11 이상을 권장합니다. 저장소 폴더에서 PowerShell로 실행하세요.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:GEMINI_API_KEY="본인의_API_Key"
$env:GEMINI_MODEL="gemini-2.5-flash"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

터미널에 표시된 `http://localhost:8501`을 엽니다. 가상 사례를 선택하거나 익명화된 업무를 입력하고 **업무 요청 분석하기**를 누르세요. 보고서는 Markdown으로 다운로드할 수 있습니다. 가상환경 활성화가 필요 없는 명령이므로 PowerShell Activate 실행 정책을 바꿀 필요가 없습니다.

macOS / Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
export GEMINI_API_KEY='your-key'
export GEMINI_MODEL='gemini-2.5-flash'
.venv/bin/python -m streamlit run app.py
```

모델 ID는 계정에서 이용 가능한 Gemini 모델로 변경하세요. ChatGPT 구독과 Gemini API 인증은 별개입니다. Key를 GitHub에 올리지 마세요. `.env.example`은 안내 파일이며 자동 로드하지 않습니다. API Key가 없으면 화면을 확인할 수 있지만 AI 분석은 실행되지 않습니다.

## 검증 및 과제 제출

```bash
python -m unittest discover -s tests -v
python evaluate.py --output experiments
```

두 번째 명령은 API Key가 필요하며 5개 가상 사례를 실제 모델로 분석하고 결과와 시간을 저장합니다. 입력이 외부 API로 전송됩니다. 웹앱은 입력을 영구 저장하지 않고 CLI는 실험 목적으로 명시적으로 결과 파일을 생성합니다.

- [문제 정의서](docs/problem-definition.md)
- [모델 선정 근거](docs/model-selection.md)
- [검증 결과·실험 기록 양식](docs/validation.md)
- [샘플 사례](samples/cases.json)
- [시연 절차](docs/demo.md)

**제출 상태:** 코드와 실행 문서는 준비했으며 실제 모델 실행·실제 업무 데이터 검증·효과 측정은 API Key 설정 후 수행해야 합니다. 기록하지 않은 성능 수치나 검증 실적은 주장하지 않습니다.

## 선택: 웹 배포

GitHub Pages는 Python 서버를 실행할 수 없습니다. Streamlit Community Cloud에서 이 저장소의 `app.py`를 지정하고 Secrets에 `GEMINI_API_KEY = "..."`를 설정하면 웹 배포할 수 있습니다. 별도 배포는 Main Quest 2 필수 조건이 아닙니다. 서버 운영자는 접근 통제와 API 사용량을 관리해야 합니다.

## 구조 및 보안

`app.py`: 입력·상태·보고서 UI / `agent.py`: 분석과 근거 검증 / `evaluate.py`: 실제 실험 / `tests/`: 자동 검사. DB, ERP 연결, 이력 저장, 멀티 Agent는 포함하지 않습니다.

기업 기밀·개인정보를 입력하지 마세요. 인용 검증은 문장 의미를 보장하지 않으므로 결과는 사람이 검토해야 합니다. 입력은 Gemini로 전송되며 사용 전 해당 API 데이터 처리 정책을 확인하세요.
