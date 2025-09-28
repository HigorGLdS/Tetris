import numpy as np
import wave
import os

os.makedirs("sons", exist_ok=True)


def gerar_seno(frequencia, duracao, volume=0.5, samplerate=44100):
    t = np.linspace(0, duracao, int(samplerate * duracao), False)
    onda = np.sin(frequencia * t * 2 * np.pi)
    audio = (onda * volume * 32767).astype(np.int16)
    return audio


def salvar_wav(nome, audio, samplerate=44100):
    with wave.open(nome, "w") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(samplerate)
        f.writeframes(audio.tobytes())

# Música de fundo (loop simples)


audio = np.concatenate([
    gerar_seno(440, 0.2),
    gerar_seno(660, 0.2),
    gerar_seno(550, 0.2),
    gerar_seno(880, 0.2)
] * 20)
salvar_wav("sons/musica.wav", audio)  # pygame lê .ogg ou .wav

# Som de linha removida
efeito = np.concatenate([
    gerar_seno(800, 0.1),
    gerar_seno(600, 0.1),
    gerar_seno(400, 0.1),
])
salvar_wav("sons/linha.wav", efeito)

print("✅ Sons gerados em /sons")
