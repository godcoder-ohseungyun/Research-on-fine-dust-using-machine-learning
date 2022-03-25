# 기간 생성기
annual = ['']
semi_annual = ['01','02']
quarterly = ['01','02','03','04']
monthly = ['01','02','03','04','05','06','07','08','09','10','11','12']


#반기  01  02
def makeCycle(startY,endY,cycle):
    result = []

    for a in range(startY,endY+1):
        stra = str(a)
        for i in cycle:
            result.append(int(stra+i))

    return result


print(makeCycle(2012,2020,monthly))
