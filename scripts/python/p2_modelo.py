"""Modelos en Python de la práctica 2 (sumador, comparador, mux y display de 7 segmentos)."""
SEG7 = {0: '0000001', 1: '1001111', 2: '0010010', 3: '0000110', 4: '1001100',
        5: '0100100', 6: '0100000', 7: '0001111', 8: '0000000', 9: '0000100'}   # activos a 0, orden abcdefg

def sum4(a, b, cin):
    t = a + b + cin
    return t & 0xF, t >> 4

def cmp4(a, b):
    return int(a > b), int(a == b), int(a < b)

def mux4(d, sel):
    return (d >> sel) & 1

def seg7(d):
    return SEG7.get(d, '1111111')

if __name__ == '__main__':
    print('--- sumador de 4 bits ---')
    for a, b, c in [(9, 8, 0), (15, 1, 0), (7, 8, 1), (15, 15, 1)]:
        s, co = sum4(a, b, c)
        print(f'{a:2d} + {b:2d} + {c} = s {s:04b} ({s:2d}), cout {co}')
    print('--- comparador ---')
    for a, b in [(5, 9), (9, 9), (12, 3)]:
        print(f'a={a:2d} b={b:2d} -> gt,eq,lt = {cmp4(a, b)}')
    print('--- mux 4:1 (d=0110) ---')
    for sel in range(4):
        print(f'sel={sel:02b} -> y={mux4(0b0110, sel)}')
    print('--- display (activo a 0, abcdefg) ---')
    for d in (0, 1, 7, 9, 12):
        print(f'{d:2d} -> {seg7(d)}')
    # comprobaciones exhaustivas
    assert all(sum4(a, b, c) == ((a + b + c) % 16, (a + b + c) // 16) for a in range(16) for b in range(16) for c in (0, 1))
    assert all(sum(map(int, cmp4(a, b))) == 1 for a in range(16) for b in range(16))
    assert all(mux4(d, s) == int(bin(d)[2:].zfill(4)[::-1][s]) for d in range(16) for s in range(4))
    print('Comprobaciones exhaustivas: OK')
