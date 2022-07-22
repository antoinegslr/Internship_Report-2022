from mpl_toolkits import mplot3d
from math import *
import numpy as np
#import matplotlib
import matplotlib.pyplot as plt
#matplotlib.use("pgf")
#matplotlib.rcParams.update({
#    "pgf.texsystem": "pdflatex",
#    'font.family': 'serif',
#    'text.usetex': True,
#    'pgf.rcfonts': False,
#})

chemin='C://Users//antoi//Downloads/new_pspc.gro'
fichier=open(chemin,'r')
listeBrute=fichier.readlines()
fichier.close()

def traduction(ligne,totatom):
    #Structure du gro : Nom du résidu, Nom de l'atome, Numéro de l'atome, x,y,z, inutile
    res=[]
    for ele in ligne.split(' '):
        if ele=='': continue
        if '\n' in ele:
            res.append(ele[:-1])
            continue
        res.append(ele)
    if len(res[1])>4:
        return [res[0],res[1][:-len(totatom)],res[1][-len(totatom):len(res[1])]]+res[2:]
    else:
        return res

def phosphore(liste):
    res=[]
    for ligne in liste:
        if ligne[2]=='P':
            res.append(ligne)
    return res

def analyseGRO(listeB):
    listeT=[]
    listeP=[]
    for ligne in listeB[2:-1]:
        listeT.append(traduction(ligne,listeBrute[1][:-1]))
    for ligne in listeT:
        if ligne[1]=='P':
            listeP.append([float(ligne[3]),float(ligne[4]),float(ligne[5])])
    return listeP

def analyseGROprot(listeB):
    listeT=[]
    listeprot=[]
    for ligne in listeB[2:-1]:
        listeT.append(traduction(ligne,listeBrute[1][:-1]))
    for ligne in listeT:
        if 'LYS' in ligne[0] or 'CYS' in ligne[0] or 'LEU' in ligne[0] or 'PRO' in ligne[0] or 'TYR' in ligne[0] or 'ARG' in ligne[0]:
            listeprot.append([float(ligne[3]),float(ligne[4]),float(ligne[5])])
    return listeprot

def xyz(listeCoord):
    resx,resy,resz=[],[],[]
    for x in listeCoord:
        resx.append(x[0])
        resy.append(x[1])
        resz.append(x[2])
    return resx,resy,resz

def splitin2(listeCoord):
    upper,lower=[],[]
    for item in listeCoord:
        if item[2]>4.5:
            upper.append(item)
            continue
        lower.append(item)
    return upper,lower


#Hopla on code maintenant
CoordP=analyseGRO(listeBrute)
upper,lower=splitin2(CoordP)
X,Y,Z=xyz(upper)

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');
#ax.scatter(X, Y, Z, c=Z, cmap='viridis', linewidth=0.5);
ax.plot_trisurf(X, Y, Z, cmap='plasma', edgecolor='none');
X,Y,Z=xyz(lower)
ax.plot_trisurf(X, Y, Z, cmap='plasma_r', edgecolor='none');
#ax.scatter(X, Y, Z, c=Z, cmap='viridis', linewidth=0.5);

#plt.savefig('C://Users//antoi//Documents//Python//Surface Membrane Drawer/histogram.pgf')
#On veut maintenant afficher avec des boules tout sauf POPS, TIP3, SOD, CLA...
coordprot=analyseGROprot(listeBrute)
X,Y,Z=xyz(coordprot)
#ax.scatter(X,Y,Z,color='orange',linewidth=0.001)
plt.show()

##Déterminons l'épaisseur en ne comptant que les atomes P autour du peptide
def distance(xyz,dist):
    return sqrt((xyz[0]-dist)**2+(xyz[1]-dist)**2)

PinPep=[]
for atome in CoordP:
    if atome[2]>4:
        if distance(atome,3.13)<=1.5:
            PinPep.append(atome)
    else:
        if distance(atome,3.5)<=1.5:
            PinPep.append(atome)

upPep,downPep=splitin2(PinPep)
meanUp,meanDown=0.0,0.0
ite=0
for el in upPep:
    meanUp+=el[2]
    ite+=1
meanUp/=ite
ite=0
for el in downPep:
    meanDown+=el[2]
    ite+=1
meanDown/=ite



fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');
coordOrange=[]
for el in CoordP:
    if el not in PinPep:
        coordOrange.append(el)
X,Y,Z=xyz(coordOrange)
ax.scatter(X,Y,Z,color='orange',linewidth=0.001)
#ax.scatter(X, Y, Z, c=Z, cmap='viridis', linewidth=0.5);
X,Y,Z=xyz(upPep)
ax.scatter(X,Y,Z,color='black',linewidth=0.001)
X,Y,Z=xyz(downPep)
ax.scatter(X,Y,Z,color='black',linewidth=0.001)
#ax.scatter(X, Y, Z, c=Z, cmap='viridis', linewidth=0.5);
coordprot=analyseGROprot(listeBrute)
X,Y,Z=xyz(coordprot)
ax.scatter(X,Y,Z,color='blue',linewidth=0.001)
plt.show()

print(meanUp-meanDown)

##wtf
def f(x, y):
    return np.sin(np.sqrt(x ** 2 + y ** 2))

x = np.linspace(-6, 6, 30)
y = np.linspace(-6, 6, 30)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)
fig = plt.figure()
ax = plt.axes(projection='3d')
ax.contour3D(X, Y, Z, 50, cmap='binary')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z');