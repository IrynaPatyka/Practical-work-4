import mmap
import os

def task_2_string_mapping():
    file_name = "string_data.txt"
    my_string = "Привіт, це рядок для запису в пам'ять!"
    encoded_data = my_string.encode('utf-8')
    size = len(encoded_data)

    print(f"Початковий рядок: {my_string}")

    # Варіант 4.1 (Постійний файл на диску)
    with open(file_name, "wb+") as f:
        f.truncate(size)
        with mmap.mmap(f.fileno(), length=size, access=mmap.ACCESS_WRITE) as mm:
            # Запис рядка
            mm.write(encoded_data)
            mm.flush()
            mm.seek(0)
            result = mm.read(size).decode('utf-8')
            print(f"Зчитано з постійного файлу: {result}")

    # Варіант 4.2 (Непостійний/анонімний файл у RAM)
    with mmap.mmap(-1, 1024, access=mmap.ACCESS_WRITE) as amm:
        amm.write(encoded_data)
        amm.seek(0)
        result_anon = amm.read(size).decode('utf-8')
        print(f"Зчитано з анонімної пам'яті: {result_anon}")

if __name__ == "__main__":
    task_2_string_mapping()