import requests
import urllib.parse


API_KEY = "17739df0-e5fa-423f-9a03-8974d5381e1b" 

def obtener_coordenadas(ciudad):
    """Obtiene latitud y longitud de una ciudad usando la API de Geocoding."""
    url = f"https://graphhopper.com/api/1/geocode?q={urllib.parse.quote(ciudad)}&locale=es&key={API_KEY}"
    response = requests.get(url).json()
    if response.get("hits"):
        point = response["hits"][0]["point"]
        return point["lat"], point["lng"]
    return None, None

def calcular_viaje(origen, destino):
    """Calcula la ruta, distancia, tiempo, combustible y narrativa del viaje."""
    lat1, lon1 = obtener_coordenadas(origen)
    lat2, lon2 = obtener_coordenadas(destino)
    
    if lat1 is None or lat2 is None:
        print(f"❌ Error: No se pudieron encontrar las coordenadas para {origen} o {destino}.")
        return

    url = f"https://graphhopper.com/api/1/route?point={lat1},{lon1}&point={lat2},{lon2}&vehicle=car&locale=es&key={API_KEY}&instructions=true"
    res = requests.get(url).json()
    
    if "paths" in res:
        path = res["paths"][0]
        # Distancia de metros a kilómetros
        distancia_km = path["distance"] / 1000
        tiempo_ms = path["time"]
        
        # Conversión de milisegundos a Horas, Minutos y Segundos
        segundos_totales = int(tiempo_ms / 1000)
        horas = segundos_totales // 3600
        minutos = (segundos_totales % 3600) // 60
        segundos = segundos_totales % 60
        
        # Consumo de Combustible aproximado (Ej: 12 km por litro)
        rendimiento_km_l = 12.0
        combustible_litros = distancia_km / rendimiento_km_l
        
        # Despliegue de resultados con 2 decimales
        print("\n" + "="*50)
        print(f"🚗 NARRATIVA DEL VIAJE: {origen.upper()} a {destino.upper()}")
        print("="*50)
        print(f"📍 Distancia total: {distancia_km:.2f} km")
        print(f"⏱️ Duración del viaje: {horas} horas, {minutos} minutos y {segundos} segundos")
        print(f"⛽ Combustible requerido: {combustible_litros:.2f} litros (Rendimiento est.: 12km/L)")
        print("-"*50)
        
        print("🗺️ Indicaciones de la ruta:")
        for idx, inst in enumerate(path.get("instructions", []), 1):
            print(f" {idx}. {inst['text']} ({inst['distance']/1000:.2f} km)")
        print("="*50)
    else:
        print("❌ No se pudo calcular la ruta entre las ciudades proporcionadas.")

# Bucle principal del programa
while True:
    print("\n--- 🗺️ Consumo de API Pública Graphhopper ---")
    origen = input("Ciudad de Origen (o presione 'q' para salir): ")
    if origen.lower() == 'q':
        print("Saliendo del programa...")
        break
        
    destino = input("Ciudad de Destino: ")
    if destino.lower() == 'q':
        print("Saliendo del programa...")
        break
        
    calcular_viaje(origen, destino)