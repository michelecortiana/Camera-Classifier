import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import PIL
import cv2 as cv
import os
import model
import camera
import sys

#Tema dell'interfaccia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class CustomDialog(ctk.CTkToplevel):
    def __init__(self, parent, title, prompt, minvalue=2, maxvalue=10, initialvalue=None):
        #Costruttore: inizializza il dialogo personalizzato con titolo, prompt e input opzionale
        super().__init__(parent)
        self.parent = parent  
        self.title(title)     
        self.geometry("480x280") 
        self.resizable(False, False)  
        
        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.cancel)
        self.bind("<Escape>", lambda e: self.cancel())
        
        #Centra il dialogo rispetto alla finestra principale
        self._center_dialog(parent)
        
        #Frame principale interno con bordo arrotondato
        container = ctk.CTkFrame(self, corner_radius=10, border_width=2)
        container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        #Frame header con icona e titolo
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill=tk.X, pady=(10, 5), padx=5)
        
        #Icona informativa
        self.info_icon = self.create_icon_label(header_frame, "ℹ️", 24)
        self.info_icon.pack(side=tk.LEFT, padx=(10, 15))
        
        #Label titolo
        title_label = ctk.CTkLabel(
            header_frame, 
            text=title,
            font=("Arial", 16, "bold"),
            anchor="w"
        )
        title_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        #Frame per il prompt/testo della finestra
        prompt_frame = ctk.CTkFrame(container, fg_color="transparent")
        prompt_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        prompt_label = ctk.CTkLabel(
            prompt_frame,
            text=prompt,
            font=("Arial", 12),
            wraplength=400,   
            justify="left",
            anchor="w"
        )
        prompt_label.pack(fill=tk.X)
        
        #Frame per l'input dell'utente
        input_frame = ctk.CTkFrame(container, fg_color="transparent")
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
        if minvalue is not None and maxvalue is not None:
            #Configura OptionMenu per la selezione di un numero tra minvalue e maxvalue
            default_value = initialvalue if initialvalue is not None else minvalue
            self.value = tk.StringVar(value=str(default_value)) 
            
            input_label = ctk.CTkLabel(
                input_frame,
                text="Scegli il numero di classi da riconoscere:",
                font=("Arial", 12)
            )
            input_label.pack(side=tk.LEFT, padx=(0, 15))
            
            spinbox = ctk.CTkOptionMenu(
                input_frame,
                values=[str(i) for i in range(minvalue, maxvalue+1)],
                variable=self.value,
                width=80,
                height=32,
                font=("Arial", 14),
                dynamic_resizing=False
            )
            spinbox.pack(side=tk.LEFT)
        else:
            #Configura Entry per l'inserimento del nome della classe
            self.value = tk.StringVar(value=initialvalue if initialvalue else "")
            
            entry = ctk.CTkEntry(
                input_frame,
                textvariable=self.value,
                font=("Arial", 14),
                height=40,
                corner_radius=8,
                placeholder_text="Inserisci il nome della classe" if not initialvalue else None
            )
            entry.pack(fill=tk.X, pady=5)
            entry.focus_set() 
            if initialvalue:
                entry.select_range(0, tk.END)  
        
        #Frame per i pulsanti OK e Cancel
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(fill=tk.X, pady=(15, 10), padx=20)
        
        #Pulsante Cancel
        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            command=self.cancel,
            font=("Arial", 12, "bold"),
            fg_color="#6c757d",
            hover_color="#5a6268",
            width=100,
            height=36
        ).pack(side=tk.RIGHT, padx=10)
        
        #Pulsante OK
        ok_btn = ctk.CTkButton(
            btn_frame,
            text="OK",
            command=self.ok,
            font=("Arial", 12, "bold"),
            width=100,
            height=36
        )
        ok_btn.pack(side=tk.RIGHT)
        
        self.bind('<Return>', lambda e: self.ok())
        self.result = None
    
    def _center_dialog(self, parent):
        #Posiziona il dialogo al centro della finestra principale
        parent.update_idletasks()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        
        dialog_width = 480
        dialog_height = 280

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        x = max(0, x)
        y = max(0, y)
        
        self.geometry(f"+{x}+{y}")  #Posizione finale
    
    def create_icon_label(self, parent, text, size):
        #Crea un'etichetta circolare con icona e colore personalizzato
        return ctk.CTkLabel(
            parent,
            text=text,
            font=("Arial", size),
            width=40,
            height=40,
            corner_radius=20,
            fg_color="#0d6efd",
            text_color="white"
        )
    
    def ok(self, event=None):
        #Conferma l'input dell'utente e chiude il dialogo
        try:
            val = int(self.value.get())  
        except Exception:
            val = self.value.get() 
        self.result = val
        self.destroy()
        
    def cancel(self, event=None):
        #Annulla l'input dell'utente e chiude il dialogo
        self.result = None
        self.destroy()


class App:
    def __init__(self, window=ctk.CTk(), window_title="Camera Classifier"):
        #Costruttore: inizializza l'applicazione, crea la finestra principale, inizializza classi, modello, camera e GUI
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1200x900")
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), "app_icon.png")
            self.window.iconbitmap(icon_path)
        except Exception as e:
            print(f"Errore nel caricamento dell'icon: {e}")
        
        self.max_classes = 10
        self.class_names = []
        self.counters = []
        self.auto_predict = False
        
        #Carica le icone necessarie
        self.load_assets()
        
        #Inizializza le classi (cartelle e nomi)
        self.init_classes()
        
        #Inizializza modello e camera
        self.model = model.Model(num_classes=len(self.class_names))
        self.camera = camera.Camera()
        
        #Costruisce la GUI
        self.init_gui()
        self.delay = 15
        self.update()
        self.window.mainloop()

    def load_assets(self):
        #Carica le icone da file e le salva in un dizionario; se non trovate, usa un dizionario vuoto
        try:
            self.icons = {
                "camera": ImageTk.PhotoImage(Image.open("camera_icon.png").resize((24, 24))),
                "train": ImageTk.PhotoImage(Image.open("train_icon.png").resize((24, 24))),
                "predict": ImageTk.PhotoImage(Image.open("predict_icon.png").resize((24, 24))),
                "auto": ImageTk.PhotoImage(Image.open("auto_icon.png").resize((24, 24))),
                "reset": ImageTk.PhotoImage(Image.open("reset_icon.png").resize((24, 24))),
            }
        except:
            self.icons = {}

    def init_classes(self):
        #Chiede all'utente quante classi creare e i nomi di ciascuna, creando le cartelle corrispondenti
        num_dialog = CustomDialog(
            self.window, 
            "Class Setup", 
            "Quante classi vuoi creare ?",
            minvalue=2, 
            maxvalue=10
        )
        self.window.wait_window(num_dialog)
        
        if num_dialog.result is None:
            self.window.destroy()
            sys.exit(0)

        num_classes = int(num_dialog.result)

        for i in range(1, num_classes + 1): 
            os.makedirs(str(i), exist_ok=True)
            self.counters.append(1)
            
            name_dialog = CustomDialog(
                self.window,
                f"Class {i} name",
                f"Inserisci il nome della classe {i}:",
                minvalue=None,  
                maxvalue=None,
                initialvalue=""  
            )
            self.window.wait_window(name_dialog)
            
            if name_dialog.result is None:
                self.window.destroy()
                sys.exit(0)

            class_name = name_dialog.result or f"Class {i}"
            self.class_names.append(class_name)

    def init_gui(self):
        #Crea tutta l'interfaccia grafica: header, camera, pulsanti, status e layout generale
        self.window.grid_columnconfigure(0, weight=1)
        self.window.grid_rowconfigure(0, weight=1)
        
        main_container = ctk.CTkFrame(self.window, corner_radius=10)
        main_container.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)
        main_container.grid_columnconfigure(0, weight=1)
        main_container.grid_rowconfigure(1, weight=1)
        
        header = ctk.CTkFrame(
            main_container, 
            height=80, 
            corner_radius=10,
            fg_color="#0d6efd"
        )
        header.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))
        
        title_label = ctk.CTkLabel(
            header,
            text="CAMERA CLASSIFIER",
            font=("Arial", 20, "bold"),
            text_color="white"
        )
        title_label.pack(side=tk.LEFT, padx=20)
        
        cam_container = ctk.CTkFrame(
            main_container, 
            corner_radius=10
        )
        cam_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        cam_container.grid_columnconfigure(0, weight=1)
        cam_container.grid_rowconfigure(1, weight=1)
        
        cam_header = ctk.CTkFrame(
            cam_container, 
            height=40,
            corner_radius=8,
            fg_color="#1e2a38"
        )
        cam_header.grid(row=0, column=0, sticky="ew", padx=5, pady=(5, 0))
        
        ctk.CTkLabel(
            cam_header,
            text="LIVE CAMERA",
            font=("Arial", 12, "bold"),
            text_color="#6ea8fe"
        ).pack(side=tk.LEFT, padx=15)
        
        self.cam_status = ctk.CTkLabel(
            cam_header,
            text="● ACTIVE",
            font=("Arial", 11),
            text_color="#20c997"
        )
        self.cam_status.pack(side=tk.RIGHT, padx=15)
        
        self.canvas = tk.Canvas(
            cam_container, 
            bg='#000000',
            highlightthickness=0,
            bd=0,
            relief='ridge'
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=5, pady=(0, 5))
        
        capture_container = ctk.CTkFrame(
            main_container, 
            height=100,
            corner_radius=10
        )
        capture_container.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        scroll_frame = ctk.CTkScrollableFrame(
            capture_container,
            orientation="horizontal",
            fg_color="transparent"
        )
        scroll_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        colors = ['#0d6efd', '#dc3545', '#198754', '#ffc107', '#6f42c1',
                  '#0dcaf0', '#fd7e14', '#6610f2', '#d63384', '#20c997']
        
        #Crea pulsanti per ogni classe
        self.class_buttons = []
        for i, class_name in enumerate(self.class_names):
            btn = ctk.CTkButton(
                scroll_frame,
                text=f"  📸 {class_name}",
                font=("Arial", 12, "bold"),
                fg_color=colors[i % len(colors)],
                hover_color=self.darken_color(colors[i % len(colors)]),
                height=45,
                width=180,
                corner_radius=8,
                command=lambda idx=i: self.save_for_class(idx + 1),
                anchor="w"
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.class_buttons.append(btn)
        
        control_container = ctk.CTkFrame(
            main_container, 
            height=80,
            corner_radius=10
        )
        control_container.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        
        #Pulsanti di controllo principali
        control_buttons = [
            ("Avvia Auto Prediction", self.auto_predict_toggle, "#198754", "auto"),
            ("Train Model", self.train_model, "#fd7e14", "train"),
            ("Predict", self.predict, "#6f42c1", "predict"),
            ("Reset", self.reset, "#6c757d", "reset")
        ]
        
        for i, (text, command, color, icon_key) in enumerate(control_buttons):
            btn = ctk.CTkButton(
                control_container,
                text=text,
                font=("Arial", 12, "bold"),
                fg_color=color,
                hover_color=self.darken_color(color),
                height=45,
                width=200,
                corner_radius=8,
                command=command,
                image=self.icons.get(icon_key, None),
                compound="left"
            )
            btn.grid(row=0, column=i, padx=10, pady=15)
            
            if "Auto" in text:
                self.btn_toggleauto = btn
            elif "Train" in text:
                self.btn_train = btn
            elif "Predict" == text:
                self.btn_predict = btn
            elif "Reset" in text:
                self.btn_reset = btn
        
        #Sezione status e label per prediction e contatore
        status_container = ctk.CTkFrame(
            main_container, 
            height=100,
            corner_radius=10,
            fg_color="#1e2a38"
        )
        status_container.grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 10))
        
        status_left = ctk.CTkFrame(status_container, fg_color="transparent")
        status_left.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        ctk.CTkLabel(
            status_left,
            text="PREDICTION:",
            font=("Arial", 12),
            text_color="#6ea8fe"
        ).pack(anchor="w")
        
        self.class_label = ctk.CTkLabel(
            status_left,
            text="IDLE",
            font=("Arial", 24, "bold"),
            text_color="#adb5bd"
        )
        self.class_label.pack(anchor="w", pady=(5, 0))
        
        status_right = ctk.CTkFrame(status_container, fg_color="transparent")
        status_right.pack(side=tk.RIGHT, padx=20, pady=10)
        
        self.counter_label = ctk.CTkLabel(
            status_right,
            font=("Arial", 11),
            text_color="#6ea8fe"
        )
        self.counter_label.pack(anchor="e")
        self.update_counter_label()
        
        #Barra di stato in basso
        self.status_bar = ctk.CTkLabel(
            self.window,
            text="Ready",
            anchor="w",
            font=("Arial", 10),
            height=28,
            corner_radius=0,
            fg_color="#0d6efd",
            text_color="white"
        )
        self.status_bar.grid(row=1, column=0, sticky="sew", padx=0, pady=0)
        
        #Dimensioni minime della finestra
        self.window.minsize(1000, 800)
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

    def darken_color(self, hex_color, factor=0.8):
        #Oscura un colore esadecimale riducendo la luminosità di ciascun canale RGB
        hex_color = hex_color.lstrip('#')
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        r = max(0, int(r * factor))
        g = max(0, int(g * factor))
        b = max(0, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def on_window_resize(self, event):
        #Aggiornamento dela dimensione della canvas quando la finestra principale viene ridimensionata
        if event.widget == self.window:
            self.update_canvas_size()

    def update_canvas_size(self):
        #Ridimensiona il canvas della camera in base alle dimensioni del contenitore e ridisegna l'immagine corrente
        container = self.canvas.master
        width = container.winfo_width() - 2
        height = container.winfo_height() - 2
        
        if width > 10 and height > 10:
            self.canvas.config(width=width, height=height)
            
            if hasattr(self, 'photo'):
                self.canvas.delete("all")
                self.canvas.create_image(
                    width//2, 
                    height//2, 
                    image=self.photo, 
                    anchor=tk.CENTER
                )

    def button_hover(self, event, button):
        #Effetto hover a un pulsante al passaggio del mouse
        button.config(relief=tk.RAISED, bd=1)

    def button_leave(self, event, button):
        #Reset dello stile del pulsante quando il mouse lascia il pulsante
        button.config(relief=tk.FLAT, bd=0)

    def update_counter_label(self):
        #Aggiorna l'etichetta dei contatori delle immagini salvate per ogni classe
        counters_text = " | ".join(
            f"{name}: {self.counters[i]-1}" 
            for i, name in enumerate(self.class_names)
        )
        self.counter_label.configure(text=f"Images: {counters_text}")

    def auto_predict_toggle(self):
        #Attiva o disattiva la modalità di predizione automatica e aggiorna i pulsanti e label corrispondenti
        self.auto_predict = not self.auto_predict
        status = "ON" if self.auto_predict else "OFF"
        color = "#198754" if self.auto_predict else "#dc3545"
        
        self.btn_toggleauto.configure(
            text=f"Auto Prediction: {status}",
            fg_color=color,
            hover_color=self.darken_color(color)
        )
        
        if not self.auto_predict:
            self.class_label.configure(text="IDLE", text_color="#adb5bd")
            self.status_bar.configure(text="Auto prediction stopped")

    def save_for_class(self, class_num):
        #Salvataggio immagine corrente dalla camera nella cartella della classe specificata
        result = self.camera.get_frame()
        if not result:
            return
            
        ret, frame = result
        if not ret:
            return
        
        #Preparazione directory e nome file
        class_idx = class_num - 1
        os.makedirs(str(class_num), exist_ok=True)
        filename = f'{class_num}/frame{self.counters[class_idx]}.jpg'
        
        #Processa e salva l'immagine
        gray = cv.cvtColor(frame, cv.COLOR_RGB2GRAY)
        resized = cv.resize(gray, (149, 112))
        cv.imwrite(filename, resized)
        
        #Aggiorna contatore e interfaccia
        self.counters[class_idx] += 1
        self.update_counter_label()
        self.status_bar.configure(text=f"Immagine salvata {filename}")
        
        #Feedback visivo sul pulsante
        original_color = self.class_buttons[class_idx].cget("fg_color")
        self.class_buttons[class_idx].configure(fg_color="#f1c40f")
        self.window.after(300, lambda: self.class_buttons[class_idx].configure(fg_color=original_color))

    def train_model(self):
        #Allenamento del modello usando le immagini salvate e aggiorna la GUI
        self.model.train_model(self.counters)
        self.status_bar.configure(text="Allenamento completato!")
        self.class_label.configure(text="READY", text_color='#2ecc71')

        #Feedback visivo sul pulsante
        original_color = self.btn_train.cget("fg_color")
        self.btn_train.configure(fg_color="#27ae60")
        self.window.after(500, lambda: self.btn_train.configure(fg_color=original_color))

    def reset(self):
        #Reset del modello e cancella tutte le immagini salvate per ogni classe
        for i in range(1, len(self.class_names) + 1):
            folder = str(i)
            if os.path.exists(folder):
                for file in os.listdir(folder):
                    file_path = os.path.join(folder, file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                    except Exception as e:
                        print(f"Errore nell'eliminazione {file_path}: {e}")
        
        #Reset dei contatori e modello
        self.counters = [1] * len(self.class_names)
        self.model = model.Model(num_classes=len(self.class_names))
        self.update_counter_label()
        self.class_label.configure(text="RESET", text_color='#f39c12')
        self.status_bar.configure(text="Modello e immagini resettate correttamente!")
        
        #Feedback visivo sul pulsante
        original_color = self.btn_reset.cget("fg_color")
        self.btn_reset.configure(fg_color="#27ae60")
        self.window.after(500, lambda: self.btn_reset.configure(fg_color=original_color))

    def update(self):
        #Aggiorna il frame della camera e ridisegna sul canvas; esegue predizione automatica se abilitata
        result = self.camera.get_frame()
        if result:
            ret, frame = result
            if ret:
                self.photo = PIL.ImageTk.PhotoImage(
                    image=PIL.Image.fromarray(frame)
                )
                self.canvas.delete("all")  
                self.canvas.create_image(
                    self.canvas.winfo_width()//2, 
                    self.canvas.winfo_height()//2, 
                    image=self.photo, 
                    anchor=tk.CENTER
                )
                
                if self.auto_predict and self.model.is_trained:
                    self.predict(frame)
        
        self.window.after(self.delay, self.update)

    def predict(self, frame=None):
        #Esegue la predizione della classe per il frame fornito (o il frame corrente dalla camera)
        if frame is None:
            result = self.camera.get_frame()
            if not result:
                return
            ret, frame = result
            if not ret:
                return
            frame_data = (ret, frame)
        else:
            frame_data = (True, frame)
        
        #Controllo se il modello è allenato
        if not self.model.is_trained:
            self.class_label.configure(text="TRAIN FIRST!", text_color='#e74c3c')
            self.status_bar.configure(text="Modello non allenato - allenare il modello prima !")
            return
        
        prediction = self.model.predict(frame_data)
        
        #Aggiorna label e barra di stato in base alla predizione
        if 1 <= prediction <= len(self.class_names):
            class_idx = prediction - 1
            class_name = self.class_names[class_idx]
            self.class_label.configure(text=f"{class_name} ✓", text_color='#2ecc71')
            self.status_bar.configure(text=f"Predicted: {class_name}")
        else:
            self.class_label.configure(text="UNCERTAIN", text_color='#f39c12')
            self.status_bar.configure(text="Poco sicuro sull'esito")
        
        #Feedback visivo sul pulsante Predict
        if frame is None:
            original_color = self.btn_predict.cget("fg_color")
            self.btn_predict.configure(fg_color="#27ae60")
            self.window.after(300, lambda: self.btn_predict.configure(fg_color=original_color))
