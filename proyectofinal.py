# Archivo con distintas funciones 
import funciones as fn
# Para la ventana
from tkinter import ttk
import tkinter as tk
# Directorio
import os
# Librosa para el audio
import librosa

#Primero vamos a definir la clase song
class Cancion:
    song_name = ''
    # Audio File
    song = None
    bpm = None
    key = ''
    _dmax = 4
    _sr = 44100 # Fijamos la señal a 44.1KHz
    
    # Constructor 
    def __init__(self, song_name):
        # Asignamos el archivo al atributo song
        direccion = os.getcwd() + '/Música'
        self.song_name = direccion + '/' + song_name + '.ogg'
        #Cargamos la cancion a librosa con el método load
        self.song, self.sr = librosa.load(self.song_name, sr=self._sr)
    
    # Metodo para determinar BPM
    def determinarBpm(self):
        # Separamos la parte de las percusiones
        song_percussive = librosa.effects.percussive(self.song)
        # Determinamos el bpm
        tempo, beats = librosa.beat.beat_track(y=song_percussive, sr=self._sr)
        self.bpm = round(tempo, 2)
        
        return self.bpm
        
    # Metodo para determinar la tonalidad
    def determinarKey(self):
        # Separamos la parte de la armonia
        song_harmonic = librosa.effects.harmonic(self.song)
        # Determinamos la energía por tiempo en cada nota
        energy = librosa.feature.chroma_cqt(y=song_harmonic, sr=self._sr, 
                                            bins_per_octave=36)
        # Llamamos a la funcion que obtinene la tonalidad
        self.key = fn.obtenerKey(energy, self._dmax)
        
        return self.key

# Seguimos con la clase Mezcla
class Mezcla:
    bpm_mix = [None, None]
    bpmSong1 = None
    bpmSong2 = None
    key_mix = ['', '']
    keySong1 = ''
    keySong2 = ''
    compatibilidad = ''
    
    # Constructor del objeto tipo Mix
    def __init__(self, song_name1, song_name2):
    
        # Construimos los objetos tipo cancion
        song1 = Cancion(song_name1)
        song2 = Cancion(song_name2)
        
        # Pasamos sus atributos a atributos a manejar por mezcla
        self.bpmSong1 = song1.determinarBpm()
        self.bpmSong2 = song2.determinarBpm()
        self.keySong1 = song1.determinarKey()
        self.keySong2 = song2.determinarKey()
    
    # Método para determinar el Bpm de la mezcla
    def determinarBpmMix(self):
        for n in range(len(self.bpm_mix)):
            ptoMedio = round((self.bpmSong1 + self.bpmSong2)/2,2)
            if n == 0:
                if (self.bpmSong1 < self.bpmSong2):
                    if (abs(self.bpmSong1 - ptoMedio) > abs(self.bpmSong1*2 - 
                                                            self.bpmSong2)):
                        a = self.bpmSong1*2
                        ptoMedio = round((a + self.bpmSong2)/2,2)
                        #diff = bpmSong1 - ptoMedio
                        self.bpm_mix[n] = ptoMedio/2
                    else:
                        self.bpm_mix[n] = ptoMedio
                elif (self.bpmSong1 > self.bpmSong2):
                    if (abs(self.bpmSong2 - ptoMedio) > abs(self.bpmSong2*2 - 
                                                            self.bpmSong1)):
                        b = self.bpmSong2*2
                        ptoMedio = round((self.bpmSong1 + b)/2,2)
                        #diff = bpmSong1 - ptoMedio
                        self.bpm_mix[n] = ptoMedio
                    else:
                        self.bpm_mix[n] = ptoMedio
                else:
                    self.bpm_mix[n] = ptoMedio
            else:
                if (self.bpmSong2 < self.bpmSong2):
                    if (abs(self.bpmSong2 - ptoMedio) > abs(self.bpmSong2*2 - 
                                                            self.bpmSong1)):
                        a = self.bpmSong2*2
                        ptoMedio = round((a + self.bpmSong1)/2,2)
                        self.bpm_mix[n] = ptoMedio/2
                    else:
                        self.bpm_mix[n] = ptoMedio
                elif (self.bpmSong2 > self.bpmSong1):
                    if (abs(self.bpmSong1 - ptoMedio) > abs(self.bpmSong1*2 - 
                                                            self.bpmSong2)):
                        b = self.bpmSong1*2
                        ptoMedio = round((self.bpmSong2 + b)/2,2)
                        #diff = bpmSong1 - ptoMedio
                        self.bpm_mix[n] = ptoMedio
                    else:
                        self.bpm_mix[n] = ptoMedio
                else:
                    self.bpm_mix[n] = ptoMedio
        
        return self.bpm_mix
    
    # Método para determinar la armoniciadad de la mezcla
    def determinarArmonicidadMix(self):
        # Le asignamos un valor de la rueda de camelot a cada tonalidad
        # Cancion 1
        keySong1Camelot = fn.asignarCamelotValue(self.keySong1)
        # Cancion 2
        keySong2Camelot = fn.asignarCamelotValue(self.keySong2)
        
        # Comparamos
        if (keySong1Camelot[0] == keySong2Camelot[0]):
            self.compatibilidad = "Son armónicamente compatibles, pues tienen la misma tonalidad o son tonalidades relativas"
        elif (keySong1Camelot[1] == keySong2Camelot[1]):
            if (keySong1Camelot[0] == 12):
                if (keySong2Camelot[0] == 1 or keySong2Camelot[0] == 11):
                    self.compatibilidad = 'Son armónicamente compatibles, pues son tonalidades adyacentes en la rueda de Camelot'
                else:
                    self.compatibilidad = "No son armónicamente compatibles"
            if (keySong1Camelot[0] == 1):
                if (keySong2Camelot[0] == 2 or keySong2Camelot[0] == 12):
                    self.compatibilidad = 'Son armónicamente compatibles, pues son tonalidades adyacentes en la rueda de Camelot'
                else:
                    self.compatibilidad = "No son armónicamente compatibles"
            elif (keySong1Camelot[0] + 1 == keySong2Camelot[0] or 
                  keySong1Camelot[0] - 1 == keySong2Camelot[0]):
                    self.compatibilidad = 'Son armónicamente compatibles, pues son tonalidades adyacentes en la rueda de Camelot'
            else:
                self.compatibilidad = "No son armónicamente compatibles"
        else:
            self.compatibilidad = "No son armónicamente compatibles"
        
        return self.compatibilidad

# Ahora la clase Ventana
class Application(ttk.Frame):
    
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.title("Mezcla armónica")
        s = ttk.Style()
        s.configure('TFrame', background='SlateGray1')
        
        # Primero mostramos en la ventana las intrucciones
        self.label_presentacion = tk.Label(self, 
        text= "Con este programa podrás verificar la compatibilidad armónica de la mezcla de dos canciones.", bg='SlateGray1')
        self.label_presentacion.place(x=50, y=15)
        
        self.label_presentacion2 = tk.Label(self, 
        text= "Selecciona una canción de cada una de las siguientes listas. Después, presiona el botón de la parte inferior izquierda.", 
        bg ='SlateGray1')
        self.label_presentacion2.place(x=50, y=35) 
        
        # Llamos a la dirección de memoria de nuestra música
        direccion = os.getcwd() + '/Música'
        contenido = os.listdir(direccion)
        # Determinamos la lista de canciones disponible
        listaCanciones = []
        for fichero in contenido:
            if os.path.isfile(os.path.join(direccion, fichero)) and fichero.endswith('.ogg'):
                listaCanciones.append(fichero)
        
        # Le quitamos la terminación del archivo, para que el usuario no tenga que verla
        for n in range(len(listaCanciones)):
            listaCanciones[n] = listaCanciones[n].rstrip(".ogg")
        
        # Abrimos dos listas desplegables
        
        # Lista desplegable 1
        # Para evitar que el usuario ingrese sus valores
        self.combo1 = ttk.Combobox(self, state="readonly")
        # Agregamos valores
        self.combo1["values"] = listaCanciones
        self.combo1.place(x=50, y=60)
              
        # Lista desplegable 2
        # Para evitar que el usuario ingrese sus valores
        self.combo2 = ttk.Combobox(self, state="readonly")
        # Agregamos valores
        self.combo2["values"] = listaCanciones
        self.combo2.place(x=400, y=60)
        
        # Especificamos el analisis al que corresponde cada una
        self.controlTexto1 = "Análisis de la primera canción" #binding
        self.label1 = tk.Label(self, text=self.controlTexto1, bg='SteelBlue1')
        self.label1.place(x=50, y=95)
        
        self.controlTexto2 = "Análisis de la segunda canción" #binding
        self.label2 = tk.Label(self, text=self.controlTexto2, bg='SteelBlue1')
        self.label2.place(x=400, y=95)
        
        # Boton que incia el analisis
        self.botonAnalisis = tk.Button(self, text="Iniciar análisis", 
        command = lambda:[self.crearMezcla(), self.mostrarBpm(), self.mostrarKey(), self.mostrarMezcla()], bg = 'SteelBlue3')
        self.botonAnalisis.place(x=50, y=250)
        
        # Boton para cerrar la ventana
        self.botonCerrar = tk.Button(self, text = "Cerrar ventana", command = self.cerrar, bg = 'red2')
        self.botonCerrar.place(x=400, y=250)
        
        main_window.configure(width=700, height=300)
        self.place(width=700, height=300)
    
    def cerrar(self):
        self.after(2000, self.destroy)
        
    def crearMezcla(self):
        self.mezcla = Mezcla(self.combo1.get(),self.combo2.get())        

    def mostrarBpm(self):
        self.label3 = tk.Label(self, text="BPM: ", bg = 'SlateGray1')
        self.label3.place(x=50, y=125)
        bpm1 = self.mezcla.bpmSong1
        self.label4 = tk.Label(self, text=bpm1, bg = 'SlateGray1', fg = 'red')
        self.label4.place(x=90, y=125)
        
        self.label5 = tk.Label(self, text="BPM: ", bg = 'SlateGray1')
        self.label5.place(x=400, y=125)
        bpm2 = self.mezcla.bpmSong2
        self.label6 = tk.Label(self, text=bpm2, bg = 'SlateGray1', fg = 'red')
        self.label6.place(x=440, y=125)
    
    def mostrarKey(self):
        self.label7 = tk.Label(self, text=("Tonalidad: "), bg = 'SlateGray1')
        self.label7.place(x=50, y=145)
        key1 = self.mezcla.keySong1
        self.label8 = tk.Label(self, text=key1, bg = 'SlateGray1', fg = 'red')
        self.label8.place(x=110, y=145)
        
        self.label9 = tk.Label(self, text=("Tonalidad: "), bg = 'SlateGray1')
        self.label9.place(x=400, y=145)
        key2 = self.mezcla.keySong2
        self.label10 = tk.Label(self, text=key2, bg = 'SlateGray1', fg = 'red')
        self.label10.place(x=460, y=145)
        
    def mostrarMezcla(self):
        self.label20 = tk.Label(self, text="Mostrando analisis de mezcla", bg='SteelBlue1')
        self.label20.place(x=50, y=175)
        
        #Utilizamos el metodo que determina el bpm de la mezcla
        bpmMix = self.mezcla.determinarBpmMix()
        
        # Determinamos el bpm de la mezcla de 1
        self.label11 = tk.Label(self, text=("BPM de la mezcla primera canción: "), bg = 'SlateGray1')
        self.label11.place(x=50, y=195)
        
        self.label12 = tk.Label(self, text = bpmMix[0], bg = 'SlateGray1', fg = 'red')
        self.label12.place(x=250, y=195)
        
        # Determinamos el bpm de la mezcla 2
        self.label21 = tk.Label(self, text=("BPM de la mezcla segunda canción: "), bg = 'SlateGray1')
        self.label21.place(x=400, y=195)
        
        self.label22 = tk.Label(self, text = bpmMix[1], bg = 'SlateGray1', fg = 'red')
        self.label22.place(x=600, y=195)
        
        # Determinamos si son armonicas de la mezcla
        keyMix = self.mezcla.determinarArmonicidadMix()
        self.label14 = tk.Label(self, text = "Compatibilidad armónica: ", bg = 'SlateGray1')
        self.label14.place(x=50, y=225)
        self.label15 = tk.Label(self, text = keyMix, bg = 'SlateGray1', fg = 'red')
        self.label15.place(x=200, y=225)
        
# Corremos la clase ventana        
main_window = tk.Tk()
app = Application(main_window)
app.mainloop()
