class CycleMaker:
        #수집기간 분류
        annual = ['']
        semi_annual = ['01','02']
        quarterly = ['01','02','03','04']
        monthly = ['01','02','03','04','05','06','07','08','09','10','11','12']

        def makeCycle(self,cycle):
            result = []

            for a in range(2012,2023): #2012~2022  # 여기 범위를 수정해주기만하면 수집기간을 자유롭게 설정가능
                stra = str(a)
                for i in cycle:
                    result.append(int(stra+i))

            return result

        # 분기 반기 주기 월기는 더이상 분화하지 않기때문에 하드코딩으로 한다.
        def getCycle(self,cycleCode):

            if(cycleCode == "annual"):
                return self.makeCycle(CycleMaker.annual)

            if(cycleCode == "semi_annual"):
                return self.makeCycle(CycleMaker.semi_annual)

            if(cycleCode == "quarterly"):
                return self.makeCycle(CycleMaker.quarterly)

            if(cycleCode == "monthly"):
                return self.makeCycle(CycleMaker.monthly)