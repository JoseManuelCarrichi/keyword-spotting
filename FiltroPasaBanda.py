import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter, freqz

def generarCoeficientes():
    # Filtro Pasa banda
    Fss = 44100 / 2  # Frecuencia de muestreo y Normalización
    N = 100  # Filtro de orden 100
    Flow = 300  # Frecuencia de corte baja
    Fhigh = 3800  # Frecuencia de corte alta
    Low = Flow / Fss
    High = Fhigh / Fss
    win = np.hamming(N)  # Tipo de ventana
    Coef = firwin(N, [Low, High], pass_zero=False) * win  # Filtro pasa banda
    plt.figure()
    plt.plot(Coef)
    plt.title('Coeficientes del filtro')
    plt.show()
    
    np.save('CoeficientesFPB.npy', Coef)  # Guardar los coeficientes en un archivo numpy

def filtrarAudio(filePath,PathSalida):
    # Cargar coeficientes
    win = np.load('CoeficientesFPB.npy')
    # Verificar el número de canales del audio
    info = sf.info(filePath)    
    if(info.channels == 2):
        # Cargar audio
        Audio_,sample_rate = sf.read(filePath)
        Audio = Audio_[:,0]
    else:
        # Cargar audio
        Audio,sample_rate = sf.read(filePath)
    
    
    AudioFiltrado = lfilter(win, 1, Audio)
    output_FilePath = PathSalida+'/AudioFiltrado.wav'
    sf.write(output_FilePath,AudioFiltrado,sample_rate)
    return output_FilePath

def graficarFiltro(originalFile,filteredFile):
    Fss = 44100 / 2  # Frecuencia de muestreo y Normalización
    N = 100  # Filtro de orden 100
    # Cargar coeficientes
    win = np.load('CoeficientesFPB.npy')
    frequencies, magnitude_response = freqz(win, worN=8000, fs=Fss)

    # Graficar la respuesta en magnitud
    fig, ax = plt.subplots(figsize=(16, 8), dpi=600)
    plt.plot(frequencies, 20 * np.log10(np.abs(magnitude_response)),linewidth = 1)
    plt.title('Respuesta en Magnitud del Filtro')
    plt.xlabel('Frecuencia (Hz)')
    plt.ylabel('Magnitud (dB)')
    plt.grid(True)
    plt.savefig("MagnitudFiltro.png", dpi=600)
    plt.show()
    
    # Abrir archivos
    original_Audio,sample_rate = sf.read(originalFile)
    filtered_Audio,sample_rate2 = sf.read(filteredFile)
    # Visualización de espectros
    fig, ax = plt.subplots(figsize=(16, 8), dpi=600)
    plt.plot(20 * np.log10(np.abs(np.fft.fft(original_Audio))),linewidth = 0.5)
    plt.plot(20 * np.log10(np.abs(np.fft.fft(filtered_Audio))),linewidth = 0.5)
    plt.title('Espectro de potencia')
    plt.legend(['Original', 'Filtrada'])
    plt.savefig("EspectroPotencia.png", dpi=600)
    plt.show()

def graficarTramas(originalFile,filteredFile):
    # Abrir Audio original
    original_Audio,sample_rate = sf.read(originalFile)
    
    fig, ax = plt.subplots(figsize=(16, 8), dpi=600)
    plt.plot(original_Audio,color='blue',linewidth=0.1)
    plt.title("Señal original")
    plt.savefig('AudioOriginal.png',dpi = 600)
    plt.show()
    
    # Abrir Audio Filtrado
    filtered_Audio,sample_rate2 = sf.read(filteredFile)
    
    fig, ax = plt.subplots(figsize=(16, 8), dpi=600)
    plt.plot(filtered_Audio,color='blue',linewidth=0.1)
    plt.title("Señal filtrada")
    plt.savefig('AudioFiltrado.png',dpi = 600)
    plt.show()
    
    fig, ax = plt.subplots(figsize=(16, 8), dpi=600)
    plt.plot(original_Audio,color='blue',linewidth=0.1)
    plt.plot(filtered_Audio,color='red',linewidth=0.1)
    plt.title("Señal original vs. Señal filtrada")
    plt.savefig('AudioOriginal_Filtrado.png',dpi = 600)
    plt.show()

