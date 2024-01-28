PROGRAM V1;

TYPE
  myArray = array [0..50] of integer;

VAR
  arr : myArray;
  index, temp : integer;

FUNCTION factorial(n : integer) : integer;
VAR
  res : integer;
  counter : integer;
begin
  counter := 1;
  for counter := 1 to n do 
    res := res * counter;
  factorial := res;
end;

begin
  for index := 0 to 50 do begin
    temp := factorial(index);
    arr[index] := temp;
  end;
end.