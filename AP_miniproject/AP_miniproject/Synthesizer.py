import random
import numpy as np
import math

class Timbre():
        sinusoidCycle = 0
        squareCycle = 1
        sawtoothCycle = 2
        whiteNoiseCycle = 3
        sinusoidSweep = 4

class Synthesizer:
    samplerate = 44100

    def __init__(self, samplerate = 44100):
        self.samplerate = samplerate

    def _wave(self, cycle, duration):
        return cycle * int((self.samplerate / len(cycle)) * duration)

    #sinusoid
    def sinusoidCycle(self, amplitude, wavelength):
        return [(math.sin((x / wavelength) * (2 * math.pi))) for x in range(int(wavelength))]

    def sinusoidWave(self, amplitude, frequency, duration):
        return self._wave(self.sinusoidCycle(amplitude, int(self.samplerate / frequency)),duration)

    def sinusoidSweepSamples(self, amplitude, startFrequency, endFrequency, samples):
        frequencyStep = (endFrequency - startFrequency) / int(samples)
        return [(math.sin((x / (self.samplerate / ((frequencyStep*x)+startFrequency))) * (2 * math.pi))) for x in range(int(samples))]

    def sinusoidSweepDuration(self, amplitude, startFrequency, endFrequency, duration):
        return self.sinusoidSweepSamples(amplitude, startFrequency, endFrequency, int(duration * self.samplerate))

    #square
    def squareCycle(self, amplitude, wavelength):
        return [(1 if (x < wavelength * 0.5) else -1) for x in range(int(wavelength))]

    def squareWave(self, amplitude, frequency, duration):
        return self._wave(self.squareCycle(amplitude, int(self.samplerate / frequency)), duration)

    #sawtooth
    def sawtoothCycle(self, amplitude, wavelength):
        return [(x * amplitude) for x in range(int(wavelength))]

    def sawtoothWave(self, amplitude, frequency, duration):
        return self._wave(self.sawtoothCycle(amplitude, int(self.samplerate / frequency)), duration)

    #whiteNoise
    def whiteNoiseCycle(self, amplitude, wavelength):
        return [(random.uniform(-amplitude, amplitude)) for _ in range(int(wavelength))]

    def whiteNoiseWave(self, amplitude, wavelength):
        return self._wave(self.whiteNoiseWave(amplitude, int(self.samplerate / frequency)), duration)

    #Guitar
    def genKarplusStrong(self, NoiseBurst, freq, decay, silence):
        print("[Synthesizer.genKarplusStrong] freq: " + str(freq) + ", decay: " + str(decay))
        delay = int(self.samplerate / freq)
        decay = float(np.clip(0, 1, float(decay)))
        output = NoiseBurst
        output.extend([0]*int(silence*self.samplerate))
        for idx in range(delay, len(output)):
            output[idx] = decay * 0.5 * (output[idx - delay] + output[idx - delay - 1])
        return output


    def makeGString(self, silence, amplitude, frequency, decay, timbre):
        print("[Synthesizer.makeGString]")
        if timbre == Timbre.sinusoidCycle:
            return self.genKarplusStrong(self.sinusoidCycle(amplitude, self.samplerate/frequency), frequency, decay, silence)
        elif timbre == Timbre.squareCycle:
            return self.genKarplusStrong(self.squareCycle(amplitude, self.samplerate/frequency), frequency, decay, silence)
        elif timbre == Timbre.sawtoothCycle:
            return self.genKarplusStrong(self.sawtoothCycle(amplitude, self.samplerate/frequency), frequency, decay, silence)
        elif timbre == Timbre.whiteNoiseCycle:
            return self.genKarplusStrong(self.whiteNoiseCycle(amplitude, self.samplerate/frequency), frequency, decay, silence)
        elif timbre == Timbre.sinusoidSweep:
            return self.genKarplusStrong(self.sinusoidSweepSamples(amplitude, 20, 20000, self.samplerate/frequency), frequency, decay, silence)

    #Disotrion
    def fullWaveRectifier(self, input):
        print("[Synthesizer.fullWaveRectifier]")
        output = input
        for idx in range(len(output)):
            if output[idx] < 0:
                output[idx] = output[idx] * -1
        return output

    def halfWaveRectifier(self, input):
        print("[Synthesizer.halfWaveRectifier]")
        output = input
        for idx in range(len(output)):
            if output[idx] < 0:
                output[idx] = 0
        return output

    def infClipping(self, input):
        print("[Synthesizer.infClipping]")
        output = input
        for idx in range(len(output)):
            if output[idx] < 0:
                output[idx] = -1
            else:
                output[idx] = 1
        return output

    def hardClipping(self, input, threshold):
        print("[Synthesizer.hardClipping] threshold: " + str(threshold))
        output = input
        for idx in range(len(output)):
            if output[idx] < (threshold * -1):
                output[idx] = threshold * -1
            elif output[idx] > threshold:
                output[idx] = threshold
            else:
                output[idx] = output[idx]
        return output

    def softClipping(self, input, distortion):
        print("[Synthesizer.softClipping] distortion: " + str(distortion))
        output = input
        for idx in range(len(output)):
            output[idx] = (2 / np.pi) * np.arctan(distortion * output[idx])
        return output


