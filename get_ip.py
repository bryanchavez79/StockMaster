#!/usr/bin/env python3
"""
Script para obtener la IP local del servidor y mostrar la URL de acceso.
"""

import socket

def obtener_ip_local():
    try:
        # Obtener el hostname
        hostname = socket.gethostname()
        # Obtener la IP local
        ip_local = socket.gethostbyname(hostname)
        return ip_local, hostname
    except Exception as e:
        return None, str(e)

if __name__ == "__main__":
    ip, hostname = obtener_ip_local()
    
    print("\n" + "="*60)
    print("STOCKMASTER - INFORMACIÓN DE ACCESO")
    print("="*60)
    
    if ip:
        print(f"\n✓ Hostname: {hostname}")
        print(f"✓ IP Local: {ip}")
        print(f"\n📱 URL para acceso local:")
        print(f"   http://127.0.0.1:5000")
        print(f"\n🌐 URL para acceso desde otra PC en la red:")
        print(f"   http://{ip}:5000")
        print(f"\n💻 URL con hostname (si está configurado):")
        print(f"   http://stockmaster:5000")
        print(f"\n⚠️  Asegúrate de que el puerto 5000 esté abierto en el firewall")
        print("="*60 + "\n")
    else:
        print(f"❌ Error al obtener la IP: {hostname}")

