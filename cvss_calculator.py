import tkinter as tk
from tkinter import ttk, messagebox
from cvss import CVSS3

class CVSSCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calcolatore CVSS v3.1")
        self.geometry("600x1500")
        self.create_widgets()

    def create_widgets(self):
        #Definisce le opzioni per ogni metrica
        options = {
            'AV': ['N', 'A', 'L', 'P'],
            'AC': ['L', 'H'],
            'PR': ['N', 'L', 'H'],
            'UI': ['N', 'R'],
            'S': ['U', 'C'],
            'C': ['N', 'L', 'H'],
            'I': ['N', 'L', 'H'],
            'A': ['N', 'L', 'H'],
            'E': ['X', 'U', 'P', 'F', 'H'],
            'RL': ['X', 'O', 'T', 'W', 'U'],
            'RC': ['X', 'U', 'R', 'C'],
            'CR': ['X', 'L', 'M', 'H'],
            'IR': ['X', 'L', 'M', 'H'],
            'AR': ['X', 'L', 'M', 'H'],
            'MAV': ['X', 'N', 'A', 'L', 'P'],
            'MAC': ['X', 'L', 'H'],
            'MPR': ['X', 'N', 'L', 'H'],
            'MUI': ['X', 'N', 'R'],
            'MS': ['X', 'U', 'C'],
            'MC': ['X', 'N', 'L', 'H'],
            'MI': ['X', 'N', 'L', 'H'],
            'MA': ['X', 'N', 'L', 'H'],
        }

        #Crea etichette e menu a tendina per ogni metrica
        self.metric_vars = {}
        row = 0
        section_labels = {
            'Metriche di Base': ['AV', 'AC', 'PR', 'UI', 'S', 'C', 'I', 'A'],
            'Metriche Temporali': ['E', 'RL', 'RC'],
            'Metriche Ambientali': ['CR', 'IR', 'AR', 'MAV', 'MAC', 'MPR', 'MUI', 'MS', 'MC', 'MI', 'MA'],
        }

        for section, metrics in section_labels.items():
            lbl_section = ttk.Label(self, text=section, font=('Arial', 14, 'bold'))
            lbl_section.grid(column=0, row=row, pady=(10, 0), sticky='w')
            row += 1
            for metric in metrics:
                lbl = ttk.Label(self, text=metric + ":")
                lbl.grid(column=0, row=row, sticky='w', padx=10, pady=5)
                var = tk.StringVar()
                var.set(options[metric][0])
                cmb = ttk.Combobox(self, textvariable=var, values=options[metric], state='readonly')
                cmb.grid(column=1, row=row, padx=10, pady=5, sticky='w')
                self.metric_vars[metric] = var
                row += 1

        #Bottone per calcolare il punteggio
        btn_calculate = ttk.Button(self, text="Calcola Punteggio CVSS", command=self.calculate_cvss)
        btn_calculate.grid(column=0, row=row, columnspan=2, pady=20)

        #Etichette per mostrare i risultati
        self.lbl_vector = ttk.Label(self, text="Vettore CVSS:")
        self.lbl_vector.grid(column=0, row=row+1, columnspan=2, padx=10, pady=5, sticky='w')

        self.lbl_base_score = ttk.Label(self, text="Punteggio Base:")
        self.lbl_base_score.grid(column=0, row=row+2, columnspan=2, padx=10, pady=5, sticky='w')

        self.lbl_temporal_score = ttk.Label(self, text="Punteggio Temporale:")
        self.lbl_temporal_score.grid(column=0, row=row+3, columnspan=2, padx=10, pady=5, sticky='w')

        self.lbl_environmental_score = ttk.Label(self, text="Punteggio Ambientale:")
        self.lbl_environmental_score.grid(column=0, row=row+4, columnspan=2, padx=10, pady=5, sticky='w')

        self.lbl_severity = ttk.Label(self, text="Gravità:")
        self.lbl_severity.grid(column=0, row=row+5, columnspan=2, padx=10, pady=5, sticky='w')

    def calculate_cvss(self):
        #Costruisce la stringa del vettore CVSS
        vector = "CVSS:3.1"
        for metric in ['AV', 'AC', 'PR', 'UI', 'S', 'C', 'I', 'A',
                       'E', 'RL', 'RC',
                       'CR', 'IR', 'AR',
                       'MAV', 'MAC', 'MPR', 'MUI', 'MS', 'MC', 'MI', 'MA']:
            value = self.metric_vars[metric].get()
            vector += f"/{metric}:{value}"

        try:
            cvss = CVSS3(vector)
            self.lbl_vector.config(text=f"Vettore CVSS: {cvss.clean_vector()}")
            self.lbl_base_score.config(text=f"Punteggio Base: {cvss.base_score}")
            self.lbl_temporal_score.config(text=f"Punteggio Temporale: {cvss.temporal_score}")
            self.lbl_environmental_score.config(text=f"Punteggio Ambientale: {cvss.environmental_score}")
            severities = cvss.severities()
            severity = severities[cvss.environmental_severity]
            self.lbl_severity.config(text=f"Gravità: {severity}")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore nel calcolo del punteggio CVSS:\n{e}")

if __name__ == "__main__":
    app = CVSSCalculator()
    app.mainloop()
