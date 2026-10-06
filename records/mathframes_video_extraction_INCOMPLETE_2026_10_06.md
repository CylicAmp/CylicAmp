# mathframes video extraction — INCOMPLETE

Commands supplied by the owner, 2026-10-06, run in a different session
(paths under `/workspace/...`, which does not exist in this container).
No output from any of these commands has been supplied. Saved as received.
Nothing here is checked or verified.

## Commands, in the order sent

```
mkdir -p /workspace/artifacts/mathframes/hi && for t in 24 28 32 36 48 56 64 72 80 88 96 104 112 120 128 136 144 152; do ffmpeg -y -i /workspace/attachments/1000035063.mp4 -ss $t -frames:v 1 -update 1 /workspace/artifacts/mathframes/hi/t$(printf '%03d' $t).jpg >/dev/null 2>&1; done && ls -la /workspace/artifacts/mathframes/hi
```

```
which whisper whisper.cpp ffmpeg python3; python3 -c "import whisper" 2>/dev/null || echo no-whisper; mkdir -p /workspace/artifacts/mathframes/sheet && ffmpeg -y -i /workspace/attachments/1000035063.mp4 -vf "fps=1/4,scale=180:-1,tile=6x9" -frames:v 1 /workspace/artifacts/mathframes/sheet/contact.jpg 2>/dev/null; ls -la /workspace/artifacts/mathframes/sheet
```

```
which tesseract; tesseract --version 2>/dev/null | head -2
```

```
python3 << 'PY'
from PIL import Image
im = Image.open("/workspace/artifacts/mathframes/hi/t136.jpg")
w,h = im.size
# table body roughly
bands = {
 "head": (0, 0, w, 280),
 "r1": (0, 250, w, 520),
 "r2": (0, 480, w, 780),
 "r3": (0, 740, w, 1040),
 "foot": (0, 1000, w, h),
}
for k,(a,b,c,d) in bands.items():
    im.crop((a,b,c,d)).save(f"/workspace/artifacts/mathframes/hi/oi_{k}.jpg", quality=92)
print("ok", w, h)
PY
for t in 100 108 124 132 140 148; do ffmpeg -y -i /workspace/attachments/1000035063.mp4 -ss $t -frames:v 1 -update 1 /workspace/artifacts/mathframes/hi/t$(printf '%03d' $t).jpg >/dev/null 2>&1; done
```

(The fourth command was sent twice, identically.)

## What's missing to complete this

- The source video, `1000035063.mp4`, or the extracted frames / contact
  sheet as image files, attached directly to a message here.
- Any printed output from the four commands above.
