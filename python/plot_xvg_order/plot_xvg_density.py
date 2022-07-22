import matplotlib.pyplot as plt
from math import floor,ceil

#----- INPUT PARAMETERS -----

#Always put 0 and the last prod file
files=['density_POPS_72.xvg']
#Path for the files
path='C://Users//antoi//OneDrive - Université Paris Sciences et Lettres//Stage//Figures/Density_plot/'

#----- END OF INPUT PARAMETERS -----

#----- FUNCTIONS -----

def readxvg(name):
    newpath=path+name
    fichier=open(newpath,'r')
    brut=fichier.readlines()
    fichier.close()
    #Each line is stored in a str
    final=[]
    for line in brut[27:]:
        aux=[]
        for item in line[:-1].split(' '):
            if item!='': aux.append(float(item))
        final.append(aux)
    return final

def plotlist(list):
    #Contains only x and y
    X,A,B,C,D=[],[],[],[],[]
    for item in list:
        X.append(item[0])
        A.append(item[1])
        B.append(item[2])
        C.append(item[3])
        D.append(item[4])
    return X,A,B,C,D

plt.clf()
Total=[]
ax=plt.axes()
ax.set_xlabel('$z$ coordinate (nm)')
ax.set_ylabel('Density (kg.m$^{-3}$)')
X,Water,Head,Glyc,Acyl=plotlist(readxvg(files[0]))
for i in range(0,len(Water)):
    Total.append(Water[i]+Head[i]+Glyc[i]+Acyl[i])
plt.plot(X,Water,label='Bulk Water')
plt.fill_between(X,Water,alpha=0.4)
plt.plot(X,Head,label='Headgroups')
plt.fill_between(X,Head,alpha=0.4)
plt.plot(X,Glyc,label='Glycerol Ester')
plt.fill_between(X,Glyc,alpha=0.4)
plt.plot(X,Acyl,label='Acyl Chains')
plt.fill_between(X,Acyl,alpha=0.4)

plt.plot(X,Total,label='Total',linewidth=3)
plt.legend()
plt.show()