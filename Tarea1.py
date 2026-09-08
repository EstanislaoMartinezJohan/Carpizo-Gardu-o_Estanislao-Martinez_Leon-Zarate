def caracter_a_valor(c):
    if '0' <= c <= '9': return int(c)
    return ord(c.upper()) - ord('A') + 10

def valor_a_caracter(v):
    if 0 <= v <= 9: return str(v)
    return chr(v - 10 + ord('A'))

def validar_congruencia(numero_str, base):
    numero_limpio = numero_str.lstrip('-').replace('.', '', 1)
    for digito in numero_limpio:
        if caracter_a_valor(digito) >= base:
            raise ValueError(f"Error: El dígito '{digito}' no es válido en base {base}.")
    return True

def cuenta_larga_a_valor(numero_str, base_origen):
    validar_congruencia(numero_str, base_origen)
    es_negativo = numero_str.startswith('-')
    if es_negativo: numero_str = numero_str[1:]
        
    if '.' in numero_str:
        parte_entera, parte_frac = numero_str.split('.', 1)
    else:
        parte_entera, parte_frac = numero_str, ""
        
    valor_acumulado = 0.0
    for i, digito in enumerate(parte_entera[::-1]):
        valor_acumulado += caracter_a_valor(digito) * (base_origen ** i)
        
    for i, digito in enumerate(parte_frac):
        valor_acumulado += caracter_a_valor(digito) * (base_origen ** -(i + 1))
        
    return -valor_acumulado if es_negativo else valor_acumulado

def valor_a_base(valor, base_destino, precision=6):
    if valor == 0: return "0"
    es_negativo = valor < 0
    valor = abs(valor)
    
    parte_entera = int(valor)
    parte_fraccionaria = valor - parte_entera
    
    res_entero = "" if parte_entera > 0 else "0"
    while parte_entera > 0:
        res_entero = valor_a_caracter(parte_entera % base_destino) + res_entero
        parte_entera //= base_destino
            
    if parte_fraccionaria == 0:
        return "-" + res_entero if es_negativo else res_entero
        
    res_frac = ""
    iteraciones = 0
    while parte_fraccionaria > 0 and iteraciones < precision:
        parte_fraccionaria *= base_destino
        digito = int(parte_fraccionaria)
        res_frac += valor_a_caracter(digito)
        parte_fraccionaria -= digito
        iteraciones += 1
            
    res_final = f"{res_entero}.{res_frac}"
    return "-" + res_final if es_negativo else res_final

def sumar_un_bit(bit_a, bit_b, acarreo_in):
    """Suma modular de 1 bit según especificación del PDF."""
    suma_total = int(bit_a) + int(bit_b) + acarreo_in
    suma = suma_total % 2
    acarreo_out = 1 if suma_total >= 2 else 0
    return str(suma), acarreo_out

def magnitud_binaria(valor, bits=5):
    """Convierte la magnitud absoluta a binario de N bits."""
    binario = ""
    v = abs(valor)
    for _ in range(bits):
        binario = str(v % 2) + binario
        v //= 2
    return binario

def generar_complemento_dos(valor, bits_totales=6):
    """Aplica la inversión y suma de +1 manual para negativos."""
    bits_mag = bits_totales - 1
    if valor < -(2**bits_mag) or valor > (2**bits_mag - 1):
        raise OverflowError(f"Valor {valor} fuera de rango para {bits_totales} bits.")
    
    magnitud = magnitud_binaria(valor, bits_mag)
    
    if valor >= 0:
        return "0" + magnitud # Bit de signo 0
        
    # Paso 1: Invertir bits de magnitud (Complemento a 1)
    mag_invertida = "".join('1' if b == '0' else '0' for b in magnitud)
    
    # Paso 2: Sumar 1 al LSB para obtener Complemento a 2
    mag_c2 = ""
    acarreo = 1
    for b in mag_invertida[::-1]:
        s, acarreo = sumar_un_bit(b, '0', acarreo)
        mag_c2 = s + mag_c2
        
    return "1" + mag_c2 # Bit de signo 1

def emulador_sumador_6bits(num1_str, num2_str, base):
    val1 = int(cuenta_larga_a_valor(num1_str, base))
    val2 = int(cuenta_larga_a_valor(num2_str, base))
    
    bin1 = generar_complemento_dos(val1)
    bin2 = generar_complemento_dos(val2)
    
    resultado = ""
    acarreo = 0
    
    # Bucle de Suma de Magnitud (5 ciclos) de derecha a izquierda
    for i in range(5, 0, -1):
        suma, acarreo = sumar_un_bit(bin1[i], bin2[i], acarreo)
        resultado = suma + resultado
        
    # Guardar acarreo que entra a la celda de signo para detectar Overflow
    acarreo_entra_signo = acarreo
    
    # Llamada de Signo (6.ª operación aislada)
    suma_signo, acarreo_sale_signo = sumar_un_bit(bin1[0], bin2[0], acarreo)
    resultado = suma_signo + resultado
    
    overflow = acarreo_entra_signo != acarreo_sale_signo
    
    return bin1, bin2, resultado, overflow

def Tarea1():
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1. Transformación de base (Divisiones/Multiplicaciones sucesivas)")
        print("2. Emulador de Sumador Binario de 6 bits (C2)")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            try:
                print("\n-- Transformación de Base --")
                base_origen = int(input("Base de origen: "))
                numero_str = input("Número a convertir: ")
                base_destino = int(input("Base de destino: "))
                
                valor_interno = cuenta_larga_a_valor(numero_str, base_origen)
                resultado = valor_a_base(valor_interno, base_destino)
                print(f"Resultado: {resultado}")
            except Exception as e:
                print(f"Error: {e}")
                
        elif opcion == '2':
            try:
                print("\n-- Sumador C2 --")
                base_origen = int(input("Base de origen de los operandos: "))
                num1 = input("Primer número: ")
                num2 = input("Segundo número: ")
                
                bin1, bin2, res, overflow = emulador_sumador_6bits(num1, num2, base_origen)
                
                print(f"\nOperando 1 (6-bit): {bin1}")
                print(f"Operando 2 (6-bit): {bin2}")
                print(f"Suma Binaria:       {res}")
                
                if overflow:
                    print("¡ADVERTENCIA! Se detectó Desbordamiento Aritmético (Overflow).")
                else:
                    print("Operación exitosa (Sin Overflow).")
            except Exception as e:
                print(f"Error: {e}")
                
        elif opcion == '3':
            break

if __name__ == "__main__":
    Tarea1()