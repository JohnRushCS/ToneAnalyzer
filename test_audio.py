import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt
from aubio import source, pitch

filename = 'pian1.wav'

chunk = 2048/4

downsample = 1
samplerate = 44100 // downsample

win_s = 4096*2 // downsample # fft size
hop_s = 512  // downsample # hop size

s = source(filename, samplerate, hop_s)
samplerate = s.samplerate

tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)
pitch_o.set_silence(-50)

pitches = []
confidences = []

# total number of frames read
total_frames = 0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    print(pitch_o.get_silence())
    #pitch = int(round(pitch))
    confidence = pitch_o.get_confidence()
    if confidence < 0.8: 
        continue
    print("%f %f %f" % (total_frames / float(samplerate), pitch, confidence))
    pitches += [pitch]
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

# open up a wave
wf = wave.open(filename, 'rb')
swidth = wf.getsampwidth()
RATE = wf.getframerate()
# use a Blackman window
window = np.blackman(chunk)
# open stream
p = pyaudio.PyAudio()
stream = p.open(format =
                p.get_format_from_width(wf.getsampwidth()),
                channels = wf.getnchannels(),
                rate = RATE,
                output = True)

# read some data
data = wf.readframes(chunk)
# play stream and find the frequency of each chunk
freqs = []
total_pts = 0
total_p = []
while len(data) == chunk*swidth:
    # write data out to the audio stream
    stream.write(data)
    # unpack the data and times by the hamming window
    indata = np.array(wave.struct.unpack("%dh"%(len(data)/swidth),\
                                         data))*window
    # Take the fft and square each value
    power = np.fft.fft(indata)
    n = len(indata)

    nUniquePts = int(np.ceil((n+1)/2.0))
    total_pts += nUniquePts
    power = power[0:nUniquePts]
    power = abs(power)

    if n % 2 > 0:
        power[1:len(power)] = power[1:len(power)] * 2
    else:
        power[1:len(power) -1] = power[1:len(power) - 1] * 2

    total_p = np.hstack((total_p, power))

    fftData=abs(np.fft.rfft(indata))**2
    # find the maximum
    which = fftData[1:].argmax() + 1
    # use quadratic interpolation around the max
    if which != len(fftData)-1:
        y0,y1,y2 = np.log(fftData[which-1:which+2:])
        x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
        # find the frequency and output it
        thefreq = (which+x1)*RATE/chunk
        print "The freq is %f Hz." % (thefreq)
    else:
        thefreq = which*RATE/chunk
        print "The freq is %f Hz." % (thefreq)
    if thefreq > 100 and thefreq < 1000:
        freqs.append(thefreq)
    # read some more data
    data = wf.readframes(chunk)
if data:
    stream.write(data)
stream.close()
p.terminate()
# plt.plot(freqs)
# plt.plot(pitches)
plt.plot(total_p)
plt.show()
