length = int(input("길이를 입력하세요"))
 
for i in range(length, 0, -1):
    # 앞의 공백
    print("  " * (length), end='')
    print(" " * i, end='')
    # 첫 번째 별
    print("☆", end='')
 
    # 별 사이의 공백
    if i != length:
        print("  " * (length - i - 1), end='')
        print("☆", end='')
 
    print()
 
for i in range(length // 2 + length % 2):
    print(" "*(length - length//2), end='')
    if i == 0:
        print("☆" * length, end='')
        print("  " * (length - (length-3)//2), end='')
        print("☆" * length, end='')
    else:
        print(" "*((length//2-1)+i),"☆"," "*((length//2+1)-i),end='')
        print(" " * (length*2-1), end='')
        print(" "*((length//2+1)-i),"☆",end='')
    print()
margin = 0
for i in range(length,0,-1):
    print(" " * (length - length // 2), end='')
    print(" "* i,'☆',end='')
    if i != 0:
        if i> 2:
            print(" " * (i-2), '☆', end='')
        elif i ==1:
            print('', end='')
        else:
            print('☆', end='')
    if i != 0:
 
        if i == length:
            print(" " * (i-2), '☆', end='')
        elif i == length-1:
            print(" "*1*2,end='☆')
        else:
            #print(length-i,end='')
            print(" "*(6*(length-i-1)+margin),end='☆')
            margin -=(length-i-2)
    if i != 0:
        if i == length:
            print()
            continue
        if i> 2:
            print(" " * (i-2), '☆', end='')
        elif i ==1:
            print('', end='')
        else:
            print('☆', end='')
    print()