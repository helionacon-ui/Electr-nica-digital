-- Práctica 3: antirrebote. La salida sigue a la entrada solo si esta permanece estable LIM ciclos.
-- Con reloj de 50 MHz y LIM = 1_000_000 el filtro espera 20 ms.
library ieee;
use ieee.std_logic_1164.all;

entity p3_antirrebote is
  generic ( LIM : positive := 1_000_000 );
  port (
    clk, btn : in  std_logic;
    limpio   : out std_logic
  );
end p3_antirrebote;

architecture rtl of p3_antirrebote is
  signal s1, s2 : std_logic := '0';           -- sincronizador de dos biestables
  signal prev   : std_logic := '0';
  signal cnt    : integer range 0 to LIM := 0;
  signal sal    : std_logic := '0';
begin
  process (clk)
  begin
    if rising_edge(clk) then
      s1 <= btn;  s2 <= s1;                   -- evita la metaestabilidad
      if s2 /= prev then                      -- la entrada ha cambiado: reinicia la cuenta
        prev <= s2;
        cnt  <= 0;
      elsif cnt = LIM then
        sal  <= prev;                         -- estable el tiempo suficiente: se acepta
      else
        cnt  <= cnt + 1;
      end if;
    end if;
  end process;
  limpio <= sal;
end rtl;
