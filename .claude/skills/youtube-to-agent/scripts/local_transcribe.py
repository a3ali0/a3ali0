#!/usr/bin/env python3
"""Local transcript for videos with no caption track. Nothing leaves your machine.

usage:
  local_transcribe.py <audio-or-video-file> [--model small] [--out notes/transcript.txt]

Install: pip install faster-whisper   (first run downloads the model, ~500 MB for small)
Apple Silicon alternative: uvx --from mlx-whisper mlx_whisper "audio.wav" --model mlx-community/whisper-large-v3-turbo
"""
import argparse
import sys

try:
    from faster_whisper import WhisperModel
except ImportError:
    sys.exit("faster-whisper is not installed. Run: pip install faster-whisper")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", help="audio or video file (anything ffmpeg can decode)")
    ap.add_argument("--model", default="small")
    ap.add_argument("--out", default=None, help="write here instead of stdout")
    args = ap.parse_args()

    model = WhisperModel(args.model, device="auto", compute_type="int8")
    segments, _ = model.transcribe(args.source)
    out = open(args.out, "w") if args.out else sys.stdout
    try:
        for s in segments:
            print(f"[{s.start:.1f}-{s.end:.1f}] {s.text.strip()}", file=out, flush=True)
    finally:
        if args.out:
            out.close()


if __name__ == "__main__":
    main()
