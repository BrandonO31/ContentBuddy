import whisper
import subprocess
from pathlib import Path

def convert_to_wav(input_path: Path) -> Path:
    output_path = input_path.with_suffix(".wav")
    command = [
        "ffmpeg",
        "-y",  
        "-i", str(input_path),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(output_path)
    ]
    subprocess.run(command, check=True)
    return output_path

def transcribe_audio(audio_path: Path, model_size: str) -> str:
    model = whisper.load_model(model_size)
    result = model.transcribe(str(audio_path), language="en", fp16=False)
    return result["text"]

def save_transcript(text: str, source_file: Path):
    transcripts_dir = Path("transcripts")
    transcripts_dir.mkdir(exist_ok=True)
    txt_path = transcripts_dir / (source_file.stem + ".txt")
    txt_path.write_text(text, encoding="utf-8")
    print(f"Transcript saved to {txt_path}")

def transcribe_full_pipeline(video_file: Path, model_size: str = "small"):
    try:
        print(f"Converting {video_file} to WAV...")
        wav_file = convert_to_wav(video_file)

        print(f"Transcribing {wav_file}...")
        transcript = transcribe_audio(wav_file, model_size=model_size)

        print("Saving transcript...")
        save_transcript(transcript, video_file)

    except Exception as e:
        print(f"[Transcription Error] {e}")


def main():
    # Replace this with your actual filename
    video_file = Path(r"C:\Users\brand\Videos\RoadTo2000Eloep40.mkv")
    wav_file = convert_to_wav(video_file)
    transcript = transcribe_audio(wav_file)
    save_transcript(transcript, video_file)

if __name__ == "__main__":
    main()

