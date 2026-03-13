import tkinter
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import csv

window = tkinter.Tk()
window.title("Fluxinator - Data converter")
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
frame = ttk.Frame(window, padding=20)
frame.pack(expand=True, fill="both")
frame.columnconfigure(0, weight=1)
frame.rowconfigure(1, weight=1)
frame.rowconfigure(3, weight=1)
window.minsize(500, 300)

Var1=tkinter.IntVar()

add_pdf = ttk.LabelFrame(frame, text="Add CSV(s)", padding=10)
add_pdf.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
add_pdf.columnconfigure(0, weight=1)
add_pdf.columnconfigure(1, weight=3)  

aine=tkinter.Label(add_pdf, text="Select gas")
aine.grid(row=0, column=0)

pdf=tkinter.Label(add_pdf, text="CSV name")
pdf.grid(row=0, column=1)

#Molar masses
kaasu_arvot={"-": 0, "CO2" : 44.0095, "N2O" : 44.0128, "CH4": 16.04246}

file_vars={}

def luo_lisaa(tiedo):
    nykyiset=[int(w.grid_info()['row']) for w in add_pdf.winfo_children() if int(w.grid_info()['row'])>0]
    seuraava=max(nykyiset, default=0)+1
    var=tkinter.StringVar(value="-")
    file_vars[tiedo]=var
    kaasu=ttk.Combobox(add_pdf, values=list(kaasu_arvot.keys()), textvariable=var, state="readonly")
    leima=tkinter.Label(add_pdf, text=os.path.basename(tiedo), width=50)
    kaasu.grid(row=seuraava, column=0, sticky="ew", padx=5, pady=3)
    leima.grid(row=seuraava, column=1, sticky="ew", padx=5, pady=3)
    
def data():
    tiedot=filedialog.askopenfilenames(title="Select CSV(s)", filetypes=[("CSV files","*.csv")])
    if tiedot:
        for widget in add_pdf.winfo_children():
            if int(widget.grid_info()['row'])>0:
                widget.destroy()
        file_vars.clear()
        for f in tiedot:
            luo_lisaa(f)
        window.update_idletasks()
        window.geometry("")
        
flux_unit=tkinter.Button(add_pdf, text="Select files", command=data)
flux_unit.grid(row=0, column=2)

varcheck=tkinter.BooleanVar()

#Change these values to read different lines from CSV
LM_COL = "LM.flux"
HM_COL = "HM.flux"
ID_COL = "UniqueID"

muunnos_e = tkinter.StringVar()
muunnos_k = tkinter.StringVar()
muunnos_t = tkinter.StringVar()

#Values for conversion
etu_arvot={"µg":1, "mg":0.001, "g":0.000001, "kg":0.000000001}
keski_arvot={"m²":1}
taka_arvot={"s⁻¹":1, "min⁻¹":60, "h⁻¹":3600, "d⁻¹":86400}



def muunnin_auki():
    for pdf_path, gas_var in file_vars.items():
        gas = gas_var.get()
    if gas in ("CO2", "CH4", "N2O"):    
        if varcheck.get():
            etu.config(state="normal")
            keski.config(state="normal")
            taka.config(state="normal")

        else:
            etu.config(state="disabled")
            keski.config(state="disabled")
            taka.config(state="disabled")
    else:
        etu.config(state="disabled")
        keski.config(state="disabled")
        taka.config(state="disabled")
          
converter=ttk.LabelFrame(frame, text="Converter", padding=10)
converter.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
converter.columnconfigure(0, weight=1)
converter.columnconfigure(1, weight=1)


convert_q=tkinter.Label(converter, text="Convert units during transformation?")
convert_q.grid(row=3, column=0)

checki=tkinter.Checkbutton(converter, variable=varcheck, command=muunnin_auki)
checki.grid(row=3, column=1)

varoitus=tkinter.Label(converter, text="⚠ Remember to select correct gas!", fg='red')
varoitus.grid(row=4, column=1)


etu=ttk.Combobox(converter, values=["µg", "mg", "g", "kg"],textvariable=muunnos_e, state="disabled", width=7)
etu.grid(row=6, column=0)
keski=ttk.Combobox(converter, values=["m²"],textvariable=muunnos_k, state="disabled", width=7)
keski.grid(row=6, column=1)
taka=ttk.Combobox(converter, values=["s⁻¹", "min⁻¹", "h⁻¹", "d⁻¹"],textvariable=muunnos_t, state="disabled", width=7)
taka.grid(row=6, column=2)

tallenna=ttk.LabelFrame(frame, text="Save settings", padding=10)
tallenna.grid(row=7, column=0, sticky="nsew", padx=10, pady=10)
tallenna.columnconfigure(0, weight=1)
tallenna.columnconfigure(1, weight=1)


valittu_talo=tkinter.StringVar()

def valinta_talo():
    directory=filedialog.askdirectory()
    if directory:
        valittu_talo.set(directory)

valinta_nappi=tkinter.Button(tallenna, text="Select output save location", command=valinta_talo)
valinta_nappi.grid(row=7, column=0)
valittu=tkinter.Entry(tallenna, textvariable=valittu_talo, width=30)
valittu.grid(row=7, column=1)
nimilappu=tkinter.Label(tallenna, text="Filename:")
nimilappu.grid(row=8, column=0)
nimi=tkinter.Entry(tallenna, width=30)
nimi.grid(row=8, column=1)


def safe_float(x):
    if x in ("NA", "", None):
        return None
    try:
        return float(x)
    except:
        return None

#Conversion function
def muunna(arvo, etu_val, taka_val, kaasu_val):
    if arvo is None or kaasu_val == "-":
        return "-"

    arvo = float(arvo)

    molar_mass = kaasu_arvot.get(kaasu_val, 1)
    if kaasu_val == "CH4" or kaasu_val == "N2O":
        tulos = arvo * molar_mass * 0.001
    else:
        tulos = arvo * molar_mass
    tulos *= etu_arvot.get(etu_val, 1)
    tulos *= taka_arvot.get(taka_val, 1)

    return tulos
#Write file
def extract_and_save(csv_files, out_csv):

    rows_out = []

    etu_val = muunnos_e.get()
    taka_val = muunnos_t.get()

    for polku in csv_files:

        kaasu_val = file_vars[polku].get()   

        with open(polku, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:

                uid = row.get("UniqueID", "-")

                lm = safe_float(row.get("LM.flux"))
                hm = safe_float(row.get("HM.flux"))

                
                if varcheck.get():
                    lm = muunna(lm, etu_val, taka_val, kaasu_val)
                    hm = muunna(hm, etu_val, taka_val, kaasu_val)
                else:
                    lm = lm if lm is not None else "-"
                    hm = hm if hm is not None else "-"

                rows_out.append([uid, lm, hm, kaasu_val])
    #Write rows
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Sample", "LM.flux", "HM.flux", "Gas"])
        w.writerows(rows_out)

    print("CSV saved:", out_csv)


def on_extract_button():
    out_dir = valittu_talo.get()
    filename = nimi.get()

    if not out_dir:
        messagebox.showerror("Error", "Select save location")
        return

    if not filename:
        messagebox.showerror("Error", "Enter filename")
        return

    if not filename.lower().endswith(".csv"):
        filename += ".csv"

    out_csv = os.path.join(out_dir, filename)
    extract_and_save(list(file_vars.keys()), out_csv)

    messagebox.showinfo("Done", "CSV saved!")

nappi=ttk.Button(tallenna, text="Extract data to CSV", command=on_extract_button)
nappi.grid(row=9, column=1, padx=3, pady=3)

window.mainloop()
