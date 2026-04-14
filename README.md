# Proyecto 8: LLM
# ChatBot SaaS con IA para Atención al Cliente 🤖

## Descripción
Sistema de atención al cliente impulsado por GPT-4.1-mini de OpenAI, 
diseñado como un SaaS configurable para cualquier tipo de negocio. 
El dueño configura el bot con los datos de su negocio y este se adapta 
automáticamente al tono, productos y personalidad deseada. Al finalizar 
cada sesión, el sistema analiza el historial de conversaciones y genera 
insights sobre productos más pedidos, horarios de actividad, sentimiento 
de los clientes y áreas de oportunidad.

## Requisitos
- Python 3.9 o superior
- Cuenta de GitHub para acceder a GitHub Models (gratis)
- Token de GitHub con permisos de Models: Read

## Instalación

1. Haz fork de este repositorio y clónalo:
git clone url_de_tu_repositorio

2. Entra a la carpeta del proyecto y crea tu entorno virtual:
python3 -m venv .venv

3. Actívalo:
source .venv/bin/activate

4. Instala las dependencias:
pip install -r requirements.txt

5. Crea un archivo .env en la raíz del proyecto:
GITHUB_TOKEN=tu_token_aqui

Para obtener tu token gratuito:
- Ve a github.com/marketplace/models
- Selecciona el modelo que prefieras (recomendado: GPT-4.1-mini)
- Click en "Use this model" → "Create Personal Access Token"
- Copia el token y pégalo en el .env

## Uso

Corre el programa:
python main.py

- Configura tu negocio respondiendo las preguntas iniciales
- Chatea con el bot como si fuera un cliente
- Escribe "salir" para terminar la sesión
- Al salir verás el análisis automático de la conversación

## Archivos generados
- historial.csv — registro de todas las conversaciones