library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;
library std;
use std.textio.all;

entity serializer_tb is
end serializer_tb;


architecture tb of serializer_tb is

component sort_1 is
		  port( rst_n     : in std_logic:='0';
			  Mat0      : in std_logic_vector(7 downto 0);
			  Mat1      : in std_logic_vector(7 downto 0);
			  Mat2      : in std_logic_vector(7 downto 0);
			  Mat3      : in std_logic_vector(7 downto 0);
			  Mat4      : in std_logic_vector(7 downto 0);
			  Mat5      : in std_logic_vector(7 downto 0);
			  Mat6      : in std_logic_vector(7 downto 0);
			  Mat7      : in std_logic_vector(7 downto 0);
			  Mat8      : in std_logic_vector(7 downto 0);
			  out_pixel : out std_logic_vector(7 downto 0):=(others=>'0');
			  temp1 : out std_logic_vector(7 downto 0)
			  );
end component;


signal	rst_n     	: std_logic:='1';
signal	Mat0      	: std_logic_vector(7 downto 0);
signal  Mat1      	: std_logic_vector(7 downto 0);
signal 	Mat2      	: std_logic_vector(7 downto 0);
signal	Mat3      	: std_logic_vector(7 downto 0);
signal	Mat4      	: std_logic_vector(7 downto 0);
signal	Mat5      	: std_logic_vector(7 downto 0);
signal	Mat6      	: std_logic_vector(7 downto 0);
signal	Mat7      	: std_logic_vector(7 downto 0);
signal	Mat8      	: std_logic_vector(7 downto 0);
signal	out_pixel 	: std_logic_vector(7 downto 0):=(others=>'0');
signal	temp1 		: std_logic_vector(7 downto 0);
signal 	matriz		: std_logic_vector(71 downto 0);
file	dados	: text;

begin

sort_map: sort_1 port map(rst_n,Mat0,Mat1,Mat2,Mat3,Mat4,Mat5,Mat6,Mat7,Mat8,out_pixel,temp1);

process
	variable status: file_open_status;
	variable l: line;
	variable i: integer;
	variable linedata: BIT_VECTOR(7 DOWNTO 0);
begin
	i:= 1;
	file_open(status,dados,"dados.txt",read_mode);
	assert status = open_ok
		report "Nao foi possivel abrir"
		severity failure;
	while not(endfile(dados)) loop
		readline(dados, l);
		read(l,linedata);
		matriz((i*8)-1 downto (i-1)*8)<= to_stdlogicvector(linedata);
		i:=i + 1;
		wait for 20ps;
	end loop;
	wait;	
end process;

Mat0 <= matriz(7 downto 0);
Mat1 <= matriz(15 downto 8); 
Mat2 <= matriz(23 downto 16);
Mat3 <= matriz(31 downto 24);
Mat4 <= matriz(39 downto 32);
Mat5 <= matriz(47 downto 40);
Mat6 <= matriz(55 downto 48);
Mat7 <= matriz(63 downto 56);
Mat8 <= matriz(71 downto 64);

end tb;