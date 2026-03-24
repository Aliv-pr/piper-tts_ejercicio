import os
import subprocess

VOICES_DIR = os.path.expanduser("/home/ivan/espacio_trabajo/codigo/piper-tts/voices")
OUTPUT_DIR = os.path.expanduser("/home/ivan/espacio_trabajo/codigo/piper-tts/salidas")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Listar modelos
models = [f for f in os.listdir(VOICES_DIR) if f.endswith(".onnx")]

if not models:
    print("❌ No hay modelos en ~/voices/piper")
    exit()

print("📢 Modelos disponibles:")
for i, model in enumerate(models):
    print(f"[{i}] {model}")

# Elegir modelo
choice = int(input("Selecciona el número del modelo: "))
MODEL = os.path.join(VOICES_DIR, models[choice])

# Tipo de entrada
print("\n¿Cómo quieres ingresar el texto?")
print("[1] Escribir en terminal")
print("[2] Usar archivo .txt")

input_type = input("Opción: ")

if input_type == "1":
    print("Escribe el texto (Enter + Ctrl+D para terminar):")
    import sys
    TEXT = sys.stdin.read()
elif input_type == "2":
    file_path = input("Ruta del archivo: ")
    if not os.path.isfile(file_path):
        print("❌ Archivo no encontrado")
        exit()
    with open(file_path, "r", encoding="utf-8") as f:
        TEXT = f.read()
else:
    print("❌ Opción inválida")
    exit()

# Nombre de salida
title = input("Nombre del archivo de salida (sin .wav): ")
output_file = os.path.join(OUTPUT_DIR, f"{title}.wav")

# Ejecutar Piper
process = subprocess.Popen(
    ["piper", "--model", MODEL, "--output_file", output_file],
    stdin=subprocess.PIPE,
    text=True
)

process.communicate(TEXT)

print(f"\n✅ Audio generado en: {output_file}")

# Reproducir
play = input("¿Quieres reproducirlo ahora? (y/n): ")
if play.lower() == "y":
    subprocess.run(["ffplay", output_file])

