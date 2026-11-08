"""Modelo del módulo de alarma de temperatura (prácticas 5-7, ejemplo) con histéresis."""
def alarma(medidas, t_alta=375, t_baja=360, hist=5):
    a = b = 0; out = []
    for t in medidas:
        if t >= t_alta: a = 1
        elif t < t_alta - hist: a = 0
        if t < t_baja: b = 1
        elif t >= t_baja + hist: b = 0
        out.append((t, a, b))
    return out

if __name__ == '__main__':
    medidas = [365, 370, 374, 375, 376, 373, 371, 369, 366, 362, 359, 361, 364, 366]
    print('temp(0,1 °C)  al_alta  al_baja')
    for t, a, b in alarma(medidas): print(f'{t:6d}        {a}        {b}')
    r = alarma(medidas)
    assert [x[1] for x in r][3] == 1 and [x[1] for x in r][5] == 1 and [x[1] for x in r][7] == 0
    assert [x[2] for x in r][10] == 1 and [x[2] for x in r][11] == 1 and [x[2] for x in r][12] == 1 and [x[2] for x in r][13] == 0
    print('Comprobaciones: OK')
