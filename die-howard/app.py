from pathlib import Path
import subprocess
import sys
import time

from rich.console import Console

console = Console()

# Caminho para o executável do Piper dentro da própria venv
PIPER = Path(sys.executable).parent / "piper"

# Ler texto
console.print("[cyan]📖 Lendo arquivo...[/cyan]")
texto = Path("texts/teste.txt").read_text(encoding="utf-8")
console.print(f"[green]✓[/green] Texto carregado ({len(texto)} caracteres)")

inicio = time.perf_counter()

# Gerar áudio
with console.status("[bold green]🎙 Gerando áudio...", spinner="dots"):
    subprocess.run(
        [
            str(PIPER),
            "--model",
            "models/pt_BR-faber-medium.onnx",
            "--output_file",
            "audios/teste.wav",
            "--length_scale",
            "1.60",
        ],
        input=texto.encode("utf-8"),
        check=True,
    )

fim = time.perf_counter()

console.print(f"[green]✓ Áudio salvo em:[/green] audios/teste.wav")
console.print(f"[bold]⏱ Tempo:[/bold] {fim - inicio:.2f} segundos")