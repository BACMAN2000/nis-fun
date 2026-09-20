from pathlib import Path
import subprocess
w=Path('work'); out=Path('outputs')
def run(args): subprocess.run(['ffmpeg','-y','-v','error',*args],check=True)
# Assemble without burned-in text, ready for the replacement closing performance.
run(['-f','concat','-safe','0','-i',str(w/'complete-concat.txt'),'-an','-t','23.5','-c:v','libx264','-crf','18','-preset','fast',str(w/'closing-prefix.mp4')])
