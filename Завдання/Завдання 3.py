import multiprocessing
import mmap
import time
def process_b(resource_name, mutex):
    """Процес В: записує друге слово"""
    time.sleep(0.5)
    mutex.acquire()
    try:
        with mmap.mmap(-1, 1024, tagname=resource_name) as mm:
            word = "World!".encode('utf-8')
            mm[7 : 7 + len(word)] = word
            print("Процес В: Записав 'World!'")
    finally:
        mutex.release()
def process_a():
    """Процес А: записує перше слово та виводить результат"""
    resource_name = "hello_map"
    mutex = multiprocessing.Lock()
    
    with mmap.mmap(-1, 1024, tagname=resource_name) as mm:
        mutex.acquire()
        word1 = "Hello, ".encode('utf-8')
        mm[0 : len(word1)] = word1
        print("Процес А: Записав 'Hello, '")
        mutex.release()
        # Процес В
        p_b = multiprocessing.Process(target=process_b, args=(resource_name, mutex))
        p_b.start()
        p_b.join()
        mutex.acquire()
        mm.seek(0)
        final_phrase = mm.read(13).decode('utf-8').strip('\x00')
        print(f"\nРезультат з пам'яті: {final_phrase}")
        mutex.release()
if __name__ == "__main__":
    process_a()