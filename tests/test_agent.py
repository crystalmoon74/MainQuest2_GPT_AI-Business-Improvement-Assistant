import unittest
from unittest.mock import patch
import json
import urllib.error
from agent import analyze, check_report, AnalysisError, validate_input

DATA={'purpose':'미확인','as_is':[{'text':'이메일 접수','evidence':'이메일로 접수'}], 'problems':[{'text':'승인 지연','evidence':'없는 근거'}], 'goals':[], 'to_be':[], 'options':[], 'questions':['처리 빈도는?','처리 빈도는?'],'unknowns':[]}
class AgentTests(unittest.TestCase):
    def test_required_input(self):
        with self.assertRaises(AnalysisError): validate_input(' ','내용')
    def test_length_limit(self):
        with self.assertRaises(AnalysisError): validate_input('업무','x'*6001)
    def test_evidence_filter_and_duplicate_questions(self):
        r=check_report(DATA,'요청을 이메일로 접수합니다.')
        self.assertEqual(len(r.as_is),1)
        self.assertEqual(r.problems,[])
        self.assertEqual(len(r.questions),1)
        self.assertTrue(r.unknowns)
    def test_question_limit(self):
        with self.assertRaises(ValueError): check_report({**DATA,'questions':['질문']*11},'')
    @patch('urllib.request.urlopen')
    def test_live_pipeline_contract(self,call):
        call.return_value.__enter__.return_value.read.return_value=json.dumps({'candidates':[{'finishReason':'STOP','content':{'parts':[{'text':json.dumps(DATA)}]}}]}).encode()
        report,meta=analyze('업무','이메일로 접수',key='test-key')
        self.assertEqual(meta['mode'],'live')
        self.assertEqual(len(report.as_is),1)
    @patch('urllib.request.urlopen',side_effect=urllib.error.HTTPError('url',429,'limit',{},None))
    def test_quota_message(self,call):
        with self.assertRaisesRegex(AnalysisError,'호출 한도'): analyze('업무','설명',key='test-key')
if __name__=='__main__': unittest.main()
