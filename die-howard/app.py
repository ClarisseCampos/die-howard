from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from rich.console import Console

console = Console()

# 1. Configuração de Caminhos
BASE_DIR = Path(__file__).resolve().parent

TEXT_FILE = BASE_DIR / "texts" / "teste.txt"
MODEL_FILE = BASE_DIR / "models" / "pt_BR-faber-medium.onnx"
OUTPUT_DIR = BASE_DIR / "audios"
OUTPUT_FILE = OUTPUT_DIR / "teste.wav"

def encontrar_executavel_piper() -> Path | None:
    local_venv_piper = Path(sys.executable).parent / "piper"
    if local_venv_piper.exists():
        return local_venv_piper

    piper_in_path = shutil.which("piper")
    if piper_in_path:
        return Path(piper_in_path)

    return None

PIPER_BIN = encontrar_executavel_piper()

# Dicionário de Pronúncia
REPLICACOES_PRONUNCIA = {
    "Shakespeare": "Chêkispir",
    "Steve": "Istív",
    "Facebook": "Feicebuk",
    "Python": "Paíton",
}

def normalizar_texto(texto: str) -> str:
    """Substitui termos estrangeiros pela forma de leitura em PT-BR."""
    texto_normalizado = texto
    for palavra_original, pronuncia_fonetica in REPLICACOES_PRONUNCIA.items():
        texto_normalizado = texto_normalizado.replace(palavra_original, pronuncia_fonetica)
    return texto_normalizado

def ajustar_ritmo_e_pausas(texto: str) -> str:
    """
    Injeta marcas de pausa sintética no texto para melhorar o ritmo sem 
    precisar esticar a voz artificialmente com length_scale.
    """
    # 1. Substitui quebras de linha/parágrafos duplos por uma pausa longa (...)
    texto_processado = re.sub(r'\n\s*\n', '... \n', texto)
    
    # 2. Garante um pequeno espaço de pausa após pontos finais e pontos e vírgula
    texto_processado = re.sub(r'(\.|\;)\s*', r'\1 ... ', texto_processado)

    # 3. Limpa múltiplos pontos/espaços repetidos acidentalmente
    texto_processado = re.sub(r'\.{4,}', '...', texto_processado)
    
    return texto_processado

def main():
    if PIPER_BIN is None or not PIPER_BIN.exists():
        console.print("[bold red]Erro:[/bold red] Executável do Piper não foi encontrado.")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not TEXT_FILE.exists():
        console.print(f"[red]Erro:[/red] Arquivo de texto não encontrado em: {TEXT_FILE}")
        return

    console.print("[cyan]📖 Lendo e processando arquivo...[/cyan]")
    texto_original = TEXT_FILE.read_text(encoding="utf-8")
    
    # Etapas da Pipeline do DieHoward
    texto_tratado = normalizar_texto(texto_original)
    texto_com_pausas = ajustar_ritmo_e_pausas(texto_tratado)
    
    console.print(f"[green]✓[/green] Texto preparado para o TTS ({len(texto_com_pausas)} caracteres)")

    inicio = time.perf_counter()

    with console.status("[bold green]🎙 Gerando áudio...", spinner="dots"):
        subprocess.run(
            [
                str(PIPER_BIN),
                "--model", str(MODEL_FILE),
                "--output_file", str(OUTPUT_FILE),
                "--length_scale", "1.5", # Velocidade natural (próxima da humana)
            ],
            input=texto_com_pausas.encode("utf-8"),
            check=True,
        )

    fim = time.perf_counter()

    console.print(f"[green]✓ Áudio salvo em:[/green] {OUTPUT_FILE}")
    console.print(f"[bold]⏱ Tempo de processamento:[/bold] {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    main()