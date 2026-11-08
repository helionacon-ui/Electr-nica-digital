-- Práctica 3: contador síncrono de módulo N con reset asíncrono y habilitación.
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity p3_contador is
  generic ( N : positive := 10 );
  port (
    clk, rst, en : in  std_logic;
    q            : out std_logic_vector(3 downto 0);
    fin          : out std_logic                       -- vale 1 en el último estado
  );
end p3_contador;

architecture rtl of p3_contador is
  signal cnt : unsigned(3 downto 0) := (others => '0');
begin
  process (clk, rst)
  begin
    if rst = '1' then
      cnt <= (others => '0');
    elsif rising_edge(clk) then
      if en = '1' then
        if cnt = N - 1 then
          cnt <= (others => '0');
        else
          cnt <= cnt + 1;
        end if;
      end if;
    end if;
  end process;

  q   <= std_logic_vector(cnt);
  fin <= '1' when cnt = N - 1 else '0';
end rtl;
