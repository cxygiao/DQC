# distributed_circuit_partition
Our code is still being improved！

This is the result of our division of partial quantum circuits. By changing the line order of quantum circuits, the transmission cost of distributed circuits is changed. The following division results can calculate a relatively optimal transmission cost.
## 4gt5-76
initial line sequence：ABCDE

optimized line sequence：ABCDE
![2022-09-26 13 18 16](https://user-images.githubusercontent.com/114378123/192199058-9d99f9a4-c783-4bd1-bc4b-9440e1e4704f.png)
### merged transfer
<img width="762" alt="image" src="https://user-images.githubusercontent.com/114378123/193528165-987603d0-1cdf-4e9b-bf35-783f8954ac8e.png">
<img width="762" alt="image" src="https://user-images.githubusercontent.com/114378123/193528097-805ce4a5-83f9-4e41-ae4a-d4515c1ac8a3.png">


## 4gt11-82
initial line sequence：ABCDE

optimized line sequence：ABCDE
![4gt11-82](https://user-images.githubusercontent.com/114378123/192195731-89b9dafa-7afd-470b-9a34-a411237010ce.png)
### merged transfer
<img width="752" alt="image" src="https://user-images.githubusercontent.com/114378123/193528384-544ddb6e-997b-4cd9-8cfc-c47e735f362e.png">
<img width="752" alt="image" src="https://user-images.githubusercontent.com/114378123/193528485-cdbe3466-043e-4104-b85e-65987195c826.png">


## mini-alu-305
initial line sequence：ABCDEFGHIJ 

optimized line sequence：ABCFGDEHIJ
![Min-alu-305](https://user-images.githubusercontent.com/114378123/192197008-afeebafc-d64d-404e-8b6d-6a79d44dadfc.png)
### merged transfer

## parity-247
initial line sequence：ABCDEFGHIJKL 

optimized line sequence：ABCDEFGHIJKL 
![parity_247](https://user-images.githubusercontent.com/114378123/192197032-ef42003b-35ee-409f-a221-765bc32f9780.png)
# sym9-147
initial line sequence：ABCDEFGHIJKL 

optimized line sequence：ABDFHICEGJKL
![Sym9-147](https://user-images.githubusercontent.com/114378123/193457591-06358d0f-be93-4119-bb43-568eba242072.png)
## sym6-316
initial line sequence：ABCDEFGHIJKLMN 

optimized line sequence：ACEFGHIBDJKLMN
![Sym6-316](https://user-images.githubusercontent.com/114378123/192197055-88fd471b-4bcc-4f4a-865f-471b7ebfcdc1.png)
## ham7-299
initial line sequence：ABCDEFGHIJKLMNOPQRSTU 

optimized line sequence：ACDJLNOPSUBEFHIKMQRT
![Ham7-299](https://user-images.githubusercontent.com/114378123/192196245-9642e076-0ff2-41aa-9759-f5fe6ec8fbd4.png)

