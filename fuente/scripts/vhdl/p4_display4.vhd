-- Práctica 4: manejo multiplexado de un display de 4 dígitos (Basys). Muestra 4 cifras BCD.
-- Se enciende un dígito cada vez. Con reloj de 50 MHz se cambia de dígito a 762,9 Hz (50e6/2^16)
-- y cada dígito se refresca a 190,7 Hz: el ojo los ve todos encendidos y sin parpadeo.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity p4_display4 is
  port (
    clk    : in  std_logic;                        -- 50 MHz
    d3, d2, d1, d0 : in std_logic_vector(3 downto 0);
    seg    : out std_logic_vector(6 downto 0);     -- activos a nivel bajo
    an     : out std_logic_vector(3 downto 0)      -- ánodos, activos a nivel bajo
  );
end p4_display4;

architecture rtl of p4_display4 is
  signal cnt : unsigned(17 downto 0) := (others => '0');   -- 2^16 ciclos por dígito
  signal sel : std_logic_vector(1 downto 0);
  signal dig : std_logic_vector(3 downto 0);
begin
  process (clk)
  begin
    if rising_edge(clk) then cnt <= cnt + 1; end if;
  end process;
  sel <= std_logic_vector(cnt(17 downto 16));

  with sel select dig <= d0 when "00", d1 when "01", d2 when "10", d3 when others;
  with sel select an  <= "1110" when "00", "1101" when "01", "1011" when "10", "0111" when others;

  with dig select
    seg <= "0000001" when "0000", "1001111" when "0001", "0010010" when "0010",
           "0000110" when "0011", "1001100" when "0100", "0100100" when "0101",
           "0100000" when "0110", "0001111" when "0111", "0000000" when "1000",
           "0000100" when "1001", "1111111" when others;
end rtl;
