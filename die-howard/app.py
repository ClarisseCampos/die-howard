from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import wave
from rich.console import Console
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

console = Console()

BASE_DIR = Path(__file__).resolve().parent
TEXT_FILE = BASE_DIR / "texts" / "teste.txt"
MODEL_FILE = BASE_DIR / "models" / "pt_BR-faber-medium.onnx"
OUTPUT_DIR = BASE_DIR / "audios"
TEMP_DIR = BASE_DIR / "temp"
OUTPUT_FILE = OUTPUT_DIR / "teste_final.wav"

def encontrar_executavel_piper() -> Path | None:
    local_venv = Path(sys.executable).parent / "piper"
    return local_venv if local_venv.exists() else Path(shutil.which("piper") or "")

PIPER_BIN = encontrar_executavel_piper()

def normalizar_texto(texto: str) -> str:
    substituicoes = {"Shakespeare": "Chêkispir", "Steve": "Istív", "Facebook": "Feicebuk", "Python": "Paíton"}
    for original, nova in substituicoes.items():
        texto = texto.replace(original, nova)
    return texto

def segmentar_texto(texto: str) -> list[str]:
    texto = re.sub(r'\s+', ' ', texto).strip()
    frases_cruas = re.split(r'(?<=[.!?])\s+', texto)
    return [f.strip() for f in frases_cruas if len(f.strip()) > 1]

def gerar_audio_piper(texto: str, arquivo_saida: Path):
    subprocess.run(
        [
            str(PIPER_BIN),
            "--model", str(MODEL_FILE),
            "--output_file", str(arquivo_saida),
            "--length_scale", "1.05",
        ],
        input=texto.encode("utf-8"),
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def concatenar_audios_com_silencio(arquivos_wav: list[Path], arquivo_final: Path, tempo_silencio_s: float = 0.4):
    if not arquivos_wav:
        return

    with wave.open(str(arquivos_wav[0]), 'rb') as w_ref:
        params = w_ref.getparams()

    frames_silencio = int(params.framerate * tempo_silencio_s)
    bytes_silencio = b'\x00' * (frames_silencio * params.nchannels * params.sampwidth)

    with wave.open(str(arquivo_final), 'wb') as w_out:
        w_out.setparams(params)
        
        for i, arq in enumerate(arquivos_wav):
            with wave.open(str(arq), 'rb') as w_in:
                w_out.writeframes(w_in.readframes(w_in.getnframes()))
            
            if i < len(arquivos_wav) - 1:
                w_out.writeframes(bytes_silencio)

def main():
    if PIPER_BIN is None or not PIPER_BIN.exists():
        console.print("[bold red]Erro:[/bold red] Executável do Piper não encontrado.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    TEMP_DIR.mkdir(parents=True, exist_ok=True)

    console.print("[cyan]📖 Lendo e processando arquivo...[/cyan]")
    texto_original = TEXT_FILE.read_text(encoding="utf-8")
    
    texto_tratado = normalizar_texto(texto_original)
    frases = segmentar_texto(texto_tratado)
    
    console.print(f"[green]✓[/green] Texto dividido em {len(frases)} frases.")

    inicio = time.perf_counter()
    arquivos_gerados = []

    # Barra de carregamento customizada do Rich
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console,
    ) as progress:
        
        tarefa = progress.add_task("[bold green]🎙 Sintetizando áudio...", total=len(frases))

        for i, frase in enumerate(frases):
            caminho_temp = TEMP_DIR / f"chunk_{i:04d}.wav"
            gerar_audio_piper(frase, caminho_temp)
            arquivos_gerados.append(caminho_temp)
            
            # Avança 1 passo na barra de progresso
            progress.update(tarefa, advance=1)

    console.print("[bold blue]🔧 Montando arquivo final com pausas...[/bold blue]")
    concatenar_audios_com_silencio(arquivos_gerados, OUTPUT_FILE, tempo_silencio_s=0.5)

    # Limpeza dos arquivos temporários
    for arq in arquivos_gerados:
        arq.unlink()

    fim = time.perf_counter()
    console.print(f"[green]✓ Áudio final salvo em:[/green] {OUTPUT_FILE}")
    console.print(f"[bold]⏱ Tempo de processamento:[/bold] {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    main()