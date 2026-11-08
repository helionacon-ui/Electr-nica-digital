-- Práctica 3: divisor de frecuencia. Con reloj de 50 MHz y DIV = 50_000_000 da una salida de 1 Hz.
library ieee;
use ieee.std_logic_1164.all;

entity p3_divisor is
  generic ( DIV : positive := 50_000_000 );     -- relación f_in / f_out (número par)
  port (
    clk, rst : in  std_logic;
    clk_out  : out std_logic
  );
end p3_divisor;

architecture rtl of p3_divisor is
  signal cnt : integer range 0 to DIV/2 - 1 := 0;
  signal s   : std_logic := '0';
begin
  process (clk, rst)
  begin
    if rst = '1' then
      cnt <= 0; s <= '0';
    elsif rising_edge(clk) then
      if cnt = DIV/2 - 1 then
        cnt <= 0;
        s   <= not s;                           -- conmuta cada medio periodo
      else
        cnt <= cnt + 1;
      end if;
    end if;
  end process;
  clk_out <= s;
end rtl;
