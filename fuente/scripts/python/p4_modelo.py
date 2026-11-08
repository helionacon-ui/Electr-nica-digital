"""Modelo de la práctica 4: refresco multiplexado del display de 4 dígitos."""
F_CLK = 50e6
def refresco(bits_cnt=18):
    t_digito = 2 ** (bits_cnt - 2)          # ciclos que cada dígito permanece encendido
    return F_CLK / t_digito, F_CLK / (4 * t_digito)

def barrido(d, ciclos_por_digito=4):
    """d = [d3, d2, d1, d0]. Devuelve la secuencia de (ánodo activo, cifra) durante un barrido."""
    an = ['1110', '1101', '1011', '0111']
    return [(an[i], d[3 - i]) for i in range(4)]

if __name__ == '__main__':
    f_dig, f_disp = refresco()
    print(f'cambio de dígito: {f_dig:.1f} Hz; refresco de cada dígito: {f_disp:.1f} Hz')
    print('barrido para mostrar 1 2 3 4:')
    for an, c in barrido([1, 2, 3, 4]): print(f'  an={an}  cifra={c}')
    assert round(f_dig, 1) == 762.9 and round(f_disp, 1) == 190.7
    print('Comprobaciones: OK')
