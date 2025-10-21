import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import schedule
import time
import win32serviceutil
import logging

#log
logging.basicConfig(filename='ReiniciarJboss_Log.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def reiniciar_servico():
    #para serviço
    win32serviceutil.StopService('JBAS711SVC')
    
    #iniciar serviço
    win32serviceutil.StartService('JBAS711SVC')
    
    status_label.config(text="O serviço foi reiniciado com sucesso.")
    logging.info("O serviço foi reiniciado com sucesso.") 

def agendar_reinicio():
    horario = entry_horario.get()
    schedule.every().day.at(horario).do(reiniciar_servico)
    status_label.config(text=f"O serviço do Jboss será reiniciado às {horario}.")
    logging.info(f"HORARA DIÁRIA DE REINICIO AGENDADO PARA ÀS {horario}.")

def verificar_agendamentos():
    schedule.run_pending()
    root.after(1000, verificar_agendamentos)

def exibir_log():
    with open('ReiniciarJboss_Log.log', 'r') as log_file:
        log_content = log_file.read()

    log_window = tk.Toplevel(root)
    log_window.title("Log de Execução")

    log_text = scrolledtext.ScrolledText(log_window, wrap=tk.WORD, width=80, height=20)
    log_text.pack(expand=True, fill='both')

    log_text.insert(tk.END, log_content)
    log_text.configure(state='disabled')

#janela principal em tkinter
root = tk.Tk()
root.title("Controle de Serviço - JBoss")

#botão reiniciar o serviço
btn_reiniciar = ttk.Button(root, text="Reiniciar Jboss", command=reiniciar_servico)
btn_reiniciar.pack(pady=10)

#inserir o horário do agendamento
label_horario = ttk.Label(root, text="                   Agendamento de Horario (HH:MM):                     ")
label_horario.pack(pady=5)
entry_horario = ttk.Entry(root)
entry_horario.pack(pady=5)

#botão agendar o reinício do serviço
btn_agendar = ttk.Button(root, text="Agendar o Reinício", command=agendar_reinicio)
btn_agendar.pack(pady=5)

#botão de exibir log
btn_exibir_log = ttk.Button(root, text="Exibir Log", command=exibir_log)
btn_exibir_log.pack(pady=10)

#status do serviço/agendamento
status_label = ttk.Label(root, text="")
status_label.pack(pady=5)

#inicia o loop da aplicação e a verificação de agendamentos
root.after(1000, verificar_agendamentos)
root.mainloop()