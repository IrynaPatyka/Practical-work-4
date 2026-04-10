import mmap
import os

def main():
    file_name = "data_notepad.txt"
    mas = [1, 32, 45, 11, -5, 0, 78, 52]
    
    data_string = " ".join(map(str, mas)) + " "
    binary_data = data_string.encode('utf-8')
    file_size = len(binary_data)

    print(f"Масив для запису: {data_string}")

    with open(file_name, "wb+") as f:
        f.write(binary_data)
        f.flush()

        with mmap.mmap(f.fileno(), length=0, access=mmap.ACCESS_WRITE) as mm:
            print("\nФайл відображено в пам'ять. Тепер його можна відкрити Блокнотом.")
            
            mm.seek(0)
            content = mm.read().decode('utf-8')
            
            input_mas = [int(x) for x in content.split() if x.strip()]
            
            print("Дані, зчитані з пам'яті:")
            print(input_mas)

    print(f"\nГотово! Перевірте файл {file_name} у Блокноті.")

if __name__ == "__main__":
    main()