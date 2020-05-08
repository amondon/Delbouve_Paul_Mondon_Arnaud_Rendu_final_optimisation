import matplotlib.pyplot as plt
import numpy as np
Qm=10


###
def PrixHoraire(t,ph,pb):
    n=np.floor(t)
    if n%50 < 24:
        return ph
    else:
        return pb

plt.figure()
VPrixHoraire= np.vectorize(PrixHoraire)
lt=np.linspace(0,300,1000)
lx=VPrixHoraire(lt,3,2)
plt.plot(lt,lx)
plt.show()

##
def charge(I,t0,tf,c0):
    n=len(I)
    listet=np.linspace(t0,tf,n+1)
    c=c0*Qm
    charge=np.zeros(n)
    for i in range (n):
        Q=(listet[i+1]-listet[i])*(-I[i])
        c+=Q
        charge[i]=c
    return charge





##
def fcout1(I,ph,pb,t0,tf,PrixHoraire):
    n=len(I)
    listet=np.linspace(t0,tf,n+1)
    S=0
    listeS=[]
    for i in range (n):
        Q=(listet[i+1]-listet[i])*I[i]
        P=PrixHoraire(listet[i],ph,pb) #On suppose ici que l'on ne change pas de prix horaire sur l'intervalle listet[i], listet[i+1]

        S+=P*Q
        listeS.append(S)
    return S,np.array(listeS)

##
def gradfcout(n,ph,pb,t0,tf,PrixHoraire):
    listet=np.linspace(t0,tf,n+1)
    G=np.zeros(n)
    for i in range (n):
        p=PrixHoraire(listet[i],ph,pb)
        q=(listet[i+1]-listet[i])
        G[i]=p*q
    return G

##
def C(I,t0,tf,PrixHoraire,Im,cf,c0):
    n=len(I)
    A=np.zeros ((2*n+2,n))
    listet=np.linspace(t0,tf,n+1)
    # Contrainte égalité
    A[0,:]=np.array([listet[i+1]-listet[i] for i in range (n)])
    A[1,:]=-np.array([listet[i+1]-listet[i] for i in range (n)])
    #Contraintes égalités
    for i in range (n):
        A[i+2,i]=1
        A[n+i+2,i]=-1
    B=np.zeros(2*n+2)
    B[0]=(cf-c0)*Qm
    B[1]=-(cf-c0)*Qm
    for i in range(2,len(B)):
        B[i]=Im
    c=np.dot(A,I)-B
    return c

##
def gradC(n,t0,tf,PrixHoraire,Im,cf,c0):
    A=np.zeros ((2*n+2,n))
    listet=np.linspace(t0,tf,n+1)
    A[0,:]=np.array([listet[i+1]-listet[i] for i in range (n)])
    A[1,:]=-np.array([listet[i+1]-listet[i] for i in range (n)])
    for i in range (n):
        A[i+2,i]=1
        A[n+i+2,i]=-1
    return A

##
def Algo(n,t0,tf,PrixHoraire,Im,cf,c0,l, max_iter, rho ,ph,pb, epsilon=1e-8):
    #reprise de Uzawa
    lamb=np.array([1 for i in range (2*n+2)])
    x0 = np.array([0.for i in range(n)])
    A=gradC(n,t0,tf,PrixHoraire,Im,cf,c0)
    G=gradfcout(n,ph,pb,t0,tf,PrixHoraire)
    Lap=G+np.dot(lamb,A)
    xk=x0
    k=0
    while (k<max_iter) and (np.linalg.norm(G+np.dot(lamb,A))>epsilon):
        k+=1
        xk+=-l*(G+np.dot(lamb,A))
        lamb=lamb+rho*l*C(xk,t0,tf,PrixHoraire,Im,cf,c0)
        print(np.linalg.norm(G+np.dot(lamb,A)))
    print(k)
    return xk

##graph
I=Algo(299,0,299,PrixHoraire,5,1,0.2,0.001,1000,0.1,0.8,0.3)
ly=fcout1(-np.array(I),0.5,0.1,0,299,PrixHoraire)[1]
lt=np.linspace(0,299,299)
lc=charge(I,0,299,0.2)
lp=np.vectorize(PrixHoraire)(lt,0.5,0.1)
plt.figure()
plt.plot(lt,ly,label="Coût")
plt.plot(lt,I,label="Intensité")
plt.plot(lt,lc,label="Charge")
plt.plot(lt,lp,label="Prix horaire")
plt.show()