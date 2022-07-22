import matplotlib.pyplot as plt
from math import floor,ceil

#----- INPUT PARAMETERS -----

#Always put 0 and the last prod file
files_unsat=['POPC_unsaturated.agr','POPS_unsaturated.agr']
files_sat=['POPC_saturated.agr','POPS_saturated.agr']
#Path for the files
path='C://Users//antoi//OneDrive - Université Paris Sciences et Lettres//Stage//Figures/order_parameters/'

#----- END OF INPUT PARAMETERS -----

#----- FUNCTIONS -----

def readxvg(name):
    newpath=path+name
    fichier=open(newpath,'r')
    brut=fichier.readlines()
    fichier.close()
    #Each line is stored in a str
    final=[]
    for line in brut[8:]:
        aux=[]
        for item in line[:-1].split('\t'):
            if item!='': aux.append(float(item))
        final.append(aux)
    return final

def plotlist(list):
    #Contains only x and y
    X,Y=[],[]
    for item in list:
        X.append(item[0])
        Y.append(item[1])
    return X,Y

plt.clf()
#2 figures
plt.subplot(1,2,1,title='(a) Unsaturated chain',xlabel='Carbon Number',ylabel='$-S_{CD}$')
X,Y=plotlist(readxvg(files_unsat[0]))
plt.plot(X,Y,c='orange',label='POPC')
X,Y=plotlist(readxvg(files_unsat[1]))
plt.plot(X,Y,label='POPS')
plt.subplot(1,2,2,xlabel='Carbon Number',ylabel='$-S_{CD}$',title='(b) Saturated chain')
X,Y=plotlist(readxvg(files_sat[0]))
plt.plot(X,Y,c='orange',label='POPC')
X,Y=plotlist(readxvg(files_sat[1]))
plt.plot(X,Y,label='POPS')
plt.legend(loc='center right',bbox_to_anchor=(1.25, 0.5))
plt.show()