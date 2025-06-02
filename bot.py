import random
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Lista de 100 palabras de 7+ letras para el juego del ahorcado
PALABRAS = [
    "ELEFANTE", "COMPUTADORA", "REFRIGERADOR", "TELEVISION", "HELICOPTERO",
    "HAMBURGUESA", "CHOCOLATE", "DINOSAURIO", "BICICLETA", "ZAPATILLA",
    "BIBLIOTECA", "VENTILADOR", "GIMNASIO", "PELICULA", "RESTAURANTE",
    "TELEFONO", "ALMOHADA", "ESCALERA", "VENTANA", "CUCHILLO",
    "SERPIENTE", "MARIPOSA", "TORTUGA", "GALAXIA", "PLANETA",
    "VOLCAN", "OCEANO", "MONTANA", "DESIERTO", "SELVA",
    "CASTILLO", "PIRAMIDE", "CATEDRAL", "HOSPITAL", "ESCUELA",
    "UNIVERSIDAD", "LABORATORIO", "FARMACIA", "PANADERIA", "CARNICERIA",
    "BARBERIA", "PELUQUERIA", "FLORISTERIA", "LIBRERIA", "PAPELERIA",
    "FERRETERIA", "GASOLINERA", "ESTACION", "AEROPUERTO", "TERMINAL",
    "AUTOBUS", "CAMION", "MOTOCICLETA", "SUBMARINO", "CRUCERO",
    "YATE", "CANOA", "HELICOPTERO", "AVION", "COHETE",
    "SATELITE", "MICROSCOPIO", "TELESCOPIO", "RADIOGRAFIA", "MEDICINA",
    "ANTIBIOTICO", "VITAMINA", "PROTEINA", "CARBOHIDRATO", "COLESTEROL",
    "PSICOLOGIA", "FILOSOFIA", "MATEMATICAS", "QUIMICA", "BIOLOGIA",
    "GEOGRAFIA", "HISTORIA", "LITERATURA", "MUSICA", "PINTURA",
    "ESCULTURA", "ARQUITECTURA", "FOTOGRAFIA", "CINEMATOGRAFIA", "TEATRO",
    "ORQUESTA", "GUITARRA", "VIOLIN", "TROMPETA", "TAMBOR",
    "XILOFONO", "ARMONICA", "ACORDEON", "CLARINETE", "SAXOFON",
    "FUTBOL", "BASQUETBOL", "VOLEIBOL", "NATACION", "ATLETISMO",
    "GIMNASIA", "CICLISMO", "BOXEO", "KARATE", "JUDO",
    "AJEDREZ", "DOMINOES", "CARTAS", "RULETA", "LOTERIA"
]

# Configuración del juego
INTENTOS_MAXIMOS = 4

class JuegoAhorcado:
    def __init__(self):
        self.palabra = ""
        self.palabra_oculta = []
        self.letras_buenas = []
        self.letras_malas = []
        self.intentos_restantes = INTENTOS_MAXIMOS
        self.activo = False
    
    def nuevo_juego(self):
        """Inicia un nuevo juego"""
        self.palabra = random.choice(PALABRAS)
        self.palabra_oculta = ["_"] * len(self.palabra)
        self.letras_buenas = []
        self.letras_malas = []
        self.intentos_restantes = INTENTOS_MAXIMOS
        self.activo = True
        
    def procesar_letra(self, letra):
        """Procesa una letra y retorna True si acierta"""
        letra = letra.upper()
        
        # Verificar si ya fue usada
        if letra in self.letras_buenas or letra in self.letras_malas:
            return None  # Letra ya usada
            
        # Verificar si está en la palabra
        if letra in self.palabra:
            self.letras_buenas.append(letra)
            # Actualizar palabra oculta
            for i, char in enumerate(self.palabra):
                if char == letra:
                    self.palabra_oculta[i] = char
            return True
        else:
            self.letras_malas.append(letra)
            self.intentos_restantes -= 1
            return False
    
    def esta_completa(self):
        """Verifica si la palabra está completa"""
        return "_" not in self.palabra_oculta
    
    def esta_perdido(self):
        """Verifica si se acabaron los intentos"""
        return self.intentos_restantes <= 0
    
    def formatear_estado(self):
        """Retorna el estado actual del juego formateado"""
        palabra_mostrar = " ".join(self.palabra_oculta)
        estrellas = "⭐" * self.intentos_restantes
        
        mensaje = f"Palabra: {palabra_mostrar}\n"
        mensaje += f"Intentos restantes: {self.intentos_restantes} {estrellas}\n"
        mensaje += f"Malas: {self.letras_malas if self.letras_malas else '[]'}\n"
        mensaje += f"Buenas: {self.letras_buenas if self.letras_buenas else '[]'}"
        
        return mensaje

# Diccionario para almacenar juegos por usuario
juegos = {}

def get_teclado_juego():
    """Retorna el teclado del juego"""
    keyboard = [[InlineKeyboardButton("Rendirse", callback_data="rendirse")]]
    return InlineKeyboardMarkup(keyboard)

def get_teclado_menu():
    """Retorna el teclado del menú principal"""
    keyboard = [
        [InlineKeyboardButton("Nuevo Juego", callback_data="nuevo_juego")],
        [InlineKeyboardButton("Salir", callback_data="salir")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    mensaje = "🎮 ¡Bienvenido al Ahorcado Bot!\n\n"
    mensaje += "Presiona 'Comenzar Nuevo Juego' para empezar a jugar."
    
    keyboard = [[InlineKeyboardButton("Comenzar Nuevo Juego", callback_data="nuevo_juego")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(mensaje, reply_markup=reply_markup)

async def nuevo_juego(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inicia un nuevo juego"""
    user_id = update.effective_user.id
    juego = JuegoAhorcado()
    juego.nuevo_juego()
    juegos[user_id] = juego
    
    mensaje = juego.formatear_estado()
    reply_markup = get_teclado_juego()
    
    if update.callback_query:
        await update.callback_query.edit_message_text(mensaje, reply_markup=reply_markup)
        await update.callback_query.answer()
    else:
        await update.message.reply_text(mensaje, reply_markup=reply_markup)

async def procesar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Procesa los mensajes de texto (letras del usuario)"""
    user_id = update.effective_user.id
    
    if user_id not in juegos or not juegos[user_id].activo:
        await update.message.reply_text("No tienes un juego activo. Usa /start para empezar.")
        return
    
    texto = update.message.text.strip()
    
    # Verificar que sea una sola letra
    if len(texto) != 1 or not texto.isalpha():
        await update.message.reply_text("Por favor, envía solo una letra.")
        return
    
    juego = juegos[user_id]
    resultado = juego.procesar_letra(texto)
    
    if resultado is None:
        await update.message.reply_text("Ya usaste esa letra. Prueba con otra.")
        return
    
    # Verificar estado del juego
    if juego.esta_completa():
        # Victoria
        mensaje = f"🎉 ¡GANASTE! 🎉\n\nLa palabra era: {juego.palabra}"
        juego.activo = False
        reply_markup = get_teclado_menu()
        await update.message.reply_text(mensaje, reply_markup=reply_markup)
    elif juego.esta_perdido():
        # Derrota
        mensaje = f"💀 ¡PERDISTE! 💀\n\nLa palabra era: {juego.palabra}"
        juego.activo = False
        reply_markup = get_teclado_menu()
        await update.message.reply_text(mensaje, reply_markup=reply_markup)
    else:
        # Continuar juego
        mensaje = juego.formatear_estado()
        reply_markup = get_teclado_juego()
        await update.message.reply_text(mensaje, reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja los callbacks de los botones"""
    query = update.callback_query
    user_id = update.effective_user.id
    
    if query.data == "nuevo_juego":
        await nuevo_juego(update, context)
    elif query.data == "rendirse":
        if user_id in juegos and juegos[user_id].activo:
            juego = juegos[user_id]
            mensaje = f"😔 Te rendiste\n\nLa palabra era: {juego.palabra}"
            juego.activo = False
            reply_markup = get_teclado_menu()
            await query.edit_message_text(mensaje, reply_markup=reply_markup)
        await query.answer()
    elif query.data == "salir":
        mensaje = "¡Gracias por jugar! 👋\n\nUsa /start cuando quieras volver a jugar."
        await query.edit_message_text(mensaje)
        await query.answer()

def main():
    """Función principal"""
    import os
    # Obtener token desde variable de ambiente
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    
    if not TOKEN:
        print("Error: No se encontró la variable TELEGRAM_TOKEN")
        print("Asegúrate de configurarla en Render o en tu .env")
        return
    
    # Crear la aplicación
    application = Application.builder().token(TOKEN).build()
    
    # Agregar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, procesar_mensaje))
    
    # Ejecutar el bot
    print("Bot iniciado. Presiona Ctrl+C para detener.")
    application.run_polling()

if __name__ == "__main__":
    main()