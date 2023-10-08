Below is example output, (you can't see the colours do appear when running in terminal)

```
letters: siatnoyodhdverhetrmoe
colors: gyyygyywwwgwywwwgwywg
S I A T N 
O   Y   O 
D H D V E 
R   H   E 
T R M O E 
OK?y
(563 options, 40+21 items, 3122 entries successfully read)
Altogether 1 solution, 156935+1727951 mems, 105575 updates, 15332 cleansings, 52540 bytes, 1001 nodes, ccost 3%.
1:
S A T I N 
H   O   E 
O R D E R 
O   D   V 
T H Y M E 

Solution possible in 10 swaps
We have a cycle: [0]
We have a cycle: [4]
We have a cycle: [10]
We have a cycle: [16]
We have a cycle: [20]
We have a cycle: [9, 17]
Swap 17 and 9
S I A T N 
O   Y   O 
D R D V E 
R   H   E 
T H M O E 


We have a cycle: [11, 15]
Swap 15 and 11
S I A T N 
O   Y   O 
D R D E E 
R   H   V 
T H M O E 


We have a cycle: [1, 2, 3]
Swap 2 and 1
S A I T N 
O   Y   O 
D R D E E 
R   H   V 
T H M O E 


Swap 3 and 2
S A T I N 
O   Y   O 
D R D E E 
R   H   V 
T H M O E 


We have a cycle: [5, 14, 8]
Swap 14 and 5
S A T I N 
H   Y   O 
D R D E E 
R   O   V 
T H M O E 


Swap 8 and 14
S A T I N 
H   Y   O 
O R D E E 
R   D   V 
T H M O E 


We have a cycle: [6, 19, 18]
Swap 19 and 6
S A T I N 
H   O   O 
O R D E E 
R   D   V 
T H M Y E 


Swap 18 and 19
S A T I N 
H   O   O 
O R D E E 
R   D   V 
T H Y M E 


We have a cycle: [7, 12, 13]
Swap 12 and 7
S A T I N 
H   O   E 
O R D E O 
R   D   V 
T H Y M E 


Swap 13 and 12
S A T I N 
H   O   E 
O R D E R 
O   D   V 
T H Y M E 
```