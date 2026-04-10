import tkinter as tk
from tkinter import colorchooser
import multiprocessing
import mmap
import struct

def child_process_window(resource_name):
    """Дочірній процес: вікно, що змінює колір фону."""
    root = tk.Tk()
    root.title("Дочірнє вікно (Результат)")
    root.geometry("400x300")
    label = tk.Label(root, font=("Arial", 12))
    label.pack(expand=True)

    def check_memory():
        try:
            with mmap.mmap(-1, 12, tagname=resource_name) as mm:
                r, g, b = struct.unpack('iii', mm[0:12])
                color_hex = f'#{r:02x}{g:02x}{b:02x}'
                root.configure(bg=color_hex)
                label.configure(bg=color_hex)
        except Exception:
            pass
        root.after(100, check_memory)
    check_memory()
    root.mainloop()

def main_app():
    """Головний процес: вікно керування."""
    resource_name = "rgb_shared_memory"
    mm = mmap.mmap(-1, 12, tagname=resource_name)
    mm[0:12] = struct.pack('iii', 240, 240, 240)
    def update_shared_memory(*args):
        """Записує значення повзунків у пам'ять."""
        r, g, b = r_scale.get(), g_scale.get(), b_scale.get()
        mm[0:12] = struct.pack('iii', r, g, b)
    p = multiprocessing.Process(target=child_process_window, args=(resource_name,))
    p.start()
    root = tk.Tk()
    root.title("Головне вікно (Керування)")
    root.geometry("300x400")

    tk.Label(root, text="Керування кольором RGB", font=("Arial", 14, "bold")).pack(pady=10)
    r_scale = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Red", fg="red", command=update_shared_memory)
    r_scale.set(240)
    r_scale.pack(fill="x", padx=20)
    g_scale = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Green", fg="green", command=update_shared_memory)
    g_scale.set(240)
    g_scale.pack(fill="x", padx=20)
    b_scale = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Blue", fg="blue", command=update_shared_memory)
    b_scale.set(240)
    b_scale.pack(fill="x", padx=20)
    def on_closing():
        mm.close()
        p.terminate()
        root.destroy()
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
if __name__ == "__main__":
    main_app()