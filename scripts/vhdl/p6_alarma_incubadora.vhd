-- Prácticas 5 a 7 (ejemplo de módulo): alarma de temperatura con histéresis para un sistema de monitorización.
-- Entrada: temperatura en décimas de grado (0 a 1023). Salidas: alarma de alta y de baja.
-- La histéresis evita que la alarma parpadee cuando la medida oscila alrededor del umbral.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity p6_alarma is
  generic (
    T_ALTA  : natural := 375;    -- 37,5 °C: se activa la alarma de alta
    T_BAJA  : natural := 360;    -- 36,0 °C: se activa la alarma de baja
    HIST    : natural := 5       -- 0,5 °C de histéresis
  );
  port (
    clk, rst : in  std_logic;
    temp     : in  std_logic_vector(9 downto 0);
    al_alta  : out std_logic;
    al_baja  : out std_logic
  );
end p6_alarma;

architecture rtl of p6_alarma is
  signal t : unsigned(9 downto 0);
  signal a, b : std_logic := '0';
begin
  t <= unsigned(temp);
  process (clk, rst)
  begin
    if rst = '1' then
      a <= '0'; b <= '0';
    elsif rising_edge(clk) then
      if    t >= T_ALTA        then a <= '1';
      elsif t <  T_ALTA - HIST then a <= '0';
      end if;
      if    t <  T_BAJA        then b <= '1';
      elsif t >= T_BAJA + HIST then b <= '0';
      end if;
    end if;
  end process;
  al_alta <= a;
  al_baja <= b;
end rtl;
