def normalizar_rut(rut: str) -> str:
    """
    Normaliza el formato del RUT chileno eliminando puntos y guiones.
    Devuelve el RUT en mayúsculas, sin separadores.
    Ejemplo:
      "12.345.678-9" → "123456789"
      "12345678-9"  → "123456789"
    """
    if not rut:
        return ""
    rut = rut.replace(".", "").replace("-", "").replace(" ", "").upper()
    return rut


def normalizar_patente(patente: str) -> str:
    """
    Normaliza una patente chilena eliminando espacios, guiones y convirtiendo a mayúsculas.
    Ejemplo:
      'ab cd 12'  → 'ABCD12'
      'AB-CD-12'  → 'ABCD12'
      'abcd12'    → 'ABCD12'
    """
    if not patente:
        return ""
    # Eliminar espacios, guiones y convertir a mayúsculas
    return patente.replace(" ", "").replace("-", "").upper()
