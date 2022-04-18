import gc
import math
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import scipy.signal
from IPython.display import Audio, display

def play(x, fs, autoplay=False):
    ''' Output an audio player that allows participants to listen to their wav files '''
    display(Audio(x, rate=fs, autoplay=autoplay))
    
    
def norm(wav):
    ''' Normalization function '''
    return wav/np.max(np.abs(wav))

def dco(wav):
    ''' Remove DC offset and normalize the signal '''
    return norm(wav - np.mean(wav))

def extract(wav, t1, t2, fs):
    ''' Extract a portion of the input signal from t1 to t2 '''
    if isinstance(t1, str) and t1 == 'start':
        cut = wav[:math.floor(t2*fs)]
    elif isinstance(t2, str) and t2 == 'end':
            cut = wav[math.floor(t1*fs):]
    else:
        cut = wav[math.floor(t1*fs):math.floor(t2*fs)]
    tcut = np.arange(len(cut))*(1./fs)
    return cut, tcut

def crosscorrelate(signal, template, fs):
    '''Cross-correlate the template against the signal'''
    Rxy = scipy.signal.correlate(signal, template, mode='valid')
    t = np.arange(len(Rxy))*(1./fs)
    return Rxy, t

def plot_signal(time_vec,x_0,xlim=None,title=None):
    ''' Plot the signal in the time doman'''
    
    fig = plt.figure(figsize=(15,12))

    ax = fig.add_subplot(2,1,1)
    ax.plot(time_vec,x_0)
    ax.set_xticklabels([])
    ax.set_ylabel('x(t)')
    ax.set_xlim(xlim)
    ax.set_title(title)

    ax = fig.add_subplot(2,1,2)
    samplerate = 1./(time_vec[1]-time_vec[0])
    ax.specgram(x_0,Fs=samplerate)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Hz')
    ax.set_xlim(xlim)
    #ax.set_ylim(0,5000)

    fig.tight_layout()
    plt.show()
    plt.close(fig)
    
    gc.collect()

def plot_correlation(tau, Rxy, title = None, return_figure=False):
    '''Plot cross-correlation values Rxy at time points tau.'''
    fig = plt.figure(figsize=(15,6))
    
    ax = fig.add_subplot(1,1,1)
    ax.plot(tau, Rxy)
    ax.set_xlabel('Tau [s]')
    ax.set_ylabel('$R_{XY}$')
    ax.set_title(title)
    
    plt.show()
    plt.close(fig)
    
    if return_figure:
        return fig
    
    gc.collect()

def plot_correlation_interactive(tau, Rxy, title = None):
    '''Plot cross-correlation interactively and highlight peaks.'''
    
    sample_rate = len(tau)/(tau[-1] - tau[0]) # assuming equally-spaced samples
    
    # require peaks that at at least .01 seconds apart (assuming sample rate is in seconds)
    indices = scipy.signal.find_peaks(Rxy, prominence=(np.max(Rxy)/4), distance=.01 * sample_rate)[0]
    R_peaks = [Rxy[i] for i in indices]
    t_peaks = [tau[i] for i in indices]
    print(f'Peaks found at {t_peaks}')
    
    fig = go.FigureWidget([go.Scatter(x=tau, y=Rxy, mode='lines'),
                          go.Scatter(x=t_peaks,
                                     y=R_peaks,
                                    mode='markers',
                                    marker=dict(size=8,color='red',symbol='cross'))])
    fig.layout.title = title
    fig.show()
    
    return R_peaks, t_peaks

def find_timing_of(template, signal, fs):
    '''Find the timing of the given test signal (template) in the given signal recording'''
    Rxy, tau = crosscorrelate(signal, template, fs)
    return np.where(np.abs(Rxy) == np.max(np.abs(Rxy)) )[0][0] * (1./fs)