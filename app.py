import io
import json
import re
import time
import wave
from pathlib import Path

from piper.voice import PiperVoice
from rich.console import Console
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
)

console = Console()

# ==========================================
# CONFIGURAÇÕES DE CAMINHOS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
TEXT_FILE = BASE_DIR / "texts" / "teste.txt"
LEXICON_FILE = BASE_DIR / "config" / "lexicon.json"
IPA_FILE = BASE_DIR / "config" / "ipa_rules.json"

OUTPUT_DIR = BASE_DIR / "audios"
OUTPUT_FILE = OUTPUT_DIR / "teste_piper_direto.wav"

MODEL_PATH = BASE_DIR / "models" / "pt_BR-faber-medium.onnx"
CONFIG_PATH = BASE_DIR / "models" / "pt_BR-faber-medium.onnx.json"

# Pausa entre frases (em segundos)
PAUSA_SEGUNDOS = 0.4


# ==========================================
# FUNÇÕES AUXILIARES
# ==========================================
def carregar_json(caminho: Path) -> dict:
    """Carrega arquivos JSON simples ou categorizados dinamicamente."""
    if not caminho.exists():
        return {}
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        # Se for um JSON categorizado (como o lexicon.json), achata as categorias
        if any(isinstance(v, dict) for v in dados.values()):
            substituicoes = {}
            for categoria in dados.values():
                substituicoes.update(categoria)
            return substituicoes
        return dados
    except Exception as e:
        console.print(f"[red]⚠️ Erro ao ler {caminho.name}:[/red] {e}")
        return {}

def aplicar_normalizacao(texto: str, regras: dict) -> str:
    """Aplica as correções apenas em palavras inteiras isoladas."""
    for original, pronuncia in regras.items():
        padrao = re.compile(rf'\b{re.escape(original)}\b', flags=re.IGNORECASE)
        texto = padrao.sub(pronuncia, texto)
    return texto

def segmentar_texto(texto: str) -> list[str]:
    """Divide o texto em frases para permitir pausas naturais e barra de progresso."""
    texto = re.sub(r'\s+', ' ', texto).strip()
    frases_cruas = re.split(r'(?<=[.!?])\s+', texto)
    return [f.strip() for f in frases_cruas if len(f.strip()) > 1]


def extrair_pcm_frase(voice: PiperVoice, frase: str) -> bytes:
    """Sintetiza uma frase via synthesize_wav em memória e extrai apenas os bytes de som."""
    buffer = io.BytesIO()
    with wave.open(buffer, "wb") as wav_temp:
        voice.synthesize_wav(frase, wav_temp)
    
    buffer.seek(0)
    with wave.open(buffer, "rb") as wav_leitura:
        return wav_leitura.readframes(wav_leitura.getnframes())


# ==========================================
# FLUXO PRINCIPAL
# ==========================================
def main():
    console.rule("[bold cyan]DieHoward TTS - Pipeline Ativo")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not TEXT_FILE.exists() or not MODEL_PATH.exists():
        console.print("[bold red]❌ Erro:[/bold red] Arquivo de texto ou modelo ONNX não encontrado.")
        return

    # 1. Carregamento do Léxico, IPA e Texto
    ipa_rules = carregar_json(IPA_FILE)
    lexicon = carregar_json(LEXICON_FILE)
    texto_bruto = TEXT_FILE.read_text(encoding="utf-8")
    
    # Aplica primeiro o IPA (mais específico) e depois o Léxico comum
    texto_tratado = aplicar_normalizacao(texto_bruto, ipa_rules)
    texto_tratado = aplicar_normalizacao(texto_tratado, lexicon)
    
    frases = segmentar_texto(texto_tratado)

    if not frases:
        console.print("[bold red]❌ Erro:[/bold red] O arquivo de texto está vazio.")
        return

    console.print(f"[green]✓[/green] Regras aplicadas (IPA: {len(ipa_rules)} | Léxico: {len(lexicon)}).")
    console.print(f"[green]✓[/green] Texto processado e dividido em {len(frases)} frases.")

    # 2. Inicialização do Modelo Neural
    console.print("[yellow]⚡ Carregando modelo ONNX na RAM...[/yellow]")
    voice = PiperVoice.load(str(MODEL_PATH), config_path=str(CONFIG_PATH))
    sample_rate = voice.config.sample_rate

    # 3. Preparação do Silêncio de Pausa
    frames_silencio = int(sample_rate * PAUSA_SEGUNDOS)
    bytes_silencio = b'\x00' * (frames_silencio * 2)

    console.print(f"[cyan]🎙 Sintetizando áudio em memória...[/cyan]")
    inicio = time.perf_counter()

    # 4. Gravação em Pipeline no WAV Final
    with wave.open(str(OUTPUT_FILE), "wb") as wav_final:
        wav_final.setnchannels(1)           # Mono
        wav_final.setsampwidth(2)           # 16-bit
        wav_final.setframerate(sample_rate) # Rate do modelo

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            TimeRemainingColumn(),
            console=console,
        ) as progress:
            
            tarefa = progress.add_task("[bold green]🎙 Sintetizando...", total=len(frases))

            for i, frase in enumerate(frases):
                pcm_bytes = extrair_pcm_frase(voice, frase)
                wav_final.writeframes(pcm_bytes)
                
                # Injeta a pausa entre as frases
                if i < len(frases) - 1:
                    wav_final.writeframes(bytes_silencio)
                
                progress.update(tarefa, advance=1)

    fim = time.perf_counter()

    console.rule("[bold cyan]Concluído")
    console.print(f"[bold green]▶ Áudio salvo em:[/bold green] {OUTPUT_FILE}")
    console.print(f"[bold]⏱ Tempo total de síntese:[/bold] {fim - inicio:.2f} segundos")

if __name__ == "__main__":
    main()