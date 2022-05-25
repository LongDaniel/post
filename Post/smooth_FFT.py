from scipy.fftpack import fft, fftfreq, ifft
import numpy as np

def smooth_FFT(X):
    X_hat = np.absolute(fft(X))
    return X_hat

def freq_FFT(X,d):
    freq = np.abs(fftfreq(X, d))
    return freq

