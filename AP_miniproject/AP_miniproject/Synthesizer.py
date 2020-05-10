import random
import numpy as np


class Synthesizer:
    samplerate = 44100
    def makeSomeNoise(self, amplitude, duration):
        return [(random.uniform(-amplitude, amplitude)) for _ in range(int(self.samplerate * duration))]

    def genKarplusStrong(self, NoiseBurst, freq, decay):
        print("Applying Karplus Strong")
        delay = int(self.samplerate / freq)
        decay = float(np.clip(0, 1, float(decay)))
        output = NoiseBurst
        for idx in range(delay, len(output)):
            output[idx] = decay * 0.5 * (output[idx - delay] + output[idx - delay - 1])

        
        return output
    def makeGString(self, duration, amplitude, freq, decay):
        print(freq)
        return self.genKarplusStrong(self.makeSomeNoise(amplitude, duration), freq, decay)

    def fullWaveRectifier(self, input):
        output = input
        for idx in range(len(output)):
            if output[idx] < 0:
                output[idx] = output*-1
        return output

    def halfWaveRectifier(self, input):
        output = input
        for idx in range(len(output)):
            if output[idx] < 0:
                output[idx] = 0
        return output

    def infClipping(self, input):
        output = input
        for idx in range(len(output)):
            if output[idx] < 0:
                output[idx] = -1
            else:
                output[idx] = 1
        return output

    def hardClipping(self, input, threshold):
        output = input
        for idx in range(len(output)):
            if output[idx] < (threshold*-1):
                output[idx] = threshold*-1
            elif output[idx] > threshold:
                output[idx] = threshold
            else:
                output[idx] = output[idx]
        return output

    def softClipping(self, input, distortion):
        output = input
        for idx in range(len(output)):
            output[idx] = (2/np.pi)*np.arctan(distortion*output[idx])


