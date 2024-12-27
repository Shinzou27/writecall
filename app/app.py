import tkinter as tk
import requests
import time
import record
from utils import url, set_call_id, headers

counting = False
initial_time = None

def start():

    label_name.pack(pady=5)
    input_name.pack(pady=5)
    btn_confirm.pack(pady=5)
    

    btn_start.config(state=tk.DISABLED)
    btn_stop.config(state=tk.DISABLED)

def confirm():
    global counting, initial_time
    name = input_name.get()
    res = requests.post(url("call"), json={"name": name}).json()
    print(res)
    set_call_id(res['id'])
    print(f"nome da call: {name}")
    record.start_recording()

    btn_stop.config(state=tk.NORMAL)

    label_name.pack_forget()
    input_name.pack_forget()
    btn_confirm.pack_forget()
    

    counting = True
    initial_time = time.time()
    update_counter()


    btn_start.config(state=tk.DISABLED)

def stop():
    global counting
    print("Chamado PARAR")
    counting = False

    time_label.config(text="")
    canvas.delete("circulo")
    record.stop_recording()

    btn_stop.config(state=tk.DISABLED)


    btn_start.config(state=tk.NORMAL)

# def list():
#     print("listando")

def update_counter():
    if counting:
        elapsed = int(time.time() - initial_time)
        h = elapsed // 3600
        m = (elapsed % 3600) // 60
        s = elapsed % 60
        time_label.config(text=f"{h:02}:{m:02}:{s:02}")
        
        window.after(1000, update_counter)

window = tk.Tk()
window.title("App Simples")
window.geometry("800x600")
window.configure(bg="#9370DB") 

botao_estilo = {
    "bg": "#4B0082", 
    "fg": "white", 
    "relief": "flat", 
    "font": ("Arial", 14),
    "width": 15,
    "height": 2,
}

btn_start = tk.Button(window, text="INICIAR", command=start, **botao_estilo)
btn_start.pack(pady=10)

btn_stop = tk.Button(window, text="PARAR", command=stop, state=tk.DISABLED, **botao_estilo)
btn_stop.pack(pady=10)

# btn_list = tk.Button(window, text="VER", command=list, **botao_estilo)
# btn_list.pack(pady=10)

label_name = tk.Label(window, text="Insira o nome da call:", bg="#9370DB", fg="white", font=("Arial", 12))
input_name = tk.Entry(window, font=("Arial", 12), width=30)
btn_confirm = tk.Button(window, text="CONFIRMAR", command=confirm, **botao_estilo)

time_label = tk.Label(window, text="", bg="#9370DB", fg="white", font=("Arial", 16))
time_label.pack(pady=20)

canvas = tk.Canvas(window, width=800, height=100, bg="#9370DB", highlightthickness=0)
canvas.pack()

window.mainloop()
