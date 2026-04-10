import multiprocessing
import mmap
import time
import struct

def process_b(resource_name, mutex):
    """Логіка Процесу В"""
    print("\t\tПроцес В запуск.")
    mutex.acquire()
    try:
        print("Процес В: Відкривається м'ютекс та пам'ять.")
        
        with mmap.mmap(-1, 1024, tagname=resource_name) as mm:
            print("Процес В: Запис даних (False).")
            mm[1:2] = struct.pack('?', False)
    except FileNotFoundError:
        print("Помилка: пам'ять не знайдена!")
    finally:
        mutex.release()
    print("\t\tПроцес В закінчив роботу.")

def process_a():
    """Логіка Процесу А"""
    resource_name = "procfile"
    print("\t\tПроцес А.")

    mutex = multiprocessing.Lock()

    with mmap.mmap(-1, 1024, tagname=resource_name) as mm:
        print("Створюється м'ютекс.")
        print("Непостійний зіставлений у пам'яті файл.")
        mutex.acquire()
        print("Запис даних (True).")
        mm[0:1] = struct.pack('?', True)
        mutex.release()
        
        #  Процес В 
        p_b = multiprocessing.Process(target=process_b, args=(resource_name, mutex))
        p_b.start()
        
       
        p_b.join()
        mutex.acquire()
        val_a = struct.unpack('?', mm[0:1])[0]
        val_b = struct.unpack('?', mm[1:2])[0]
        
        print(f"Процес А передав: {val_a}")
        print(f"Процес В передав: {val_b}")
        mutex.release()

if __name__ == "__main__":
    process_a()