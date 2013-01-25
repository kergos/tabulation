
import sys
import pyaudio
import wave
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from numpy import * #floor, int16, fromstring, vstack, savetxt, fft

# TODOS
#1.Abgleichen der Frequenzen mit (inkl Toleranz ca 3-4+-) Array in dem Töne/Grifffrequenzen stehen
# und namen ausgeben --> weitere Instruktionen in Kommentaren in aufnahme-schleife
#2.Hemmschwelle einbauen Ton wird erst ab gewisser Lautstärke akzeptiert
#3. chibsch machen


exiting = False
class Window(QWidget):
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.thread = Worker()
        label = QLabel(self.tr("Starten sie Ihre Aufnahme"))
        self.startButton = QPushButton(self.tr("&Start"))
        self.stopButton = QPushButton(self.tr("&Stop"))
        self.viewer = QLabel()
        self.viewer.setFixedSize(300, 300)
        self.connect(self.thread, SIGNAL("finished()"), self.updateUi)
        self.connect(self.thread, SIGNAL("terminated()"), self.updateUi)
        self.connect(self.thread, SIGNAL("output(QRect, QImage)"), self.addImage)
        self.connect(self.startButton, SIGNAL("clicked()"), self.startRecording)
        self.connect(self.stopButton, SIGNAL("clicked()"), self.__del__)

        layout = QGridLayout()
        layout.addWidget(label, 0, 0)
        #layout.addWidget(self.spinBox, 0, 1)
        layout.addWidget(self.startButton, 0, 2)
        layout.addWidget(self.stopButton, 3, 4)
        layout.addWidget(self.viewer, 1, 0, 1, 3)
        self.setLayout(layout)

        self.setWindowTitle(self.tr("Tabulation Aufnahme"))

    def startRecording(self):
        self.startButton.setEnabled(False)
        self.thread.runStart()

    def addImage(self, rect, image):
        pixmap = self.viewer.pixmap()
        painter = QPainter()
        painter.begin(pixmap)
        painter.drawImage(rect, image)
        painter.end()
        self.viewer.update(rect)

    def updateUi(self):
        self.startButton.setEnabled(True)
    def __del__(self):
        global exiting
        exiting = True
        #print(exiting)

class Worker(QThread):

    def test(self):
        if exiting == True:
            global exiting
            exiting = False

    def __init__ (self, parent = None):

        QThread.__init__(self, parent)
        global exiting
        exiting = False

    def __del__(self):
        global exiting
        exiting = True
        #print(exiting)

    # def get_current_first_channel(self):
        # return self.first_channel

    # def get_current_device_nchannels(self):
        # return self.pa.get_device_info_by_index(self.device)['maxInputChannels']


    def runStart(self):
        self.start()



    def run(self):
        print("Starte Run")
        CHUNK = 1024 * 8
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        #RECORD_SECONDS = 10
        #WAVE_OUTPUT_FILENAME = "aufnahme.wav"
        #channel = self.get_current_first_channel()
        #nchannels = self.get_current_device_nchannels()
        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []
        self.test()
        #print(exiting)

        #Frequenztabelle = [65.4064, 69.2957, 73.4162, 77.7817, 82.4069, 87.3071, 92.4986, 97.9989,
                           #103.826, 110.000, 116.541, 123.471, 130.813, 138.591, 146.832, 155.563,
                           #164.814, 174.614, 184.997, 195.998, 207.652, 220.000, 233.082, 246.942,
                           #261.626, 277.183, 293.665, 311.127, 329.628, 349.228, 369.994, 391.995,
                           #415.305, 440.000, 466.164, 493.883, 523.251, 554.365, 587.330, 622.254,
                           #659.255, 698.456, 739.989, 783.991, 830.609, 880.000, 932.328, 987.767,
                           #1046.50, 1108.73, 1174.66, 1244.51, 1318.51, 1396.91, 1479.98, 1567.98,
                           #1661.22, 1760.00, 1864.66, 1957.53, 2093.00, 2217.46, 2349.32, 2489.02,
                           #2637.02, 2793.83, 2959.96, 3135.96, 3322.44, 3520.00, 3729.31, 3951.07,
                           #4186.01]
        #Notentabelle = ['X', 'X', 'X', 'X', 'E0', 'E1', 'E2', 'E3',
                        #'E4', 'E5A0', 'E6A1', 'E7A2', 'E8A3', 'E9A4', 'E10A5D0', 'E11A6D1',
                        #'E12A7D2', 'A8D3', 'A9D4', 'A10D5G0', 'A11D6G1', 'A12D7G2', 'D8G3', 'D9G4H0',
                        #'D10G5H1', 'D11G6H2', 'D12G7H3', 'G8H4', 'G9H5e0', 'G10H6e1', 'G11H7e2', 'G12H8e3',
                        #'H9e4','H10e5','H11e6','H12e7','e8','e9','e10','e11',
                        #'e12', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                         #'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                         #'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                         #'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X',
                         #'X'
                        #]

        Frequliste =     [(0, "emergency"),(65.4064, "X"), (69.2957, "X"), (73.4162, "X"), (77.7817, "X")
                        , (82.4069, "E0"), (87.3071, "E1"), (92.4986, "E2"), (97.9989, "E3")
                        , (103.826, "E4"), (110.000, "E5A0"), (116.541, "E6A1"), (123.471, "E7A2")
                        , (130.813, "E8A3"), (138.591, "E9A4"), (146.832, "E10A5D0"), (155.563, "E11A6D1")
                        , (164.814, "E12A7D2"), (174.614, "A8D3"), (184.997, "A9D4"), (195.998, "A10D5G0")
                        , (207.652, "A11D6G1"), (220.000, "A12D7G2"), (233.082, "D8G3"), (246.942, "D9G4H0")
                        , (261.626, "D10G5H1"), (277.183, "D11G6H2"), (293.665, "D12G7H3"), (311.127, "G8H4")
                        , (329.628, "G9H5e0"), (349.228, "G10H6e1"), (369.994, "G11H7e2"), (391.995, "G12H7e3")
                        , (415.305, "H8e4"), (440.000, "H9e5"), (466.164, "H10e6"), (493.883, "H11e7")
                        , (523.251, "H12e8"), (554.365, "e9"), (587.330, "e10"), (622.254, "e11")
                        , (659.255, "e12"), (698.456, "X"), (739.989, "X"), (783.991, "X")
                        , (830.609, "X"), (880.000, "X"), (932.328, "X"), (987.767, "X")
                        , (1046.50, "X"), (1108.73, "X"), (1174.66, "X"), (1244.51, "X")
                        , (1318.51, "X"), (1396.91, "X"), (1479.98, "X"), (1567.98, "X")
                        , (1661.22, "X"), (1760.00, "X"), (1864.66, "X"), (1957.53, "X")
                        , (2093.00, "X"), (2217.46, "X"), (2349.32, "X"), (2489.02, "X")
                        , (2637.02, "X"), (2793.83, "X"), (2959.96, "X"), (3135.96, "X")
                        , (3322.44, "X"), (3520.00, "X"), (3729.31, "X"), (3951.07, "X"), (4186.01, "X"),(1000000,"emergency")
                        ]


        while not exiting:
            #print(".")
            data = stream.read(CHUNK)
            frames.append(data)
            floatdata = fromstring(data, int16)[0::2] / (2. ** (16 - 1))

            #nur weitermachen wenn ueber bestimmten dB bereich
            #print(max(floatdata))
            #noch testen wie es in action reagiert
            if max(floatdata) > 0.1:

                fft_array = fft.fft(floatdata)
                #b = abs(fft_array)
                b = [abs(x) for x in fft_array][:4098]  # betrag, erste Haelfte
                m = max(b)

                for i, x in enumerate(b):
                    if x > m / 30:  # umso hoeher mehr werte
                        #print(i, i*RATE/CHUNK, " "* int(100*x/m), "#")
                        if m == x:
                            mi = i
                            #print ("max: ", m , " bei ", mi , " ",  mi*RATE/CHUNK, " Hz")
                            #Nach dem Errechnen eine Methode die das Ganze mit einer Liste abgleicht mit Toleranz
                            KEYNOTE = mi * RATE / CHUNK
                            #methode mit unscharfer abgleichung fuer notenerkennung
                            #print("Der Grundton betraegt: ", KEYNOTE, " Hz")
                            #frequentabelle mit  KEYNOTE durchgehen, ersten größeren wert nehmen
                            #index dieses wertes finden, und des wertes darunter
                            #verhältnis ausrechnen, den wert nehmen welchen verhältnis besser ist
                            # tadaa, richtige note, mithilfe des index auf notentabelle(derindex) zugreifen
                            #Profit!

                #print (KEYNOTE)

                nied = [ (f,n)  for f,n in Frequliste if f > KEYNOTE][0]
                hoch = [ (f,n)  for f,n in Frequliste if f < KEYNOTE][-1]
                #print("KN:",KEYNOTE)
                #print("nied",nied)
                #print("hoch",hoch)
                verhaltnisklein = KEYNOTE/nied[0]
                verhaltnisgross = hoch[0]/KEYNOTE
                #print(verhaltnisklein)
                #print(verhaltnisgross)
                if verhaltnisklein < verhaltnisgross:
                    print("Der Grundton ist: ",KEYNOTE,"Der Ton ist: ",hoch[0]," das entspricht den Noten: ",hoch[1])
                else:
                    print("Der Grundton ist: ",KEYNOTE,"und der Ton ist: ",nied[0]," das entspricht den Noten: ",nied[1])



                #for j in Frequenztabelle:
                    #if j > KEYNOTE:
                        ##print(j)
                        #y = Frequenztabelle.index(j)
                        ##print("keynote: ",KEYNOTE,"Der erste grossere Wert betraegt: ",j,"und der Wert darunter ist: ",Frequenztabelle[y-1])
                        #verhaltnisklein = KEYNOTE/Frequenztabelle[y-1]
                        #verhaltnisgross = j/KEYNOTE
                        ##print("verhaltnisklein: ",verhaltnisklein," verhaltnisgros: ",verhaltnisgross)
                        #if verhaltnisklein < verhaltnisgross:
                            #print("Der Grundton ist: ",KEYNOTE,"und der Ton ist: ",Frequenztabelle[y-1])
                            #print(Notentabelle[y-1])
                            ##print("mimi: ",(y-1))
                        #else:
                            #print("Der Grundton ist: ",KEYNOTE,"Der Ton ist: ",j)
                            #print(Notentabelle[y])
                            ##print("mimi: ",y)
                        #break
            #else:
                #print("treshhold geholdet")


                        #findeTon(KEYNOTE)
                        #frequenzTabelle.count(frequenz)
                        #frequenzTabelle.index(KEYNOTE)
                        #print("Frequenz kommt vor ", frequenzTabelle.count(KEYNOTE))
                        #print int(round(8359980, -2))
                        #print (round(KEYNOTE, -2))


            #print(data)
            #print(floatdata)

        #text_file = open("Output.txt", "w")0
        #text_file.write(floatdata)
        #text_file.close()
        #savetxt('output.txt', floatdata, delimiter=',')
        #savetxt('fft.txt', fft_array, delimiter=',')
        #print("done recording *")
        #print(c)

        #b = [abs(x) for x in fft_array][:3072]  #betrag, erste Haelfte
        #m = max(b)
        #with open("kurve.txt", "w") as f:
            ##mi = -1
            #for i, x in enumerate(b):
                #if x > m/10: # umso hoeher mehr werte
                    #print(i, i*RATE/CHUNK, " "* int(100*x/m), "#", file=f)
                    #if m == x:
                        #mi = i
            #print ("max: ", m , " bei ", mi , "(",  mi*RATE/CHUNK, " Hz",  file=f)

        #a = get_device_count()
        #print(a)
        #print(floatdata)
        #numpyarray into string damit in txt file
        #import pdb; pdb.set_trace() #Python Debugger
        #dir (data)
        #print(pa.get_device_info_by_index(device))
        #str(data)
        #floatdata = frombytes(data, int16)
        #print(floatdata)

        stream.stop_stream()
        stream.close()
        p.terminate()


        #nächste zeilen speichern ein wav file ab
        #wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        #wf.setnchannels(CHANNELS)
        #wf.setsampwidth(p.get_sample_size(FORMAT))
        #wf.setframerate(RATE)
        #wf.writeframes(b''.join(frames))
        #wf.close()
if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())


