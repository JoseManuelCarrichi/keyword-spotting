import matplotlib.pyplot as plt
import numpy as np
import soundfile as sf

def VAD(filePath,PathSalida,nMuestras):
    # Verificar canales de audio
    infoAudio = sf.info(filePath)
    if(infoAudio.channels == 2):
        # Lectura del audio
        Audio_, sample_rate = sf.read(filePath) 
        Audio = Audio_[:,0]
    else:
        # Lectura del audio
        Audio, sample_rate = sf.read(filePath) 
    
    #tam = len(Audio)
    yn = Audio**2 # Calcular la energía de la señal
    yne = np.log(yn) # Pasar a escala logarítmica
    yneAux = np.copy(yne)
    yneAux[np.isneginf(yne)] = np.nan # Busca valores en -inf y los asigna como Not as Number
    minimo = np.nanmin(yneAux) # Busca el valor mínimo en la señal
    yne[np.isneginf(yne)] = minimo # En aquellos puntos donde asigno NAN, coloca el mínimo
    
    del yneAux, minimo # Elimina las variables
    aux = np.max(yne)
    aux1 = np.min(yne) + 17
    YnenNoise = yne[np.where(yne <= aux1)[0]]
    
    
    plt.figure()
    plt.title('Señal de entrada excluyendo los mínimos')
    plt.plot(YnenNoise)
    plt.show()
    
    hyne, _ = np.histogram(YnenNoise, bins=10) #Obtiene el histograma de la señal
    
    Ind1, Ind2, Ind3 = np.argsort(hyne)[-3:]
    
    #Graficar el histograma
    plt.figure()
    plt.plot(hyne,color='green')
    plt.bar(range(len(hyne)),hyne)
    plt.title('Histograma inicial')
    plt.show()
    
    hyne[Ind1] = 0
    
    #Graficar el histograma
    plt.figure()
    plt.plot(hyne,color='green')
    plt.bar(range(len(hyne)),hyne)
    plt.title('Histograma sin el 1er valor más repetido')
    plt.show()
    
    hyne[Ind2] = 0
    
    #Graficar el histograma
    plt.figure()
    plt.plot(hyne,color='green')
    plt.bar(range(len(hyne)),hyne)
    plt.title('Histograma sin el 2do valor más repetido')
    plt.show()
    
    hyne[Ind3] = 0
    
    
    #Graficar el histograma
    plt.figure()
    plt.plot(hyne,color='green')
    plt.bar(range(len(hyne)),hyne)
    plt.title('Histograma modificado')
    plt.show()
    
    # Encontrar los valores de los índices maximos
    Q = ((-((10 - Ind1) + 0.5) + aux1)+ (-((10 - Ind2) + 0.5) + aux1)+ (-((10 - Ind3) + 0.5) + aux1)) / 3
    
    audio = Q +aux
    #k3 = (Q - (audio*(0.375/3)))+1
    #k3 = (Q - (audio*(0.375/1.6)))
    #k3 = (Q - (audio*(0.375/2.3)))
    k3 = (Q - (audio*(0.375/2)))
   
    
    plt.figure()
    plt.plot(yne)
    plt.axhline(k3)
    plt.title('Señal en escala logaritmica vs umbral')
    plt.show()
    
    Humbralk3 = np.zeros(len(Audio))
    Humbralk3[yne>=k3] = 1 # Los valores que superan el humbral se colocan en 1
    
    r = np.where(Humbralk3 == 1)[0]
    aux = len(r)
    contador = 1
    for s in range(aux - 1):
        if (r[s + 1] - r[s]) <= 7500:
            Humbralk3[r[s]:r[s + 1] + 1] = 1 
            #sf.write(f'Output_Audio/segmento {contador}.wav',Humbralk3[r[s]:r[s + 1] + 1],sample_rate)
            #contador += 1
            

    AudioAux = np.copy(Audio) 
    AudioAux[Humbralk3 == 0] = 0
    
    fig, ax = plt.subplots(figsize=(16, 8), dpi=600)  
    plt.plot(Audio,linewidth = 0.1, color = 'lightgray')
    plt.plot(AudioAux,linewidth = 0.1, color ='blue')
    plt.title('Segmentos de audio')
    #plt.savefig('Segmentos.png',dpi = 600)
    plt.show()
    #AudioAux contiene los segmentos de interés
    
    # Graficar el humbralk3
    plt.figure()
    plt.plot(Humbralk3,linewidth=0.5)
    plt.title('Vector de la señal recuperada sobre el Humbral')
    plt.show()
    
    AudioClean = Audio[Humbralk3 > 0]
    
    fig, ax = plt.subplots(dpi=600)
    plt.plot(AudioClean,linewidth=0.1, color = 'blue')
    plt.title('Audio sin silencios')
    #plt.savefig('AudioSinSilencios.png',dpi = 600)
    plt.show()
    
    #plt.figure()
    fig, ax = plt.subplots(figsize=(16, 8), dpi=600)
    plt.plot(Audio,linewidth=0.1, color ='blue')
    plt.plot(Humbralk3,linewidth=0.5, color = 'red')
    plt.title('Regiones vocalizadas')
    #plt.savefig('RegionesVocalizadas.png',dpi = 600)
    plt.show()
    
    r = np.where(np.diff(Humbralk3) == 1)[0] + 1
    print(r)
    contador = 1
    for s in range(len(r)):
        inicio = r[s] - nMuestras
        print(f"Original: {r[s]}   Adelantado: {r[s]-300}")
        fin = len(Humbralk3) if s == len(r) - 1 else r[s + 1]
        segmento = Audio[inicio:fin]
        print(len(segmento))
        if len(segmento) > 0:
            sf.write(PathSalida + f'/segmento_{contador}.wav', segmento, sample_rate)
            print(f"Segmento {contador}")
            contador += 1
       
    
    # Guardar el audio final
    sf.write(PathSalida + '/Voice_without_silence.wav',AudioClean,sample_rate)
