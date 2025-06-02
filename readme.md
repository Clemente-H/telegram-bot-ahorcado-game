# 🎮 Bot de Ahorcado para Telegram

Un juego simple y divertido del clásico ahorcado implementado como bot de Telegram. Partidas rápidas de 3-5 minutos con palabras en español de 7+ letras.

## 🚀 Características

- **100 palabras** variadas de diferentes categorías
- **4 intentos** para adivinar la palabra
- **Interfaz limpia** con solo la información esencial
- **Partidas rápidas** - perfecto para jugar en cualquier momento
- **Sin complicaciones** - solo escribe letras y juega

## 🎯 Cómo Jugar

1. Inicia el bot con `/start`
2. Presiona "Comenzar Nuevo Juego"
3. Escribe una letra en el chat
4. El bot te muestra si acertaste o no
5. Continúa hasta completar la palabra o quedarte sin intentos

### Ejemplo de Juego
```
Palabra: _ _ _ _ _ _ _ _ 
Intentos restantes: 4 ⭐⭐⭐⭐
Malas: []
Buenas: []

[Rendirse]
```

Usuario escribe: "E"

```
Palabra: E _ E _ _ _ _ E 
Intentos restantes: 4 ⭐⭐⭐⭐
Malas: []
Buenas: [E]

[Rendirse]
```

## 📁 Estructura del Proyecto

```
hangman-telegram-bot/
├── bot.py              # Código principal del bot
├── requirements.txt    # Dependencias de Python
├── README.md          # Este archivo
└── .env.example       # Ejemplo de variables de ambiente
```

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8+
- Una cuenta de Telegram
- Token de bot de Telegram (obtenido de @BotFather)

### Pasos

1. **Clona el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/hangman-telegram-bot.git
   cd hangman-telegram-bot
   ```

2. **Instala las dependencias**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configura el token**
   - Crea un bot en Telegram con @BotFather
   - Copia el token que te da
   - Reemplaza `TU_TOKEN_AQUI` en `bot.py` con tu token

4. **Ejecuta el bot**
   ```bash
   python bot.py
   ```

## 📦 Dependencias

```txt
python-telegram-bot==20.7
```

## 🎮 Funcionalidades del Bot

### Comandos
- `/start` - Inicia el bot y muestra el menú principal

### Botones
- **Comenzar Nuevo Juego** - Inicia una nueva partida
- **Rendirse** - Termina la partida actual
- **Nuevo Juego** - Inicia otra partida después de terminar
- **Salir** - Cierra el juego

### Mecánica del Juego
- **Estado persistente**: Cada usuario tiene su propia partida
- **Validación de entrada**: Solo acepta letras individuales
- **Detección de letras repetidas**: No permite usar la misma letra dos veces
- **4 intentos máximo**: Balance perfecto entre desafío y diversión

## 🎯 Palabras Incluidas

El bot incluye 100 palabras cuidadosamente seleccionadas de diferentes categorías:

- **Animales**: ELEFANTE, SERPIENTE, MARIPOSA...
- **Objetos**: COMPUTADORA, REFRIGERADOR, TELEVISION...
- **Lugares**: BIBLIOTECA, RESTAURANTE, AEROPUERTO...
- **Deportes**: FUTBOL, BASQUETBOL, NATACION...
- **Instrumentos**: GUITARRA, VIOLIN, SAXOFON...
- **Ciencias**: QUIMICA, BIOLOGIA, MATEMATICAS...

Todas las palabras tienen entre 7-15 letras para mantener el desafío apropiado.

## 🔧 Personalización

### Cambiar Número de Intentos
Modifica la constante `INTENTOS_MAXIMOS` en `bot.py`:
```python
INTENTOS_MAXIMOS = 6  # Cambia a 6 intentos
```

### Agregar Más Palabras
Edita la lista `PALABRAS` en `bot.py`:
```python
PALABRAS = [
    "ELEFANTE", "COMPUTADORA", # ... palabras existentes
    "TUPALABRA", "OTRAPALABRA"  # Agregar aquí
]
```

### Cambiar Mensajes
Modifica los strings en las funciones correspondientes para personalizar los mensajes del bot.

## 🚀 Despliegue

### Opción 1: Servidor Local
Ejecuta `python bot.py` en tu computadora. El bot funcionará mientras tu computadora esté encendida.

### Opción 2: Heroku
1. Crea una cuenta en Heroku
2. Instala Heroku CLI
3. Crea un `Procfile`:
   ```
   worker: python bot.py
   ```
4. Configura las variables de ambiente con tu token
5. Despliega con `git push heroku main`

### Opción 3: VPS
Sube el código a tu VPS y ejecútalo con `screen` o `tmux` para mantenerlo activo.

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

## 🐛 Reportar Bugs

Si encuentras un bug o tienes una sugerencia, por favor abre un issue en GitHub con:
- Descripción del problema
- Pasos para reproducirlo
- Comportamiento esperado vs actual

## 🎉 ¡Disfruta Jugando!

Un proyecto simple pero divertido perfecto para aprender sobre bots de Telegram o simplemente pasar un buen rato jugando ahorcado.