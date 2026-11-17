import dns.resolver

# 1. Consultar los registros MX de gmail.com
respuesta_mx = dns.resolver.query("gmail.com", "MX")

# 2. Ordenar los registros por prioridad (preference) de menor a mayor
registros_ordenados = sorted(respuesta_mx, key=lambda r: r.preference)

# 3. Resolver la IP (registro A) de cada máquina (exchange) y mostrarla
for r in registros_ordenados:
    nombre_servidor = str(r.exchange)
    respuesta_a = dns.resolver.query(nombre_servidor, "A")
    ip = respuesta_a[0].address
    print(f"{r.preference} {nombre_servidor} {ip}")