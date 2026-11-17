"""Explicitly save anonymized experiment results; app itself does not persist inputs."""
import argparse
import json
from pathlib import Path
from agent import analyze, AnalysisError, markdown

parser=argparse.ArgumentParser()
parser.add_argument('--output',default='experiments')
args=parser.parse_args()
folder=Path(args.output)
folder.mkdir(parents=True,exist_ok=True)
cases=json.loads(Path('samples/cases.json').read_text())
results=[]
for case in cases:
    try:
        report,meta=analyze(case['title'],case['description'],case['goal'])
        record={'case':case['id'],**meta,'report':report.model_dump(),'human_review':'pending'}
        (folder/(case['id']+'.md')).write_text(markdown(case['title'],report,meta),encoding='utf-8')
        print(case['id'],'OK',meta['seconds'],'seconds')
    except AnalysisError as e:
        record={'case':case['id'],'status':'failed','error':str(e)}
        print(case['id'],'FAILED',str(e))
    results.append(record)
(folder/'results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
if any(r.get('status')=='failed' for r in results): raise SystemExit(1)
