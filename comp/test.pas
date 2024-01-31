PROGRAM V1;

TYPE
  myArray = array[1..10, 1..10] of integer;

VAR
  i, b : integer;
  arr : myArray;
  flag : boolean;

FUNCTION test(arr: myArray) : myArray;
Var
  i, j : integer;
  ret_array : array[1..10, 1..10] of integer;

begin
  for i := 1 to 10 do
    for j := 1 to 10 do
      ret_array[i,j] := i * j;
  test := ret_array;
end;
  
begin
  i := -(i + 1) + 3;
end.