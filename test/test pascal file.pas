PROGRAM V1;

TYPE
  customArray = array[10..20] of integer;
  myInt = integer;

Var
  a, b, c : myInt;
  
begin
  a := 10;
  b := a;
  c := b;
  for a:= 1 to 10 do 
    b := b + 1;
end.