-- Práctica 1: entradas y salidas de la placa Basys.
-- Cada interruptor enciende el LED de su mismo número.
library ieee;
use ieee.std_logic_1164.all;

entity p1_leds is
  port (
    sw  : in  std_logic_vector(7 downto 0);   -- interruptores
    btn : in  std_logic_vector(3 downto 0);   -- pulsadores
    led : out std_logic_vector(7 downto 0)    -- LEDs
  );
end p1_leds;

architecture flujo of p1_leds is
begin
  -- Los 4 LEDs bajos copian los interruptores; los 4 altos muestran un AND y un OR de ejemplo.
  led(3 downto 0) <= sw(3 downto 0);
  led(4) <= sw(0) and sw(1);          -- AND
  led(5) <= sw(0) or  sw(1);          -- OR
  led(6) <= sw(0) xor sw(1);          -- XOR
  led(7) <= btn(0);                   -- el pulsador 0 enciende el LED 7
end flujo;
