import os, json, glob, asyncio, sys
import edge_tts
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO = os.path.join(ROOT, "audio")
VOICE = "en-GB-SoniaNeural"   # teacher "Miss Vega"
def collect():
    jobs=[]
    for lv in ["ket","pet","b2f","c1a"]:
        for f in sorted(glob.glob(os.path.join(ROOT,"content",lv,"unit-*.json"))):
            u=json.load(open(f,encoding="utf-8"))
            for a in u.get("activities",[]):
                if a.get("type")=="listening" and a.get("audio") and a["data"].get("script"):
                    out=os.path.join(AUDIO, a["audio"].replace("/",os.sep))
                    jobs.append((out, a["data"]["script"]))
    return jobs
async def one(out, text):
    os.makedirs(os.path.dirname(out), exist_ok=True)
    c=edge_tts.Communicate(text, VOICE, rate="-8%")
    await c.save(out)
async def main():
    jobs=collect()
    force = "--force" in sys.argv
    todo=[(o,t) for (o,t) in jobs if force or not os.path.exists(o)]
    print(f"total listening: {len(jobs)} · to generate: {len(todo)}")
    ok=0
    for out,text in todo:
        try:
            await one(out,text); ok+=1
            print("OK", os.path.relpath(out,AUDIO))
        except Exception as e:
            print("ERR", os.path.relpath(out,AUDIO), str(e)[:80])
    print(f"DONE generated {ok}/{len(todo)}")
asyncio.run(main())
