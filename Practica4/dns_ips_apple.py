import dns.resolver

#depende lo que consultemos da uno o varios
respuesta = dns.resolver.query('apple.com')
#otra forma de hacerlo
respuesta = dns.resolver.resolve('apple.com')


for i in respuesta:
    print(i)
