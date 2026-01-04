import cv2
import mediapipe as mp
import ollama
import pyttsx3
import time
import sys

# =============================================================================
# ZONA 1: CONFIGURACIÓN Y "CALENTAMIENTO" (Se ejecuta 1 vez al inicio)
# =============================================================================

print("--- INICIANDO SISTEMA UMBRAL ---")

# 1. CONFIGURAR CONSTANTES
MODELO_IA = "llama3.2"       # Tu modelo local ligero
TIEMPO_LIMITE = 10           # Segundos para activar la alerta
ANCHO_ZONA = 640             # Ancho de la cámara (ajustable)
ALTO_ZONA = 480              # Alto de la cámara

# 2. INICIALIZAR MOTOR DE VOZ (La Boca)
print("🔊 Configurando sistema de audio...")
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 140) # Velocidad un poco más lenta para ser clara
    engine.setProperty('volume', 1.0)
except Exception as e:
    print(f"❌ Error al iniciar audio: {e}")
    sys.exit(1)

# 3. INICIALIZAR VISIÓN ARTIFICIAL (Los Ojos)
print("👁️ Cargando modelos de MediaPipe...")
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
detector = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# 4. CALENTAR IA LOCAL (El Cerebro)
print(f"🧠 Despertando a {MODELO_IA} (esto puede tardar unos segundos)...")
try:
    # Enviamos un mensaje vacío para cargar el modelo en la VRAM de tu NVIDIA
    ollama.chat(model=MODELO_IA, messages=[{'role': 'user', 'content': 'ping'}])
    print("✅ IA Local lista y cargada.")
except Exception as e:
    print(f"❌ ERROR CRÍTICO: No se detecta Ollama. ¿Ejecutaste 'ollama serve'?")
    print(f"Detalle: {e}")
    sys.exit(1)

# =============================================================================
# ZONA 2: FUNCIONES AUXILIARES (Herramientas)
# =============================================================================

def hablar_radio(texto):
    """Función para que el computador hable"""
    print(f"📡 RADIO GUARDIA: {texto}")
    engine.say(texto)
    engine.runAndWait() # Esto pausará el video brevemente mientras habla (normal en MVP)

def consultar_cerebro(contexto):
    """Consulta al modelo local Llama 3.2"""
    try:
        response = ollama.chat(model=MODELO_IA, messages=[
            {
                'role': 'system', 
                'content': 'Eres un psicólogo orientado a la prevención de riesgos. Tu trabajo consiste en comunicar, su nivel de gravedad y la información sensible asociada dependiendo de la calidad. Para ello, debes utilizar por ejemplo si la persona esta en el anden norte o sur, e identificar los criterios que definen la información relevante a comunicar. Se entiende por información “delicada” aquella con alto potencial de impacto, que debe ser tratada como privada.Para determinar el nivel de riesgo, debes utilizar una escala del 1 al 100, donde 100 corresponde al riesgo máximo y 1 al riesgo mínimo. Tus respuestas deben ser concisas y directas, limitándose únicamente a una de las siguientes cuatro opciones, según lo que observes. Luego, deberás transmitir la información por radio siguiendo el grado de riesgo y los criterios de prioridad: No hay riesgo (1–25 puntos; persona tranquila, sin agitación motora, relajada) respuesta esperada: todo bien.Línea amarilla 25–50 puntos; persona sobre la línea amarilla por más de 5 segundos) → respuesta esperada: “Activar recordatorio por voz”. Riesgo bajo 50–75 puntos; la persona mantiene los pies en un mismo punto, se toma la cabeza con las manos o presenta conducta física anormal) → respuesta esperada: “🚨 Riesgo Bajo: Guardias por favor atentos a los andenes”. Riesgo alto 75–100 puntos; la persona se mueve de un lado a otro, observa fijamente el túnel o realiza movimientos corporales erráticos) → respuesta esperada: “🚨 Riesgo Alto: activar alerta por voz y activar protocolo de asistencia inmediata.” Criterios generales: una persona acompañada presenta menor riesgo. El reporte generado tras la palabra “afirmativo” debe incluir únicamente la sección “Ficha Única del Accidente (Datos de Ingreso)”, completada con la información relevante identificada en el evento. Es estrictamente necesario omitir cualquier análisis, nota o referencia a los criterios de “información delicada”. La respuesta por radio debe ser exclusivamente una de las cuatro frases predefinidas, sin descripciones, análisis ni justificaciones del contenido del video, imagen o de la puntuación asignada. Como psicólogo de prevención de riesgos, solo puedes emitir la alerta inmediata correspondiente entre las cuatro opciones disponibles. Todo esto debes decirlo en 15 o 10 palabras maximo'
            },
            {
                'role': 'user', 
                'content': contexto
            }
        ])
        return response['message']['content']
    except:
        return "Alerta de prioridad. Acérquese con precaución."

# =============================================================================
# ZONA 3: BUCLE PRINCIPAL (El Orquestador en Tiempo Real)
# =============================================================================

def main():
    cap = cv2.VideoCapture(0) # Abrir Webcam
    
    # Variables de estado
    inicio_permanencia = None  # Cronómetro
    alerta_disparada = False   # Para no repetir la alerta infinitamente

    print("\n🟢 SISTEMA OPERATIVO. PREPARADO PARA DETECCIÓN.")
    print("Presiona 'q' para salir.")

    while True:
        ret, frame = cap.read()
        if not ret: break

        # 1. Pre-procesamiento de imagen
        frame = cv2.flip(frame, 1) # Efecto espejo (más natural)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 2. Detección de Cuerpo (MediaPipe)
        resultado = detector.process(frame_rgb)
        
        hay_persona = False
        if resultado.pose_landmarks:
            hay_persona = True
            # Opcional: Dibujar el esqueleto para que se vea "Tech" en la demo
            mp_drawing.draw_landmarks(frame, resultado.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # 3. LÓGICA DE TIEMPO (El Algoritmo "Coreano" simplificado)
        if hay_persona:
            if inicio_permanencia is None:
                inicio_permanencia = time.time() # Iniciar reloj
            
            tiempo_transcurrido = int(time.time() - inicio_permanencia)
            
            # Mostrar cronómetro en pantalla
            color_reloj = (0, 255, 0) # Verde
            if tiempo_transcurrido > TIEMPO_LIMITE / 2: color_reloj = (0, 255, 255) # Amarillo
            if tiempo_transcurrido >= TIEMPO_LIMITE: color_reloj = (0, 0, 255) # Rojo
            
            cv2.putText(frame, f"Permanencia: {tiempo_transcurrido}s", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, color_reloj, 2)

            # --- MOMENTO DE LA ALERTA ---
            if tiempo_transcurrido >= TIEMPO_LIMITE and not alerta_disparada:
                alerta_disparada = True # Bloquear para que no se dispare 2 veces
                
                # A. Feedback Visual (Pantalla Roja)
                cv2.rectangle(frame, (0,0), (ANCHO_ZONA, ALTO_ZONA), (0,0,255), 10)
                cv2.putText(frame, "RIESGO DETECTADO", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
                cv2.imshow('UMBRAL - MONITOR', frame)
                cv2.waitKey(1) # Forzar pintado en pantalla antes de pensar
                
                # B. Consultar IA (Puede tardar 1 seg)
                instruccion = consultar_cerebro(f"Sujeto estático detectado por {tiempo_transcurrido} segundos. Posible riesgo.")
                
                # C. Hablar
                hablar_radio(instruccion)
                
                # D. Resetear (Para demo continua) o Pausar
                # inicio_permanencia = None # Descomentar si quieres resetear inmediato
                
        else:
            # Si la persona se va, reseteamos todo
            inicio_permanencia = None
            alerta_disparada = False

        # 4. Mostrar Video Final
        cv2.imshow('UMBRAL - MONITOR', frame)

        # Salir con tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Limpieza al cerrar
    cap.release()
    cv2.destroyAllWindows()
    print("🔴 Sistema apagado.")

if __name__ == "__main__":
    main()