import json
import os
from pathlib import Path
import streamlit as st
from agent import analyze, AnalysisError, Report, markdown

st.set_page_config(page_title='업무 개선 분석 Assistant',page_icon='◈',layout='wide')
st.markdown('''<style>
.stApp{background:#f5f7fa} h1,h2,h3{color:#16352f} .block-container{padding-top:2.5rem;max-width:1250px}
[data-testid="stSidebar"]{background:#173e36} [data-testid="stSidebar"] *{color:#e8f1ec}
.stButton>button[kind="primary"]{background:#23735d;border:none}
</style>''',unsafe_allow_html=True)
cases=json.loads((Path(__file__).parent/'samples/cases.json').read_text())
with st.sidebar:
    st.markdown('## ◈ BUSINESS\n### Improvement Assistant')
    st.divider()
    st.markdown('**01  업무 요청 작성**\n\n02  AI 요구사항 분석\n\n03  보고서 검토')
    st.divider()
    st.caption('MAIN QUEST 02 · PoC\n\n업무 문제를 명확하게 정의하고, 더 나은 업무 방식을 검토합니다.')
    st.caption('모델: '+os.getenv('GEMINI_MODEL','gemini-2.5-flash'))
st.caption('WORKSPACE / 업무 개선 요청 분석')
st.title('업무의 불편함을, 개선의 출발점으로.')
st.write('현재 업무를 설명해 주세요. AI가 핵심 문제와 추가 확인 사항을 정리합니다.')
st.warning('가상 또는 익명화된 사례만 입력해 주세요. 실제 분석 시 입력이 Google Gemini API로 전송됩니다.')
left,right=st.columns([1,1.15],gap='large')
with left:
    st.subheader('01  업무 요청')
    selected=st.selectbox('샘플로 시작하기',['직접 입력']+[c['title'] for c in cases])
    case=next((c for c in cases if c['title']==selected),{'title':'','description':'','goal':''})
    with st.form('request'):
        title=st.text_input('업무명 *',value=case['title'],max_chars=120,key='title_'+selected)
        description=st.text_area('현재 업무 및 문제점 *',value=case['description'],height=200,max_chars=6000,key='description_'+selected,placeholder='누가, 어떤 도구로, 어떻게 일하며 무엇이 불편한가요?')
        goal=st.text_area('개선하고 싶은 내용',value=case['goal'],height=100,max_chars=2000,key='goal_'+selected)
        sent=st.form_submit_button('업무 요청 분석하기 →',type='primary',use_container_width=True)
    st.caption('입력은 별도 데이터베이스에 저장하지 않습니다. 결과는 현재 세션에서만 유지됩니다.')
    if st.button('입력·결과 초기화'):
        st.session_state.clear()
        st.rerun()
    if sent:
        st.session_state.pop('result',None)
        try:
            with st.spinner('요구사항 구조화 → 누락 정보 확인 → 보고서 작성 중…'):
                report,meta=analyze(title,description,goal)
            st.session_state.result=(title,report,meta)
        except AnalysisError as e: st.error(str(e))
with right:
    st.subheader('02  분석 보고서')
    if 'result' not in st.session_state:
        st.info('왼쪽에 업무 요청을 작성하면 분석 보고서가 여기에 표시됩니다.')
        st.markdown('#### 분석할 내용\n\n현재 업무와 주요 문제 · 개선 목적 · AS-IS / TO-BE · 비개발 대안을 포함한 개선 후보 · 추가 확인 질문')
        st.caption('확인된 사실에는 입력 근거를 표시하고, 제안과 미확인 사항을 별도로 정리합니다.')
    else:
        title,report,meta=st.session_state.result
        st.success(f"분석 완료 · {meta['seconds']}초 · {meta['model']}")
        st.caption('직전 분석 요청의 결과입니다. 입력을 수정했다면 다시 분석해 주세요.')
        output=markdown(title,report,meta)
        st.download_button('보고서 내려받기 (.md)',output,'analysis-report.md','text/markdown')
        st.markdown(output)
        st.warning('AI 초안입니다. 근거와 해석을 확인한 뒤 업무 검토에 활용하세요.')
