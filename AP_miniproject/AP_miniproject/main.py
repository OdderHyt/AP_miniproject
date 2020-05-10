from tkinter import *
from Synthesizer import *
from AdditiveStream import *

import time

root = Tk() #first thing you do in tkinter
root.title('Guitar Synthesizer')
root.geometry("700x300")
#creating things and putting them ón the screen
synth = Synthesizer(96000)

player = AdditiveStream(96000)
noteFreqs = [0] * 48
noteNames = ["A", "A#", "B", "C" , "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

timbre = IntVar()
timbre.set(3)
octave = IntVar()
octave.set(1)


x = 0
for i, val in enumerate(noteFreqs):
    noteFreqs[i] = 55 * 2**(x/12)
    x+=1
    print(noteFreqs[i])
print("sampling all notes")


def genNoteButtons():
    x = 0
    
    for i in noteNames:
        Button(noteView, text=noteNames[x], command= lambda freq = noteFreqs[(12*octave.get())+x]: player.play(synth.makeGString(5, 1, freq, decaySlider.get(), timbre.get())), pady=20).grid(row=0, column=x, sticky="nsew")
        x+=1
        print(+x)


notesize = 0

slideView = Frame(root, bd=1, relief="sunken")
noteView = Frame(root, bd=1, relief="sunken")
octaveView = Frame(root, bd=1, relief="sunken")


slideView.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=2, pady=2)
octaveView.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)
noteView.grid(row=1, column=1, sticky="nsew", padx=2, pady=2)



root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=2)
root.grid_rowconfigure(1, weight=1)

root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

for i in range(4):
    octaveView.grid_columnconfigure(i, weight=1, uniform="fred")

for i, val in enumerate(noteNames):
    noteView.grid_columnconfigure(i, weight=1, uniform="fred")
noteView.grid_rowconfigure(0, weight=1, uniform="fred")




noteView.grid_columnconfigure(0, weight=1, uniform="fred") 
octaveNames = [
    ("1"),
    ("2"),
    ("3"),
    ("4")
]

def selectOctave():
    Label(octaveView, text="Currently playing in octave " + str(octave.get()+1)).grid(row=0, column=0, columnspan=10)
    genNoteButtons()

    print(octave.get())

for val, octaveNames in enumerate(octaveNames):
    Radiobutton(octaveView, 
                  text=octaveNames,
                  indicatoron = 0,
                  padx = 20, 
                  variable=octave, 
                  command=selectOctave,
                  value=val).grid(row=1, column = 0+val, columnspan = 1, sticky="we")

#slideview setup
sliderHeader = Label(slideView, text="Adjust the sliders below to change the guitar sounds").grid(row=0, column=0, columnspan=2)
decayLabel = Label(slideView, text="Decay:").grid(row=1, column=0)
decaySlider = Scale(slideView,
              from_=0.99, 
              to=0.9999,
              length=200,
              resolution=0.0001,
              orient=HORIZONTAL)
decaySlider.grid(row=1, column=1)
miscLabel = Label(slideView, text="Decay:").grid(row=2, column=0)
slider = Scale(slideView,
              from_=0.5, 
              to=0.999,
              length=200,
              resolution=0.001,
              orient=HORIZONTAL)
slider.grid(row=2, column=1)


timbreNames = [
    ("Sinusoid"),
    ("Square"),
    ("Sawtooth"),
    ("White Noise"),
    ("Sine Wave Chirp")
]

def selectTimbre():
    print(timbre.get())


for val, timbreNames in enumerate(timbreNames):
    Radiobutton(slideView, 
                  text=timbreNames,
                  indicatoron = 0,
                  width = 20,
                  padx = 20, 
                  variable=timbre, 
                  command=selectTimbre,
                  value=val).grid(row=3+val, column = 0, columnspan = 3, sticky="we")

selectOctave()
root.mainloop()
