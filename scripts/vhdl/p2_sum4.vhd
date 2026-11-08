-- Práctica 2: sumador de 4 bits con acarreo de entrada y de salida.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity p2_sum4 is
  port (
    a, b : in  std_logic_vector(3 downto 0);
    cin  : in  std_logic;
    s    : out std_logic_vector(3 downto 0);
    cout : out std_logic
  );
end p2_sum4;

architecture rtl of p2_sum4 is
  signal t : unsigned(4 downto 0);        -- un bit más para el acarreo
begin
  t    <= ('0' & unsigned(a)) + ('0' & unsigned(b)) + ("0000" & cin);
  s    <= std_logic_vector(t(3 downto 0));
  cout <= t(4);
end rtl;
