-- Práctica 2: multiplexor 4 a 1 (dos descripciones equivalentes).
library ieee;
use ieee.std_logic_1164.all;

entity p2_mux4 is
  port (
    d   : in  std_logic_vector(3 downto 0);
    sel : in  std_logic_vector(1 downto 0);
    y   : out std_logic
  );
end p2_mux4;

architecture rtl of p2_mux4 is
begin
  with sel select
    y <= d(0) when "00",
         d(1) when "01",
         d(2) when "10",
         d(3) when others;
end rtl;
