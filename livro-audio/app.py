from pathlib import Path
import subprocess

texto = Path("texts/teste.txt").read_text(encoding="utf-8")

subprocess.run(
    [
        "piper",
        "--model",
        "models/pt_BR-faber-medium.onnx",
        "--output_file",
        "audios/teste.wav",
    ],
    input=texto.encode("utf-8"),
    check=True,
)
