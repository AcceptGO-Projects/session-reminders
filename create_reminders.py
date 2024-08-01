import requests
from datetime import datetime, timedelta

# Configuración
course_id = 3
category = "alert"

# Lista de recordatorios con fechas en UTC-4
reminders = [
    {"date": "31/7/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S3 Momentos de Gloria 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "5/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S4 Verbos, experiencia y acción 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "7/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S5 Tu Postal de experiencia - El CV 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "9/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S6 Roles y Diseño de vidas 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "12/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S7 Tu Marca Personal 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "13/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S8 Networking 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "15/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S9 Brilla en 30 segundos 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "19/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S10 Mapa de Brechas 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"},
    {"date": "21/8/2024", "time": "18:00", "message": "🚨 Alerta de Avance 🚨\n\nHola {{name}},\n\nHoy te toca avanzar la lección S11 Piensa diferente 🤩\nQuedamos atentos a cualquier duda\n\nSaludos"}
]

# Función para convertir la fecha y hora de UTC-4 a UTC-0
def convert_to_utc(date_str, time_str):
    local_time = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
    utc_time = local_time + timedelta(hours=4)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

# Realizar los posts
for reminder in reminders:
    due_date = convert_to_utc(reminder['date'], reminder['time'])
    data = {
        "course_id": course_id,
        "message": reminder['message'],
        "category": category,
        "due_date": due_date
    }
    
    # Realizar la solicitud POST
    response = requests.post("http://ec2-18-216-12-244.us-east-2.compute.amazonaws.com/api/v1/reminders", json=data)
    
    if response.status_code == 200:
        print(f"Recordatorio enviado correctamente para el {reminder['date']} a las {reminder['time']}.")
    else:
        print(f"Error al enviar el recordatorio para el {reminder['date']} a las {reminder['time']}: {response.status_code} - {response.text}")
