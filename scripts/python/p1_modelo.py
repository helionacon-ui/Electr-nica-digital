"""Modelo en Python de la práctica 1 (p1_leds.vhd): reproduce qué LEDs se encienden."""
def leds(sw, btn):
    sw0, sw1 = sw & 1, (sw >> 1) & 1
    led = sw & 0xF
    led |= (sw0 & sw1) << 4
    led |= (sw0 | sw1) << 5
    led |= (sw0 ^ sw1) << 6
    led |= (btn & 1) << 7
    return led

if __name__ == '__main__':
    print('sw        btn0  led')
    for sw, btn in [(0b00000000, 0), (0b00000001, 0), (0b00000011, 0), (0b00000010, 1), (0b00001111, 1)]:
        print(f'{sw:08b}  {btn}     {leds(sw, btn):08b}')
    assert leds(0b11, 0) == 0b00110011
