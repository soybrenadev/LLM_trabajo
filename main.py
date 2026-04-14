import os
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
token = os.environ.get("GITHUB_TOKEN")

client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=token)


def configurar_negocio():
    nombre_negocio=input("¿Cual es el nombre de su negocio?")
    tipo_negocio=input("¿Cual es el tipo de negocio?")
    vibras_respuesta=input("¿Cual es el tipo de vibras que quiere al responder?")
    servicios_ofrecidos=input("¿Cuales son los servicios que ofrece?")
    horarios_atencion=input("¿Cuales son los horarios de atencion de su negocio?")
    direccion=input("¿Cual es la direccion de su negocio?")
    telefono=input("¿Cual es el telefono de su negocio?")
    email=input("¿Cual es el email de su negocio?")
    redes_sociales=input("¿Cuales son las redes sociales de su negocio?")
    nombre_del_bot=input("¿Cual es el nombre del bot?")

    return {
        "nombre_negocio": nombre_negocio,
        "tipo_negocio": tipo_negocio,
        "vibras_respuesta": vibras_respuesta,
        "servicios_ofrecidos": servicios_ofrecidos,
        "horarios_atencion": horarios_atencion,
        "direccion": direccion,
        "telefono": telefono,
        "email": email,
        "redes_sociales": redes_sociales,
        "nombre_del_bot": nombre_del_bot
    }


def crear_system_prompt(config):
    
    openai_prompt = f"""
    Eres un chatbot de atencion al cliente de un negocio de {config["tipo_negocio"]}.
    El nombre del negocio es {config["nombre_negocio"]}.
    El tipo de vibras que quiere al responder es {config["vibras_respuesta"]}.
    Los servicios que ofrece son {config["servicios_ofrecidos"]}.
    Los horarios de atencion son {config["horarios_atencion"]}.
    La direccion de su negocio es {config["direccion"]}.
    El telefono de su negocio es {config["telefono"]}.
    El email de su negocio es {config["email"]}.
    Las redes sociales de su negocio son {config["redes_sociales"]}.
    El nombre del bot es {config["nombre_del_bot"]}.
    Responde siempre en el idioma del cliente. Si no sabes algo, di que consultarás con el equipo. Siempre usa emojis.
    Si el cliente pregunta algo que no tiene relación con el negocio, responde amablemente que solo puedes ayudar con temas relacionados a {config["nombre_negocio"]}.
    Si el cliente hace un pedido, confirma el pedido, di "¡Listo! Ya avisé a la taquería sobre tu pedido 🎉" y muestra un resumen del pedido con precios y total y que el negocio marcará de regreso para confirmar el pedido y que si puede dejar un numero de contacto para que el negocio le llame y dirección de entrega y sigue preguntando hasta que responda un numero de contacto valido.
    Nunca inventes productos que no estén en el menú.
    Solo responde preguntas relacionadas al negocio.
    """

    return openai_prompt


def iniciar_chat(config):
    system_prompt = crear_system_prompt(config)
    historial = [{"role": "system", "content": system_prompt}]
    
    print(f"\n¡Hola! Soy {config['nombre_del_bot']} de {config['nombre_negocio']}. ¿En qué puedo ayudarte hoy?")

    while True:
        mensaje = input("Tú: ")
        if mensaje.lower() == "salir":
            print("¡Adios! ¡Que tengas un buen día!")
            break
        
        historial.append({"role": "user", "content": mensaje})
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=historial
        )

        chat_respuesta = response.choices[0].message.content
        print(f"Bot: {chat_respuesta}")
        historial.append({"role": "assistant", "content": chat_respuesta})

        guardar_mensajes("user", mensaje, config["nombre_negocio"])
        guardar_mensajes("assistant", chat_respuesta, config["nombre_negocio"])


def guardar_mensajes(rol, nmensaje, nombre_negocio):
    ahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos = {
        "fecha_hora": [ahora],
        "nombre_negocio": [nombre_negocio],
        "rol": [rol],
        "mensaje": [nmensaje]
    }
    df = pd.DataFrame(datos)

    archivo_existe = os.path.exists("historial.csv")
    df.to_csv("historial.csv", mode='a', header=not archivo_existe, index=False)


def analizar_datos(nombre_negocio):
    df = pd.read_csv("historial.csv")
    historial_texto = df.to_string()

    response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "system", "content": "Eres un analista de datos experto en negocios."},
        {"role": "user", "content": f"""Analiza este historial de conversaciones de un negocio y dame insights sobre:
        1. Productos más pedidos
        2. Si los pedidos son a domicilio o para recoger
        3. Horarios con más actividad
        4. Sentimiento general de los clientes
        5. Preguntas más frecuentes
        
        Historial:
        {historial_texto}"""}
    ]
    )
    chat_analisis = response.choices[0].message.content
    print("\n📊 ANÁLISIS DEL NEGOCIO:")
    print(chat_analisis)
    print(f"\n📧 Enviando análisis al correo del negocio... ✅")

if __name__ == "__main__":
    config = configurar_negocio()
    iniciar_chat(config)
    analizar_datos(config["nombre_negocio"])

        

    