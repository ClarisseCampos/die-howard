# Projeto DieHoward


## 1. Sobre

**DieHoward** é o nome que dei ao meu núcleo de processamento de texto/áudio baseado em IA. 

A ideia do projeto é transformar livros e textos em uma experiência de áudio confortável, funcionando como sistema local de conversão de texto em fala. Meu objetivo é evitar depender de APIs pagas ou serviços externos sempre que possível. Quero utilizar **modelos locais e software open source**, principalmente porque pretendo processar textos longos.
O projeto ainda está em desenvolvimento, então algumas decisões de arquitetura podem mudar.

### Origem do Nome:
O nome veio em homenagem a um monólogo do filme "Pearl" (2022) onde a atriz Mia Goth interpreta magistralmente um monólogo de mais de oito minutos, em que simula uma conversa dissecante com seu marido Howard.

> "Howard... Eu te odeio tanto por me deixar aqui, às vezes espero que você morra. Sinto muito. Sinto-me péssimo admitindo isso, mas é a verdade. "

Este texto serviu de base para rastrear a evolução do projeto. Afinal ele expôs os principais desafios: o ritmo, a entonação e a pronúncia de palavras estrangeiras, como 'Howard'. Tal qual a Pearl espera que Howard morra, eu espero que os problema da pronúncia também morra, por isso "DieHoward".

## 2. Objetivo

O objetivo é criar um sistema que consiga:

1. Receber um livro ou texto.
2. Processar o conteúdo.
3. Identificar e organizar os trechos.
4. Transformar o texto em fala.
5. Gerar arquivos de áudio.
6. Permitir que eu escute o resultado confortavelmente, inclusive durante deslocamentos, como no ônibus.

No futuro, quero que o sistema seja mais inteligente do que simplesmente mandar o texto inteiro para um TTS.

Por exemplo, ele poderia entender melhor:

* capítulos;
* parágrafos;
* diálogos;
* nomes próprios;
* citações;
* diferentes idiomas;
* pontuação;
* pausas;
* ritmo;
* entonação.

## 3. TTS atual

Atualmente estou usando **Piper TTS**.

Estou utilizando uma voz em português:

`pt_BR-faber-medium.onnx`

Tenho chamado o Piper a partir de Python utilizando `subprocess`.

Um exemplo da ideia do código é:

```python
subprocess.run([
    "piper",
    "--model", "pt_BR-faber-medium.onnx",
    "--output_file", "output.wav",
    "--length_scale", "1.60"
])
```

Eu aumentei o `length_scale` porque a leitura padrão estava rápida demais.

O resultado do Piper é mais natural do que uma voz extremamente robótica, mas ainda existem problemas importantes.

## 4. Problemas que já encontrei

### Velocidade

A leitura padrão estava rápida demais.

Consegui diminuir a velocidade utilizando `--length_scale`, mas quero encontrar uma maneira melhor de controlar o ritmo.

### Ritmo

O maior problema atualmente é que a voz não possui um ritmo muito natural.

Ela consegue pronunciar o texto, mas às vezes parece estar simplesmente percorrendo as palavras em sequência.

Quero melhorar:

* pausas;
* duração das pausas;
* velocidade por trecho;
* ritmo de frases;
* ênfase;
* pontuação;
* diálogos.

### Nomes em inglês

Também percebi dificuldades quando um texto em português contém nomes ou palavras em inglês.

Por exemplo, um personagem com nome inglês pode ser pronunciado de uma maneira estranha pelo modelo português.

Quero encontrar uma forma de lidar com isso sem necessariamente precisar trocar toda a voz.

## 5. Filosofia do projeto

Quero que o DieHoward seja principalmente:

* local;
* barato;
* open source quando possível;
* modular;
* extensível;
* capaz de trabalhar com textos longos;
* relativamente leve;
* independente de APIs proprietárias;
* capaz de evoluir para algo mais inteligente.

Não quero simplesmente criar um script que executa:

`texto -> Piper -> MP3`

Quero eventualmente construir uma arquitetura em que diferentes componentes tenham responsabilidades diferentes.

Por exemplo:

```text
Livro
  ↓
Parser
  ↓
Analisador de texto
  ↓
Normalização
  ↓
Detecção de idioma
  ↓
Tratamento de nomes/termos
  ↓
Segmentação
  ↓
Controle de ritmo
  ↓
TTS
  ↓
Pós-processamento de áudio
  ↓
Arquivo final
```

Isso é apenas uma ideia inicial, não uma arquitetura definitiva.


## 8. Hardware e ambiente

Meu ambiente principal é Linux Mint.

Tenho interesse em executar o máximo possível localmente.

Meu computador utiliza um:

* AMD Ryzen 5 3400G
* Radeon Vega Graphics

Também já tive/tenho uma NVIDIA GTX 960 disponível em meu ambiente, portanto considere que **GPU pode ou não estar disponível dependendo da configuração atual**.

Não presuma que tenho uma GPU moderna com grande quantidade de VRAM.

Sempre considere o custo computacional das soluções.

## 9. Direção futura

No futuro, gostaria que o DieHoward pudesse evoluir de um simples TTS para um sistema de processamento de livros.

Por exemplo:

```text
              ┌──────────────┐
              │    Livro     │
              └──────┬───────┘
                     ↓
             ┌───────────────┐
             │    Parser     │
             └───────┬───────┘
                     ↓
        ┌─────────────────────────┐
        │ Análise / Normalização  │
        └────────────┬────────────┘
                     ↓
          ┌─────────────────────┐
          │ Segmentação textual │
          └──────────┬──────────┘
                     ↓
        ┌────────────────────────┐
        │ Preparação para TTS    │
        └────────────┬───────────┘
                     ↓
              ┌───────────┐
              │    TTS    │
              └─────┬─────┘
                    ↓
          ┌──────────────────┐
          │ Pós-processamento│
          └────────┬─────────┘
                   ↓
             ┌───────────┐
             │   Áudio   │
             └───────────┘
```

Isso pode posteriormente incluir recursos como:

* múltiplas vozes;
* vozes diferentes para personagens;
* detecção de diálogos;
* controle automático de velocidade;
* pronúncia personalizada;
* dicionário de nomes;
* suporte multilíngue;
* geração de capítulos;
* metadados;
* conversão para formatos como WAV/MP3/Opus;
* normalização de volume;
* processamento de silêncio;
* retomada de processamento caso o programa seja interrompido.

Mas não quero implementar tudo isso de uma vez.

## 10. Como quero que você me ajude

Quero trabalhar **incrementalmente**.

Se eu perguntar:

> "Como faço X?"

Primeiro explique o conceito e depois mostre uma implementação adequada ao estágio atual do projeto.

Se houver uma solução simples e outra sofisticada, apresente primeiro a simples e explique quando faria sentido migrar para a sofisticada.

Se você perceber que estou tentando resolver um problema no nível errado da arquitetura, diga isso explicitamente.

Também quero que você questione decisões ruins em vez de simplesmente concordar comigo.

Por exemplo:

> "Essa abordagem funciona, mas eu não recomendo porque..."

Isso é desejável.

