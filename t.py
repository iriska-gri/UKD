import re


pcode = [1.1,'10',"2.3","1.1.31","1.1.4.1","1.1.3","5_ЮЛ"]
for x in pcode:
    
    
    x=re.sub(r'[_a-zA-Zа-яА-ЯёЁ]',"",str(x))    
    y=x.split(".")    
    y=y[0] +"."+ "".join(y[1:])
    print(float(y))
    