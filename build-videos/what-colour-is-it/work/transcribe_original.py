import sys,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'asr-readable'))
from faster_whisper import WhisperModel
model_path='C:/Users/User/.cache/huggingface/hub/models--mobiuslabsgmbh--faster-whisper-large-v3-turbo/snapshots/0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf'
model=WhisperModel(model_path,device='cpu',compute_type='int8',cpu_threads=6)
for arg in sys.argv[1:]:
    p=Path(arg)
    segments,info=model.transcribe(str(p),language='en',word_timestamps=True,beam_size=5,vad_filter=False)
    data=[{'start':s.start,'end':s.end,'text':s.text,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in s.words]} for s in segments]
    p.with_suffix('.transcript.json').write_text(json.dumps(data,indent=2),encoding='utf-8')
    print(json.dumps({'file':str(p),'segments':data}),flush=True)


