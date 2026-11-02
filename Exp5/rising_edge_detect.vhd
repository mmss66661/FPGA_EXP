-- Counts the rising edges of the debounced key pulse, 4 decimal digits output
library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity rising_edge_detect is
    port(
        KEY_IN : in  std_logic;
        D      : out std_logic_vector(15 downto 0)
    );
end rising_edge_detect;

architecture behav of rising_edge_detect is
    signal d0, d1, d2, d3 : unsigned(3 downto 0) := (others => '0');
begin
    process(KEY_IN)
    begin
        if rising_edge(KEY_IN) then
            if d0 = 9 then
                d0 <= (others => '0');
                if d1 = 9 then
                    d1 <= (others => '0');
                    if d2 = 9 then
                        d2 <= (others => '0');
                        if d3 = 9 then
                            d3 <= (others => '0');
                        else
                            d3 <= d3 + 1;
                        end if;
                    else
                        d2 <= d2 + 1;
                    end if;
                else
                    d1 <= d1 + 1;
                end if;
            else
                d0 <= d0 + 1;
            end if;
        end if;
    end process;

    D <= std_logic_vector(d3) & std_logic_vector(d2) &
         std_logic_vector(d1) & std_logic_vector(d0);
end behav;
