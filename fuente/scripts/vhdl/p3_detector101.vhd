-- Práctica 3: máquina de estados. Detector Mealy de la secuencia 101 con solape.
library ieee;
use ieee.std_logic_1164.all;

entity p3_detector101 is
  port (
    clk, rst, x : in  std_logic;
    z           : out std_logic
  );
end p3_detector101;

architecture rtl of p3_detector101 is
  type estado_t is (S0, S1, S2);
  signal est, sig : estado_t := S0;
begin
  -- Proceso 1: registro de estado (parte secuencial)
  process (clk, rst)
  begin
    if rst = '1' then
      est <= S0;
    elsif rising_edge(clk) then
      est <= sig;
    end if;
  end process;

  -- Proceso 2: lógica de siguiente estado y de salida (parte combinacional)
  process (est, x)
  begin
    z <= '0';
    case est is
      when S0 =>
        if x = '1' then sig <= S1; else sig <= S0; end if;
      when S1 =>
        if x = '0' then sig <= S2; else sig <= S1; end if;
      when S2 =>
        if x = '1' then sig <= S1; z <= '1'; else sig <= S0; end if;
    end case;
  end process;
end rtl;
