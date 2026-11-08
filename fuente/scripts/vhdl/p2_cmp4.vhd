-- Práctica 2: comparador de 4 bits.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity p2_cmp4 is
  port (
    a, b       : in  std_logic_vector(3 downto 0);
    gt, eq, lt : out std_logic
  );
end p2_cmp4;

architecture rtl of p2_cmp4 is
begin
  gt <= '1' when unsigned(a) >  unsigned(b) else '0';
  eq <= '1' when unsigned(a) =  unsigned(b) else '0';
  lt <= '1' when unsigned(a) <  unsigned(b) else '0';
end rtl;
