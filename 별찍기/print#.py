height = int(input("높이를 입력하세요: "))

for i in range(height):
    if i == 1 : 
        print('#'*(height+12))
    if i == height - 2:
        print('#'*(height+12))
    else:
        for j in range(height - i - 1):
            print(' ', end='')
        print('#','  '*3,'#')


