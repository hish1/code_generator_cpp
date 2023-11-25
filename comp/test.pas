PROGRAM V1;

CONST
  N = 10;

TYPE
  customArray = array [1..N] of integer;

VAR
  i : integer;
  arr : customArray;

PROCEDURE sortArray(arr : customArray; N : integer);
VAR
  i, j : integer;
  temp : integer;
begin
  for i := 1 to N do begin
    for j := 1 to N do begin
      if arr[i] < arr[j] then begin
        temp := arr[i];
        arr[i] := arr[j];
        arr[j] := arr[i];
      end;
    end;
  end;
end;

begin
   for i := 1 to N do begin
    arr[i] := i * i;
   end;
end.