-- BCD to 7-segment (active low, DE10-Lite) display interface
library ieee;
use ieee.std_logic_1164.all;

entity seg_show is
    port(
        Num  : in  std_logic_vector(15 downto 0);
        HEX0 : out std_logic_vector(7 downto 0);
        HEX1 : out std_logic_vector(7 downto 0);
        HEX2 : out std_logic_vector(7 downto 0);
        HEX3 : out std_logic_vector(7 downto 0)
    );
end seg_show;

architecture behav of seg_show is
    function seg(bcd : std_logic_vector(3 downto 0)) return std_logic_vector is
        variable s : std_logic_vector(7 downto 0);
    begin
        case bcd is
            when "0000" => s := "11000000";   -- 0, dp off
            when "0001" => s := "11111001";   -- 1
            when "0010" => s := "10100100";   -- 2
            when "0011" => s := "10110000";   -- 3
            when "0100" => s := "10011001";   -- 4
            when "0101" => s := "10010010";   -- 5
            when "0110" => s := "10000010";   -- 6
            when "0111" => s := "11111000";   -- 7
            when "1000" => s := "10000000";   -- 8
            when "1001" => s := "10010000";   -- 9
            when others => s := "11111111";   -- blank
        end case;
        return s;
    end function;
begin
    HEX0 <= seg(Num(3 downto 0));
    HEX1 <= seg(Num(7 downto 4));
    HEX2 <= seg(Num(11 downto 8));
    HEX3 <= seg(Num(15 downto 12));
end behav;
