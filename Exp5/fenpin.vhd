-- 50 MHz clock divider for experiment 5
library ieee;
use ieee.std_logic_1164.all;

entity fenpin is
    port(
        clk_50M  : in  std_logic;
        clk_5M   : out std_logic;
        clk_500k : out std_logic;
        clk_10k  : out std_logic;
        clk_5k   : out std_logic;
        clk_500  : out std_logic;
        clk_50   : out std_logic;
        clk_1    : out std_logic
    );
end fenpin;

architecture behav of fenpin is
    signal s5M, s500k, s10k, s5k, s500, s50, s1 : std_logic := '0';
begin
    process(clk_50M)
        variable n5M   : integer range 0 to 4        := 0;
        variable n500k : integer range 0 to 49       := 0;
        variable n10k  : integer range 0 to 2499     := 0;
        variable n5k   : integer range 0 to 4999     := 0;
        variable n500  : integer range 0 to 49999    := 0;
        variable n50   : integer range 0 to 499999   := 0;
        variable n1    : integer range 0 to 24999999 := 0;
    begin
        if rising_edge(clk_50M) then
            if n5M = 4 then
                n5M := 0;
                s5M <= not s5M;
            else
                n5M := n5M + 1;
            end if;
            if n500k = 49 then
                n500k := 0;
                s500k <= not s500k;
            else
                n500k := n500k + 1;
            end if;
            if n10k = 2499 then
                n10k := 0;
                s10k <= not s10k;
            else
                n10k := n10k + 1;
            end if;
            if n5k = 4999 then
                n5k := 0;
                s5k <= not s5k;
            else
                n5k := n5k + 1;
            end if;
            if n500 = 49999 then
                n500 := 0;
                s500 <= not s500;
            else
                n500 := n500 + 1;
            end if;
            if n50 = 499999 then
                n50 := 0;
                s50 <= not s50;
            else
                n50 := n50 + 1;
            end if;
            if n1 = 24999999 then
                n1 := 0;
                s1 <= not s1;
            else
                n1 := n1 + 1;
            end if;
        end if;
    end process;

    clk_5M   <= s5M;
    clk_500k <= s500k;
    clk_10k  <= s10k;
    clk_5k   <= s5k;
    clk_500  <= s500;
    clk_50   <= s50;
    clk_1    <= s1;
end behav;
