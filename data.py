import matplotlib.pyplot as plt 
import numpy as np 

def get_data():
    data=open("donnees-projet-gr1.txt","r")
    T=[]
    C=[]
    I=[]

    lignes=data.readlines()
    for i in lignes:

        x=i.split("\t")
        T.append(float(x[0]))
        I.append(float(x[1]))
        C.append(float(x[2].strip("\n")))


    n=len(T)

    I2=[]
    C2=[]

    for i in range(n):

        I2.append(I[n-1-i])
        C2.append(C[n-1-i])
    data.close()
    return [T,I2,C2]

def int_rectangle(I):
    S=0
    L=[]
    for i in range(len(I)):
        S+=I[i]
        L.append(S)
    return L



[T,I,C]=get_data() 
Cmax=1/(C[-1]-C[0])*int_rectangle(I)[-1]
print(int_rectangle(I)[-1])
print(Cmax)
L=int_rectangle(I)
L2=[L[i]*1/Cmax+C[0] for i in range (len(L))]
plt.plot(T,L2,label="charge calculé par le modèle")
plt.plot(T,I,label="Intensité")
plt.plot(T,C,label="Charge")
plt.legend()
plt.show()

    
