PROGRAM V1;

TYPE
  myArray = array[1..10] of integer;

VAR
  arr : myArray;
  i : integer;

FUNCTION countAverage(temp : array [1..10] of integer; n : integer) : real;
VAR
  i : integer;
  sum : integer;
begin
  for i := 1 to n do
    sum := sum + temp[i];
  countAverage := sum / n;
end;
begin
  for i := 1 to 10 do
    arr[i] := i;
  countAverage(arr, 10);
end.