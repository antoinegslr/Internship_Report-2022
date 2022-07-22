from mpl_toolkits import mplot3d
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
from time import sleep
#matplotlib.use("pgf")
#matplotlib.rcParams.update({
#    "pgf.texsystem": "pdflatex",
#    'font.family': 'serif',
#    'text.usetex': True,
#    'pgf.rcfonts': False,
#})

#x=CR, y=temps, z=energie

totalBrut=[]
pas=5 #En ns
nb_end=35
# Pulling protocol is in Downloads, here it is Convergence for Insertion (corrected)
#chemin='C://Users//antoi//OneDrive - Université Paris Sciences et Lettres//Stage//Figures//CV Wham US pep insert/profile_'
#Insertion protocol
chemin='C://Users//antoi//OneDrive - Université Paris Sciences et Lettres//Stage//Figures/Convergence US_ins (corrected)/profile_'
for i in range(0,nb_end+1):
    path=chemin+str(i)+'.xvg'
    fichier=open(path,'r')
    listeBrute=fichier.readlines()
    totalBrut.append(listeBrute)
    fichier.close()

def traduction(ligne):
    #Structure du xvg : Coordonnée Réactionnelle, Energie
    res=[]
    for ele in ligne.split('\t'):
        if '\n' in ele:
            res.append(float(ele[:-1]))
            continue
        res.append(float(ele))
    return res

totalTrad=[]
time=-5
maxlen=0
thislen=0
for ite in totalBrut:
    time+=5
    for ligne in ite:
        if ligne[0]=='@' or ligne[0]=='#': continue
        totalTrad.append([time]+traduction(ligne))
        thislen+=1
    if maxlen<thislen: maxlen=thislen
    thislen=0

X,Y,Z=[],[],[]
for item in totalTrad:
    X.append(item[0])
    Y.append(item[1])
    Z.append(item[2])


#Z_grid=[[0]*maxlen]*nb_end
#for i in range(0,nb_end):
#    for j in range(0,maxlen):
#        Z_grid[i][j]=Z[i*35+j]


#fig = plt.figure()
#ax0 = plt.axes()
#c = ax0.pcolor(Z_grid[0:])
#ax0.set_title('No edge image')
#plt.show()



fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('Time of simulation (ns)')
ax.set_ylabel('z coordinate (nm)')
ax.set_zlabel('Potential Mean Force (kJ/mol)');
#p=ax.scatter(X, Y, Z, c=Z, cmap='plasma', linewidth=0.5);
#fig.colorbar(p)
ax.plot_trisurf(X, Y, Z, cmap='plasma', edgecolor='none');
#ax.plot_trisurf(X, Y, Z, cmap='plasma_r', edgecolor='none');
#ax.scatter(X, Y, Z, c=Z, cmap='viridis', linewidth=0.5);
plt.show()
#plt.savefig('C://Users//antoi//Documents//Python//Surface Membrane Drawer/histogram.pgf')
#On veut maintenant afficher avec des boules tout sauf POPS, TIP3, SOD, CLA...


##
fig2=plt.figure()
ax=plt.axes()
listeX=[]
listeY=[]
mean=[]
for i in range(0,nb_end+1):
    listeY.append(Z[(200*i)+99])
    listeX.append(X[(200*i)+99])
    aux=0
    for item in listeY:
        aux+=item
    mean.append(aux/len(listeY))
ax.plot(listeX,listeY)
ax.plot(listeX,mean)
fig2.suptitle('Energetic profile at z=0')
ax.set_xlabel('Time of simulation (ns)')
ax.set_ylabel('Potential of Mean Force (kJ/mol)')
plt.show()
fig2=plt.figure()
ax=plt.axes()
listeX=[]
listeY=[]
mean=[]
for i in range(0,nb_end+1):
    listeY.append(Z[(200*i)+199])
    listeX.append(X[(200*i)+199])
    aux=0
    for item in listeY:
        aux+=item
    mean.append(aux/len(listeY))
ax.plot(listeX,listeY)
ax.plot(listeX,mean)
fig2.suptitle('Energetic profile at z=4')
ax.set_xlabel('Time of simulation (ns)')
ax.set_ylabel('Potential of Mean Force (kJ/mol)')
plt.show()
##2D Plot with error bars
#X contains time
#Y contains z position
#Z contains PMF value
#Goal is to show mean PMF as a fonction of z first
fig3=plt.figure()
ax=plt.axes()
axeZ=[]
PMF=[]
upPMF=[]
downPMF=[]
begin=4
for i in range(0,200):
    aux=Z[i+begin*200]
    zcoo=Y[i+begin*200]
    up,down=Z[i+begin*200],Z[i+begin*200]
    for j in range(begin+1,nb_end+1):
        aux+=Z[j*200+i]
        zcoo+=Y[j*200+i]
        if Z[j*200+i]>up: up=Z[j*200+i]
        if Z[j*200+i]<down: down=Z[j*200+i]
    aux/=(nb_end-begin+1)
    zcoo/=(nb_end-begin+1)
    upPMF.append(up)
    downPMF.append(down)
    PMF.append(aux)
    axeZ.append(zcoo)

ax.fill_between(axeZ,downPMF,upPMF,facecolor='lightgray')
ax.plot(axeZ,PMF,label='Pure POPS membrane',c='black')
ax.set_xlabel('Coordinate along the z-axis (nm)')
ax.set_ylabel('Potential of Mean Force (kJ/mol)')
symPMF=[]
for i in range(0,100):
    symPMF.append(PMF[i])
for i in range(99,-1,-1):
    symPMF.append(symPMF[i])
ax.plot(axeZ,symPMF,label='Symmetrized curve',c='orange')
ax.legend()
plt.show()

##2D Plot of consecutive curves
curves=[]
Zvalues=[]
for i in range(0,nb_end+1):
    aux=[]
    Zaux=[]
    for j in range(0,200):
        Zaux.append(Y[i*200+j])
        aux.append(Z[i*200+j])
    curves.append(aux)
    Zvalues.append(Zaux)

fig4=plt.figure()
ax=plt.axes()
ax.plot(Zvalues[0],curves[0],label='Profile '+str(0),c='gold')
plt.show()
for i in range(1,nb_end+1):
    fig4=plt.figure()
    ax=plt.axes()
    for j in range(0,i):
        ax.plot(Zvalues[j],curves[j],c='cornsilk')
    ax.plot(Zvalues[i],curves[i],c='gold')
    plt.show()

print('test')