import sys
import numpy as np
import simpleaudio as sa
from colorama import init, Back

# Инициализация colorama
init(autoreset=True)

def play_sound(frequency, duration):
    # Генерация звуковой волны
    sample_rate = 44100  # Частота дискретизации
    t = np.linspace(0, duration, int(sample_rate * duration), False)  # Временные точки
    wave = 0.5 * np.sin(2 * np.pi * frequency * t)  # Синусоидальная волна
    audio = wave * 32767  # Приведение к диапазону int16
    audio = audio.astype(np.int16)  # Преобразование в int16

    # Воспроизведение звука
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
    play_obj.wait_done()  # Ожидание завершения воспроизведения

def print_color_strip(bit):
    if bit == '0':
        print(Back.BLUE + ' ' * 10)  # Синяя полоска
        play_sound(440, 0.1)  # Звук для бита 0 (частота 440 Гц)
    elif bit == '1':
        print(Back.YELLOW + ' ' * 10)  # Желтая полоска
        play_sound(550, 0.1)  # Звук для бита 1 (частота 550 Гц)

def read_binary_file(file_path):
    try:
        with open(file_path, 'rb') as file:
            byte = file.read(1)
            while byte:
                # Преобразуем байт в двоичную строку
                bits = f"{int.from_bytes(byte, 'big'):08b}"
                for bit in bits:
                    print_color_strip(bit)
                byte = file.read(1)
    except FileNotFoundError:
        print("Файл не найден. Пожалуйста, проверьте путь к файлу.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python script.py <путь_к_файлу>")
    else:
        file_path = sys.argv[1]
        read_binary_file(file_path)
