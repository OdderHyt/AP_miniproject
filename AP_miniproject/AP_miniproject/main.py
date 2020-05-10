from tkinter import *
from Synthesizer import *
from AdditiveStream import *

root = Tk() #first thing you do in tkinter
root.title('Guitar Synthesizer')
root.geometry("700x300")
#creating things and putting them ón the screen
synth = Synthesizer()

player = AdditiveStream()
noteFreqs = [0] * 60
noteNames = ["A", "A#", "B", "C" , "C#", "D", "D#", "E", "F", "F#", "G", "G#"]


x = 0
for i, val in enumerate(noteFreqs):
    noteFreqs[i] = 55 * 2**(x/12)
    x+=1
    print(noteFreqs[i])
print("sampling all notes")

for i in range(12):
    player.play(synth.makeGString(5,1,noteFreqs[12+i],0.990))
    player.play(synth.hardClipping(synth.makeGString(5,1,noteFreqs[12+i],0.990), .07))
    player.play(synth.fullWaveRectifier(synth.makeGString(5,1,noteFreqs[12+i],0.990)))
    player.play(synth.halfWaveRectifier(synth.makeGString(5,1,noteFreqs[12+i],0.990)))


def genNoteButtons(octaveshift):
    x = 0
    for i in noteNames:
        Label(octaveView, text="Currently playing in octave "+ str(int(octaveshift/12)+1)).grid(row=0, column=0, columnspan=10)
        Button(noteView, text=noteNames[x], command= lambda: player.play(synth.makeGString(5, 1, noteFreqs[x+octaveshift], slider.get())), pady=20).grid(row=0, column=x, sticky="nsew")
        x+=1
        print(octaveshift+x)

def octaveChanger(octave):
    if octave == 1:
        genNoteButtons(0)
    elif octave == 2:
        genNoteButtons(12)
    elif octave == 3:
        genNoteButtons(24)
    elif octave == 4:
        genNoteButtons(36)
    elif octave == 5:
        genNoteButtons(48)
    else:
        print("Octave error: No Octave selected?")


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




noteView.grid_columnconfigure(0, weight=1, uniform="fred")#octaveview setup
octOne = Button(octaveView, text="1", command= lambda: octaveChanger(1), padx=20).grid(row=1, column=0, sticky="nsew")
octTwo = Button(octaveView, text="2", command= lambda: octaveChanger(2), padx=20).grid(row=1, column=1, sticky="nsew")
octThree = Button(octaveView, text="3", command= lambda: octaveChanger(3), padx=20).grid(row=1, column=2, sticky="nsew")
octFour = Button(octaveView, text="4", command= lambda: octaveChanger(4), padx=20).grid(row=1, column=3, sticky="nsew")

#slideview setup
sliderHeader = Label(slideView, text="Adjust the sliders below to change the guitar sounds").grid(row=0, column=0, columnspan=2)
decayLabel = Label(slideView, text="Decay:").grid(row=1, column=0)
decaySlider = Scale(slideView,
              from_=0.5, 
              to=0.999,
              length=200,
              resolution=0.001,
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


octaveChanger(2)
root.mainloop()
