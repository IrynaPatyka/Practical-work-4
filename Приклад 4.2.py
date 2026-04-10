import mmap
import struct

def main():
    mas = [1, 32, 45, 11, 0, 78, 52]
    input_mas = []

    print("Масив:")
    print(*(f"{i} " for i in mas))
    size = 4096
    print("\nНепостійний зіставлений у пам'яті файл.")

    with mmap.mmap(-1, size, access=mmap.ACCESS_WRITE) as mm:
        for i, val in enumerate(mas):
            mm[i*4 : (i+1)*4] = struct.pack('i', val)
        print("Дані записані в анонімну пам'ять.")
        mm.seek(0)
        for _ in range(len(mas)):
            chunk = mm.read(4)
            value = struct.unpack('i', chunk)[0]
            input_mas.append(value)
        print("\nЗчитані дані:")
        print(*(f"{i} " for i in input_mas))

if __name__ == "__main__":
    main()