"""Modelos en Python de la práctica 3: contador, divisor de frecuencia, antirrebote y detector 101."""
def contador(N, ciclos, en=1):
    q, out = 0, []
    for _ in range(ciclos):
        out.append(q)
        if en:
            q = 0 if q == N - 1 else q + 1
    return out

def divisor(f_in, f_out):
    div = round(f_in / f_out)
    return div, div // 2 - 1, (div // 2 - 1).bit_length()

def antirrebote(entrada, lim):
    prev = cnt = sal = 0; s1 = s2 = 0; out = []
    for x in entrada:
        s2_old = s2; s2 = s1; s1 = x
        if s2_old != prev:           # el VHDL compara s2 (valor ya registrado) con prev
            prev = s2_old; cnt = 0
        elif cnt == lim:
            sal = prev
        else:
            cnt += 1
        out.append(sal)
    return out

def detector101(bits):
    est = 0; z = []
    T = {(0, 0): 0, (0, 1): 1, (1, 0): 2, (1, 1): 1, (2, 0): 0, (2, 1): 1}
    for x in bits:
        z.append(int(est == 2 and x == 1)); est = T[(est, x)]
    return z

if __name__ == '__main__':
    print('contador mod 10:', contador(10, 13))
    print('contador mod 12:', contador(12, 14))
    print('divisor 50 MHz -> 1 Hz: DIV=%d, cuenta hasta %d, %d bits' % divisor(50e6, 1))
    print('divisor 50 MHz -> 1 kHz: DIV=%d, cuenta hasta %d, %d bits' % divisor(50e6, 1000))
    ent = [0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    sal = antirrebote(ent, 3)
    print('entrada :', ''.join(map(str, ent)))
    print('salida  :', ''.join(map(str, sal)))
    x = [1, 0, 1, 0, 1, 1, 0, 1]
    print('detector 101: x =', x, ' z =', detector101(x))
    assert contador(10, 13)[-3:] == [0, 1, 2]
    assert divisor(50e6, 1) == (50000000, 24999999, 25)
    assert detector101(x) == [0, 0, 1, 0, 1, 0, 0, 1]
    assert sal[-1] == 0 and max(sal) == 1
    print('Comprobaciones: OK')
