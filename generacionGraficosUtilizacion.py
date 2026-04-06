"""PROGRAMA DE CREACIÓN DE GRÁFICAS DE UTILIZACIÓN DE APOYOS EN ALTA TENSIÓN
Yure Wagemann Valadares Magalhães

Este programa genera la gráfica de utilización de los apoyos de líneas de Alta Tensión.
[VERSIÓN DE ESTUDIO - BETA] Algunas fórmulas están desactivadas para depuración en clase.

El programa traza las rectas de las diferentes hipótesis de carga (viento, hielo, etc.), el límite del vano máximo y la restricción por 
inclinación de la cadena de aisladores.
Además, inserta el punto del apoyo específico en la gráfica con la sección 4 (valores especificos de L y N).
Se puede configurar el límite del eje x (L) a partir de la ventana, en la sección 5 (valor de 500m por defecto)."""

# Importación de librerías necesarias
import tkinter as tk  # interfaz de usuario (GUI)
from tkinter import ttk  # botones extras
from tkinter import messagebox  # ventanas de alerta o error
from tkinter import filedialog  # Para abrir el explorador y guardar la imagen generada
from matplotlib.figure import Figure  # dibujar gráficos matemáticos
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # para que yo consiga utilizar Matplotlib en Tkinter
import numpy as np  # Matemática necesaria para los cálculos 


# VARIABLES GLOBALES 
# Usamos variables globales para el lienzo y los ejes para poder borrarlos y redibujarlos cada vez que el usuario pulse el botón de "Generar Gráfica".
lienzoGrafico = None  
ejesGrafico = None  

# Aquí las funciones que utilizo en el código principal, así se queda mejor separado (todas las "def").

def leerNumeroSeguro(casillaTexto):
    # Lee el texto que el usuario ha escrito en la interfaz. limpia espacios, cambia comas por puntos
    textoIngresado = casillaTexto.get().strip()
    
    # Si la casilla está vacía, detenemos el cálculo aquí devolviendo None
    if not textoIngresado:  
        return None 
    
    # Preparamos el texto para que Python lo entienda
    textoLimpio = textoIngresado.replace(',', '.')   # Cambiamos coma por punto
    textoLimpio = textoLimpio.replace(';', '.')      # Por si el usuario teclea mal
    try:
        valorDecimal = float(textoLimpio)
        return valorDecimal
    except ValueError:  
        # Si el usuario escribió letras o algo ilegible, devolvemos None 
        return None 


def aplicarEstiloEjes(ejes, limiteVanoX):
    # Configura el visual y  límites de la gráfica. Fija el eje Y (Utilización N) en -1 y 1.
    ejes.set_title("Gráfica de utilización")  
    ejes.set_xlabel("Vano L (metros)")  
    ejes.set_ylabel("Utilización N")  
    
    # Límites de la gráfica
    ejes.set_xlim(0, limiteVanoX)  
    ejes.set_ylim(-1, 1)  
    
    # Eje Y con intervalo de 0.1
    marcasEjeY = np.round(np.arange(-1.0, 1.1, 0.1), 1)  
    ejes.set_yticks(marcasEjeY)  
    
    # Adaptamos la separación de las líneas del eje X (si menor que 600 m, cada 50 m hay una marca. Si mayor, cada 100 metros).
    if limiteVanoX < 600:  
        ejes.set_xticks(np.arange(0, limiteVanoX + 1, 50))  
    else:  
        ejes.set_xticks(np.arange(0, limiteVanoX + 1, 100)) 
        
    #  rejilla de fondo
    ejes.grid(True, linestyle=':', alpha=0.7)  


def arrancarGraficaEnBlanco(panelContenedor):
    global lienzoGrafico, ejesGrafico  
    
    # Creamos la figura y ajustamos el espacio para que la leyenda quepa a la derecha
    figuraPrincipal = Figure(figsize=(6, 4.8), dpi=100)  
    figuraPrincipal.subplots_adjust(bottom=0.25, right=0.75) 
    
    # ejes y su estilo inicial (vano de 500 m en el inicio, por defecto)
    ejesGrafico = figuraPrincipal.add_subplot(111)  
    aplicarEstiloEjes(ejesGrafico, 500)  
    
    # Ponemos la figura en la ventana de Tkinter
    lienzoGrafico = FigureCanvasTkAgg(figuraPrincipal, master=panelContenedor)  
    lienzoGrafico.draw()  
    lienzoGrafico.get_tk_widget().pack(fill=tk.BOTH, expand=True)  


def ejecutarTrazadoGrafica():
    # Aquí leo todos los datos introducidos, realizo los trazados en la gráfica de utilización y la leyenda.
    try:
        # 1. Definir el límite visual del Vano (Eje X)
        valorLimiteX = leerNumeroSeguro(casillaLimiteX)  
        if valorLimiteX is None:  
            messagebox.showerror("Error", "Introduce un valor válido para L máximo.")
            return

        # Limpiamos el dibujo anterior 
        ejesGrafico.clear()  
        aplicarEstiloEjes(ejesGrafico, valorLimiteX)  
        
        # Variable de control: si no dibujamos nada, no mostraremos la leyenda
        seHanDibujadoLineas = False  

        # 2. Trazado de las Hipótesis de Cálculo (Viento, Hielo, etc.)
        configuracionHipotesis = [
            (casillaHip1NMenos1, casillaHip1N1, 'red', 'Hipótesis 1'),
            (casillaHip2NMenos1, casillaHip2N1, 'purple', 'Hipótesis 2'),
            (casillaHip2VHNMenos1, casillaHip2VHN1, 'dodgerblue', 'Hipótesis 2 (V-H)'),
            (casillaHip3NMenos1, casillaHip3N1, 'orange', 'Hipótesis 3')
        ]

        for casillaNMenos1, casillaN1, colorLinea, nombreEtiqueta in configuracionHipotesis:
            vanoParaNMenos1 = leerNumeroSeguro(casillaNMenos1) 
            vanoParaN1 = leerNumeroSeguro(casillaN1)  
            
            if vanoParaNMenos1 is not None and vanoParaN1 is not None:
                ejesGrafico.plot([vanoParaNMenos1, vanoParaN1], [-1, 1], color=colorLinea, linewidth=2, label=nombreEtiqueta)
                seHanDibujadoLineas = True

        # 3. Trazado del Límite Estructural: Vano Máximo
        valorVanoMaximo = leerNumeroSeguro(casillaVanoMaximoL)
        if valorVanoMaximo is not None:
            if valorVanoMaximo <= valorLimiteX: 
                # TODO: Aquí falta la función de Matplotlib para trazar la línea vertical verde del Vano Máximo
                # Pista: investigar sobre 'axvline'
                pass 

        # 4. Trazado de la Restricción: Desviación de Cadena de Aisladores
        valorCadenaNOrigen = leerNumeroSeguro(casillaCadenaNOrigen)
        valorCadenaLSegundo = leerNumeroSeguro(casillaCadenaL2)
        valorCadenaNSegundo = leerNumeroSeguro(casillaCadenaN2)

        if valorCadenaNOrigen is not None and valorCadenaLSegundo is not None and valorCadenaNSegundo is not None:
            if valorCadenaLSegundo != 0:
                # TODO: Falta calcular la pendiente geométrica de la recta (m)
                # ¿Cuál es la fórmula matemática para calcular la pendiente entre dos puntos (X1,Y1) y (X2,Y2)?
                pendienteRecta = 0 # Corregir este 0 por la fórmula real
                
                # Proyectamos la recta hasta el final del gráfico para que se vea completa
                valorNAlFinalDelGrafico = valorCadenaNOrigen + (pendienteRecta * valorLimiteX)
                
                ejesGrafico.plot([0, valorLimiteX], [valorCadenaNOrigen, valorNAlFinalDelGrafico], color='blue', linewidth=2, label='Desviación Cadena')
                seHanDibujadoLineas = True

        
        # 6. Leyenda
        if seHanDibujadoLineas:
            ejesGrafico.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=1)  
        
        lienzoGrafico.draw()  
        
    except Exception as errorEncontrado:
        messagebox.showerror("Error", f"Fallo al procesar el cálculo: {errorEncontrado}")


def ejecutarExportacionImagen():
    # Guarda el estado actual del gráfico como JPG, o sea, una exportación del gráfico.
    if lienzoGrafico is None:
        return 
        
    rutaGuardado = filedialog.asksaveasfilename(
        defaultextension=".jpg",
        filetypes=[("Archivos de imagen JPG", "*.jpg"), ("Todos los archivos", "*.*")],
        title="Guardar gráfica de utilización como..."
    )
    
    if rutaGuardado:
        try:
            lienzoGrafico.figure.savefig(rutaGuardado, format='jpg', dpi=300, facecolor='white', bbox_inches='tight')
            messagebox.showinfo("Éxito", "Gráfica guardada correctamente.")
        except Exception as errorExportacion:
            messagebox.showerror("Error", f"No se pudo guardar la gráfica: {errorExportacion}")


def abrirModuloAsistenteEcuaciones():
    ventanaAsistente = tk.Toplevel(ventanaPrincipal) 
    ventanaAsistente.title("Asistente de Ecuaciones")
    
    posicionX = ventanaPrincipal.winfo_x() + 450
    posicionY = ventanaPrincipal.winfo_y() + 80
    ventanaAsistente.geometry(f"620x480+{posicionX}+{posicionY}")
    
    ventanaAsistente.calculoFinalizado = False 
    
    marcoContenedor = ttk.Frame(ventanaAsistente, padding="20")
    marcoContenedor.pack(fill=tk.BOTH, expand=True)
    
    # 1. Primera Hipótesis
    ttk.Label(marcoContenedor, text="Primera hipótesis:", font=fuenteTitulos).grid(row=0, column=0, sticky=tk.W, pady=5)
    ttk.Label(marcoContenedor, text="").grid(row=0, column=1, padx=5) 
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip1_A']).grid(row=0, column=2) 
    ttk.Label(marcoContenedor, text=" L  + ").grid(row=0, column=3)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip1_B']).grid(row=0, column=4) 
    ttk.Label(marcoContenedor, text=" N  + ").grid(row=0, column=5)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip1_C']).grid(row=0, column=6) 
    ttk.Label(marcoContenedor, text=" =  0").grid(row=0, column=7)

    # 2. Segunda Hipótesis Hielo
    
    # 3. Segunda Hipótesis (V-H)
    ttk.Label(marcoContenedor, text="Segunda hipótesis (V-H):", font=fuenteTitulos).grid(row=2, column=0, sticky=tk.W, pady=5)
    ttk.Label(marcoContenedor, text="").grid(row=2, column=1)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip2VH_A']).grid(row=2, column=2)
    ttk.Label(marcoContenedor, text=" L  + ").grid(row=2, column=3)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip2VH_B']).grid(row=2, column=4)
    ttk.Label(marcoContenedor, text=" N  + ").grid(row=2, column=5)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip2VH_C']).grid(row=2, column=6)
    ttk.Label(marcoContenedor, text=" =  0").grid(row=2, column=7)

    # 4. Tercera Hipótesis
    ttk.Label(marcoContenedor, text="Tercera hipótesis:", font=fuenteTitulos).grid(row=3, column=0, sticky=tk.W, pady=5)
    ttk.Label(marcoContenedor, text="").grid(row=3, column=1)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip3_A']).grid(row=3, column=2)
    ttk.Label(marcoContenedor, text=" L  + ").grid(row=3, column=3)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip3_B']).grid(row=3, column=4)
    ttk.Label(marcoContenedor, text=" N  + ").grid(row=3, column=5)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['hip3_C']).grid(row=3, column=6)
    ttk.Label(marcoContenedor, text=" =  0").grid(row=3, column=7)

    ttk.Separator(marcoContenedor, orient='horizontal').grid(row=4, column=0, columnspan=8, sticky="ew", pady=10)

    # 5. Vano Máximo 
    ttk.Label(marcoContenedor, text="Vano Máximo:", font=fuenteTitulos).grid(row=5, column=0, sticky=tk.W, pady=5)
    ttk.Label(marcoContenedor, text="L = ").grid(row=5, column=1, sticky=tk.E)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['vanoMaximoAsistente']).grid(row=5, column=2, sticky=tk.W)

    ttk.Separator(marcoContenedor, orient='horizontal').grid(row=6, column=0, columnspan=8, sticky="ew", pady=10)

    # 6. Desviación de Cadena 
    
    ttk.Label(marcoContenedor, text="").grid(row=8, column=1) 
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['cadena_A']).grid(row=8, column=2, pady=5)
    ttk.Label(marcoContenedor, text=" L  + ").grid(row=8, column=3)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['cadena_B']).grid(row=8, column=4)
    ttk.Label(marcoContenedor, text=" N  + ").grid(row=8, column=5)
    ttk.Entry(marcoContenedor, width=8, textvariable=variablesAsistente['cadena_C']).grid(row=8, column=6)
    ttk.Label(marcoContenedor, text=" =  0").grid(row=8, column=7)
    
    # 7. Área de Botones
    marcoBotones = ttk.Frame(marcoContenedor)
    marcoBotones.grid(row=9, column=0, columnspan=8, pady=(20, 10))
    
    textoInformativo = "Nota: Observe el signo del término independiente de las ecuaciones.\nSi es negativo, inclúyalo en el campo (ejemplo: -3500)."
    ttk.Label(marcoContenedor, text=textoInformativo, font=('Segoe UI', 9, 'italic'), foreground="#555555", justify=tk.CENTER).grid(row=10, column=0, columnspan=8, pady=5)

    def ejecutarCalculoEcuaciones():
        try:
            def extraerValorDecimal(variableString):
                texto = variableString.get().strip()
                if not texto: return None
                texto = texto.replace(',', '.').replace(';', '.').replace(' ', '').replace('−', '-')
                try: return float(texto)
                except ValueError: return None
            
            def formatearSalidaTexto(valor, cantidadDecimales=2):
                if valor is None: return ""
                return f"{valor:.{cantidadDecimales}f}".replace('.', ',')

            def calcularPuntosHipotesis(varA, varB, varC, casillaDestinoNMenos1, casillaDestinoN1):
                valorA = extraerValorDecimal(varA)
                valorB = extraerValorDecimal(varB)
                valorC = extraerValorDecimal(varC)
                
                if valorA is not None and valorB is not None and valorC is not None and valorA != 0:
                    
                    # TODO: Aquí falta la fórmula para despejar el Vano L asumiendo que la Utilización N vale -1
                    # Ecuación origen: A*L + B*N + C = 0
                    calculoLMenos1 = None  
                    
                    # TODO: Aquí falta la fórmula para despejar el Vano L asumiendo que la Utilización N vale 1
                    calculoL1 = None  
                    
                    if calculoLMenos1 is not None:
                        casillaDestinoNMenos1.delete(0, tk.END)
                        casillaDestinoNMenos1.insert(0, formatearSalidaTexto(calculoLMenos1, 2))
                    
                    if calculoL1 is not None:
                        casillaDestinoN1.delete(0, tk.END)
                        casillaDestinoN1.insert(0, formatearSalidaTexto(calculoL1, 2))

            calcularPuntosHipotesis(variablesAsistente['hip1_A'], variablesAsistente['hip1_B'], variablesAsistente['hip1_C'], casillaHip1NMenos1, casillaHip1N1)
            calcularPuntosHipotesis(variablesAsistente['hip2_A'], variablesAsistente['hip2_B'], variablesAsistente['hip2_C'], casillaHip2NMenos1, casillaHip2N1)
            calcularPuntosHipotesis(variablesAsistente['hip2VH_A'], variablesAsistente['hip2VH_B'], variablesAsistente['hip2VH_C'], casillaHip2VHNMenos1, casillaHip2VHN1)
            calcularPuntosHipotesis(variablesAsistente['hip3_A'], variablesAsistente['hip3_B'], variablesAsistente['hip3_C'], casillaHip3NMenos1, casillaHip3N1)

            valorVanoLeido = extraerValorDecimal(variablesAsistente['vanoMaximoAsistente'])
            if valorVanoLeido is not None:
                casillaVanoMaximoL.delete(0, tk.END)
                casillaVanoMaximoL.insert(0, formatearSalidaTexto(valorVanoLeido, 2))

            # Cálculo de la Inclinación de la Cadena de Aisladores
            vanoReferencia = extraerValorDecimal(variablesAsistente['cadenaVanoReferencia'])
            valorCadenaA = extraerValorDecimal(variablesAsistente['cadena_A'])
            valorCadenaB = extraerValorDecimal(variablesAsistente['cadena_B'])
            valorCadenaC = extraerValorDecimal(variablesAsistente['cadena_C'])

            if all(variable is not None for variable in [vanoReferencia, valorCadenaA, valorCadenaB, valorCadenaC]) and valorCadenaB != 0:
                
                # TODO: Falta despejar N asumiendo que el vano es 0 (L = 0)
                # Ecuación: A*L + B*N + C = 0
                calculoNCuandoL0 = None 
                
                # TODO: Falta despejar N para el valor de L que introdujo el usuario
                calculoNCuandoLRef = None 
                
                if calculoNCuandoL0 is not None:
                    casillaCadenaNOrigen.delete(0, tk.END)
                    casillaCadenaNOrigen.insert(0, formatearSalidaTexto(calculoNCuandoL0, 4)) 
                
                casillaCadenaL2.delete(0, tk.END)
                casillaCadenaL2.insert(0, formatearSalidaTexto(vanoReferencia, 2))  
                
                if calculoNCuandoLRef is not None:
                    casillaCadenaN2.delete(0, tk.END)
                    casillaCadenaN2.insert(0, formatearSalidaTexto(calculoNCuandoLRef, 4)) 

            ventanaAsistente.calculoFinalizado = True
            messagebox.showinfo("Éxito", "Cálculo procesado. Revisa si los datos se han insertado correctamente.", parent=ventanaAsistente)
            
        except Exception as errorCálculo:
            messagebox.showerror("Error Matemático", f"Revisa los datos introducidos:\n{errorCálculo}", parent=ventanaAsistente)

    def accionCerrarSegura():
        if not ventanaAsistente.calculoFinalizado:
            respuestaUsuario = messagebox.askyesno("Confirmación", "¿Quieres realmente salir?", parent=ventanaAsistente)
            if respuestaUsuario:
                ventanaAsistente.destroy()
        else:
            ventanaAsistente.destroy()
            
    botonResolver = ttk.Button(marcoBotones, text="Resolver Sistema", command=ejecutarCalculoEcuaciones)
    botonResolver.pack(side=tk.LEFT, padx=15)
    
    botonCerrar = ttk.Button(marcoBotones, text="Cerrar Asistente", command=accionCerrarSegura)
    botonCerrar.pack(side=tk.LEFT, padx=15)
    
    ventanaAsistente.protocol("WM_DELETE_WINDOW", accionCerrarSegura)


# INICIO DE LA APLICACIÓN Y CONFIGURACIÓN DE LA VENTANA PRINCIPAL
ventanaPrincipal = tk.Tk()
ventanaPrincipal.title("Creación de gráficas de utilización de Apoyos de Alta Tensión - Yure Wagemann")

# VARIABLES DE MEMORIA DEL ASISTENTE 
variablesAsistente = {
    'hip1_A': tk.StringVar(), 'hip1_B': tk.StringVar(), 'hip1_C': tk.StringVar(),
    'hip2_A': tk.StringVar(), 'hip2_B': tk.StringVar(), 'hip2_C': tk.StringVar(),
    'hip2VH_A': tk.StringVar(), 'hip2VH_B': tk.StringVar(), 'hip2VH_C': tk.StringVar(),
    'hip3_A': tk.StringVar(), 'hip3_B': tk.StringVar(), 'hip3_C': tk.StringVar(),
    'vanoMaximoAsistente': tk.StringVar(),
    'cadenaVanoReferencia': tk.StringVar(), 
    'cadena_A': tk.StringVar(), 'cadena_B': tk.StringVar(), 'cadena_C': tk.StringVar()
}

# CONFIGURACIÓN DE PANTALLA 
anchoAplicacion = 1400
altoAplicacion = 750 
anchoMonitor = ventanaPrincipal.winfo_screenwidth()
altoMonitor = ventanaPrincipal.winfo_screenheight()

centroX = int((anchoMonitor/2) - (anchoAplicacion/2))
centroY = int((altoMonitor/2) - (altoAplicacion/2)) - 40 
if centroY < 0: centroY = 0 
ventanaPrincipal.geometry(f"{anchoAplicacion}x{altoAplicacion}+{centroX}+{centroY}")

# DISEÑO GRÁFICO (UI/UX) 
estilosVisuales = ttk.Style()
estilosVisuales.theme_use('clam') 
fuenteEstandar = ('Segoe UI', 11)
fuenteTitulos = ('Segoe UI', 11, 'bold')

estilosVisuales.configure(".", font=fuenteEstandar)
estilosVisuales.configure("TLabelframe.Label", font=fuenteTitulos, foreground="#2c3e50")
estilosVisuales.configure("TButton", font=('Segoe UI', 11, 'bold'), padding=5)

# CREACIÓN DE LAS ÁREAS DE TRABAJO 
panelControlesIzquierda = ttk.Frame(ventanaPrincipal, padding="10")
panelControlesIzquierda.pack(side=tk.LEFT, fill=tk.Y, expand=False)

panelVisualizacionDerecha = ttk.Frame(ventanaPrincipal, padding="15", relief="sunken")
panelVisualizacionDerecha.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

arrancarGraficaEnBlanco(panelVisualizacionDerecha)

# FORMULARIO DE INTRODUCCIÓN DE DATOS
# SECCIÓN 1: HIPÓTESIS REGLAMENTARIAS 
marcoHipotesis = ttk.LabelFrame(panelControlesIzquierda, text=" 1. Hipótesis de Carga (Rectas L/N) ", padding="5")
marcoHipotesis.pack(fill=tk.X, pady=2)

ttk.Label(marcoHipotesis, text="Hipótesis 1:").grid(row=0, column=0, sticky=tk.W)
ttk.Label(marcoHipotesis, text="Vano (N=-1):").grid(row=0, column=1, padx=(10, 2))
casillaHip1NMenos1 = ttk.Entry(marcoHipotesis, width=10)
casillaHip1NMenos1.grid(row=0, column=2)
ttk.Label(marcoHipotesis, text="Vano (N=1):").grid(row=0, column=3, padx=(10, 2))
casillaHip1N1 = ttk.Entry(marcoHipotesis, width=10)
casillaHip1N1.grid(row=0, column=4, sticky=tk.E)

ttk.Label(marcoHipotesis, text="Hipótesis 2:").grid(row=1, column=0, sticky=tk.W)
ttk.Label(marcoHipotesis, text="Vano (N=-1):").grid(row=1, column=1, padx=(10, 2))
casillaHip2NMenos1 = ttk.Entry(marcoHipotesis, width=10)
casillaHip2NMenos1.grid(row=1, column=2)
ttk.Label(marcoHipotesis, text="Vano (N=1):").grid(row=1, column=3, padx=(10, 2))
casillaHip2N1 = ttk.Entry(marcoHipotesis, width=10)
casillaHip2N1.grid(row=1, column=4, sticky=tk.E)

ttk.Label(marcoHipotesis, text="Hipótesis 2 (V-H):").grid(row=2, column=0, sticky=tk.W)
ttk.Label(marcoHipotesis, text="Vano (N=-1):").grid(row=2, column=1, padx=(10, 2))
casillaHip2VHNMenos1 = ttk.Entry(marcoHipotesis, width=10)
casillaHip2VHNMenos1.grid(row=2, column=2)
ttk.Label(marcoHipotesis, text="Vano (N=1):").grid(row=2, column=3, padx=(10, 2))
casillaHip2VHN1 = ttk.Entry(marcoHipotesis, width=10)
casillaHip2VHN1.grid(row=2, column=4, sticky=tk.E)

ttk.Label(marcoHipotesis, text="Hipótesis 3:").grid(row=3, column=0, sticky=tk.W)
ttk.Label(marcoHipotesis, text="Vano (N=-1):").grid(row=3, column=1, padx=(10, 2))

# SECCIÓN 2: LÍMITE ESTRUCTURAL 
marcoVano = ttk.LabelFrame(panelControlesIzquierda, text=" 2. Límite de Vano ", padding="5")
marcoVano.pack(fill=tk.X, pady=2)
marcoVano.columnconfigure(1, weight=1)
ttk.Label(marcoVano, text="Vano máximo admisible (L):").grid(row=0, column=0, sticky=tk.W)
casillaVanoMaximoL = ttk.Entry(marcoVano, width=10)
casillaVanoMaximoL.grid(row=0, column=1, sticky=tk.E)

# SECCIÓN 3: RESTRICCIÓN DE LA CADENA DE AISLADORES 
marcoCadena = ttk.LabelFrame(panelControlesIzquierda, text=" 3. Desviación de Cadena ", padding="5")
marcoCadena.pack(fill=tk.X, pady=2)
marcoCadena.columnconfigure(1, weight=1)
ttk.Label(marcoCadena, text="Utilización N (cuando Vano = 0):").grid(row=0, column=0, sticky=tk.W, pady=3)
casillaCadenaNOrigen = ttk.Entry(marcoCadena, width=10)
casillaCadenaNOrigen.grid(row=0, column=1, sticky=tk.E)

ttk.Label(marcoCadena, text="Segundo valor de Vano de prueba:").grid(row=1, column=0, sticky=tk.W, pady=3)
casillaCadenaL2 = ttk.Entry(marcoCadena, width=10)
casillaCadenaL2.grid(row=1, column=1, sticky=tk.E)

ttk.Label(marcoCadena, text="Utilización N en ese segundo Vano:").grid(row=2, column=0, sticky=tk.W, pady=3)
casillaCadenaN2 = ttk.Entry(marcoCadena, width=10)
casillaCadenaN2.grid(row=2, column=1, sticky=tk.E)

# SECCIÓN 4: PUNTO ESPECÍFICO DEL APOYO
marcoGeometria = ttk.LabelFrame(panelControlesIzquierda, text=" 4. Parámetros Específicos ", padding="5")
marcoGeometria.pack(fill=tk.X, pady=2)
marcoGeometria.columnconfigure(1, weight=1)
ttk.Label(marcoGeometria, text="Vano L con Eolovano:").grid(row=0, column=0, sticky=tk.W, pady=3)
casillaEoloVanoL = ttk.Entry(marcoGeometria, width=10)
casillaEoloVanoL.grid(row=0, column=1, sticky=tk.E)

ttk.Label(marcoGeometria, text="Valor N por diferencia de tangentes:").grid(row=1, column=0, sticky=tk.W, pady=3)
casillaTangentesN = ttk.Entry(marcoGeometria, width=10)
casillaTangentesN.grid(row=1, column=1, sticky=tk.E)

# SECCIÓN 5: CONFIGURACIÓN VALOR MÁXIMO EJE X 
marcoVisual = ttk.LabelFrame(panelControlesIzquierda, text=" 5. Configuración Visual ", padding="5")
marcoVisual.pack(fill=tk.X, pady=2)
marcoVisual.columnconfigure(1, weight=1)
ttk.Label(marcoVisual, text="Límite máximo a dibujar (Eje X):").grid(row=0, column=0, sticky=tk.W)
casillaLimiteX = ttk.Entry(marcoVisual, width=10)
casillaLimiteX.grid(row=0, column=1, sticky=tk.E)
casillaLimiteX.insert(0, "500") 

# BOTONES 
botonDesplegarAsistente = ttk.Button(panelControlesIzquierda, text="Asistente de Ecuaciones", command=abrirModuloAsistenteEcuaciones)
botonDesplegarAsistente.pack(pady=(10, 5), fill=tk.X)

botonRenderizarGrafica = ttk.Button(panelControlesIzquierda, text="Generar Gráfica de Utilización", command=ejecutarTrazadoGrafica)
botonRenderizarGrafica.pack(pady=(0, 5), fill=tk.X)

botonExportarJPG = ttk.Button(panelControlesIzquierda, text="Exportar Gráfica (JPG)", command=ejecutarExportacionImagen)
botonExportarJPG.pack(pady=(0, 10), fill=tk.X)

ventanaPrincipal.mainloop()
