from datetime import datetime, timezone
import numpy as np
import pytz


month_string = {
'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
}

def convertir_fecha(day_month_string:str, year:str):
    year = year.strip()
    day_month_string = day_month_string.strip().lower()
    [day, _prep, month] = day_month_string.split()
    month = month_string[month.lower()]

    return datetime.strptime(f"{day}-{month}-{year}", "%d-%m-%Y")

def numpy_date_to_datetime(np_datetime):
    if isinstance(np_datetime, np.datetime64):
        timestamp = np_datetime.astype('datetime64[ms]').astype('int64') / 1000.0
        return datetime.fromtimestamp(timestamp, timezone.utc)
    else:
        raise TypeError("La entrada debe ser de tipo np.datetime64")

def datetime_to_timezone(dt, zone:str):
    # Verificar si la entrada es de tipo datetime
    if not isinstance(dt, datetime):
        raise TypeError("La entrada debe ser de tipo datetime")

    # Obtener la zona horaria de Madrid
    tz = pytz.timezone(zone)

    # Si la hora no está en UTC, convertir a UTC primero
    if dt.tzinfo is None:
        dt = pytz.utc.localize(dt)
    elif dt.tzinfo != pytz.utc:
        dt = dt.astimezone(pytz.utc)

    # Convertir a la hora de Madrid
    local_dt = dt.astimezone(tz)
    return local_dt
