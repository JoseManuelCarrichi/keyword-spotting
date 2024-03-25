from EliminarSilencios import VAD
from FiltroPasaBanda import filtrarAudio, graficarTramas, graficarFiltro



#Path del audio que quieres segmentar (sin diagonal al final)
AudioFile = ''
# Path de la carpeta donde quieres guardar los segmentos obtenidos
PathSalida = ''
# Numero de muestras que quieres adelantar
nMuestras = 500


# Filtrar audio
#path_Output = filtrarAudio(AudioFile,PathSalida)

# Graficar audios 
#graficarTramas(AudioFile, path_Output)z
#graficarFiltro(AudioFile,path_Output)

# Eliminar Silencios y detectar voz
#VAD(path_Output)
#VAD(AudioFile) 

# Filtrar y segmentar
VAD(filtrarAudio(AudioFile,PathSalida), PathSalida, nMuestras)

