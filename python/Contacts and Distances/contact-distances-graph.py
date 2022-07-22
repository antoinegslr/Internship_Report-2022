import matplotlib.pyplot as plt
from math import floor,ceil

#Files have to be named in this form: type_id_residue.xvg
#----- INPUT PARAMETERS -----

#Always put 0 and the last prod file
files=[i for i in range(0,77)]
#files=[0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,76]
#Position of prod_0
start=3.8
#Position of prod_76
end=-3.8
#Path for the files
path='C://Users//antoi//OneDrive - Université Paris Sciences et Lettres//Stage//Figures/contact_dist/'

#----- END OF INPUT PARAMETERS -----

#----- FUNCTIONS -----
def nb2coord(x):
    return round(start-(x*(start-end))/files[-1],1)

def readxvg(type,id,residue):
    newpath=path+type+'_'+str(id)+'_'+residue+'.xvg'
    fichier=open(newpath,'r')
    brut=fichier.readlines()
    fichier.close()
    #Each line is stored in a str
    final=[]
    for line in brut[24:]:
        aux=[]
        for item in line[:-1].split(' '):
            if item!='': aux.append(float(item))
        final.append(aux)
    return final

def plotlist(list,title='',axex='',axey=''):
    #Contains only x and y
    fig=plt.figure()
    ax=plt.axes()
    ax.set_xlabel(axex)
    ax.set_ylabel(axey)
    plt.title(title)
    X,Y=[],[]
    for item in list:
        X.append(item[0])
        Y.append(item[1])
    ax.plot(X,Y)
    fig.show()

def mean(list):
    #Contains time and value to mean
    aux=0
    ite=0
    for item in list:
        ite+=1
        aux+=item[1]
    return aux/ite

def mean_time(list,begin,end):
    #Contains time and value to mean
    aux=0
    ite=0
    for item in list:
        if item[0]>begin and item[0]<end:
            ite+=1
            aux+=item[1]
    return aux/ite

def histolist(list,title='',axex='',axey=''):
    #List containing positions and average value of contact
    Hist=[]
    for item in list:
        for ite in range(0,ceil(item[1])):
            Hist.append(item[0])
    fig=plt.figure()
    ax=plt.axes()
    ax.set_xlabel(axex)
    ax.set_ylabel(axey)
    plt.style.use('ggplot')
    plt.hist(Hist, bins=len(files))
    plt.title(title)
    plt.show()

#----- END OF FUNCTIONS -----

#----- FREESTYLE AREA -----
contact_water,contact_pops,dist_prot,dist_pops,contact_carb,dist_carb,contact_carb2,dist_carb2=[],[],[],[],[],[],[],[]
contact_water_time=[]
#Let's start with water
for id in files:
    contact_water.append([nb2coord(id),mean(readxvg('contact',id,'water'))])
    #contact_water_time.append([nb2coord(id),mean_time(readxvg('contact',id,'water'),0,50000)])
histolist(contact_water,'Number of contacts between Calcium and Water','Reaction coordinate','Contacts with water')
#histolist(contact_water_time,'Contacts with water, t<50 ns','Reaction coordinate','Contacts with water')
#Then let's do distance with protein
for id in files:
    dist_prot.append([nb2coord(id),mean(readxvg('dist',id,'prot'))])
plotlist(dist_prot,'Distance with PROT as a function of penetration of bilayer','Reaction coordinate','Distance (nm)')
#Then let's do distance and contact with phosphates
for id in files:
    dist_pops.append([nb2coord(id),mean(readxvg('dist',id,'phosphate'))])
    contact_pops.append([nb2coord(id),mean(readxvg('contact',id,'phosphate'))])
plotlist(dist_pops,'Distance with phosphate atoms as a function of penetration of bilayer','Reaction coordinate','Distance (nm)')
histolist(contact_pops,'Contacts with phopshate atoms','Reaction coordinate','Contacts with lipids')
#And with carboxyl groups
for id in files:
    dist_carb.append([nb2coord(id),mean(readxvg('dist',id,'carboxyl'))])
    contact_carb.append([nb2coord(id),mean(readxvg('contact',id,'carboxyl'))])
    dist_carb2.append([nb2coord(id),mean(readxvg('dist',id,'carboxyl2'))])
    contact_carb2.append([nb2coord(id),mean(readxvg('contact',id,'carboxyl2'))])
plotlist(dist_carb,'Distance with carboxyl group as a function of penetration of bilayer','Reaction coordinate','Distance (nm)')
histolist(contact_carb,'Contacts with carboxyl group','Reaction coordinate','Contacts with carboxyl')
plotlist(dist_carb2,'Distance with carboxyl group2 as a function of penetration of bilayer','Reaction coordinate','Distance (nm)')
histolist(contact_carb2,'Contacts with carboxyl group2','Reaction coordinate','Contacts with carboxyl')
#----- END OF FREESTYLE -----

##MEGA FREESTYLE TIME
for i in range(0,77):
    plotlist(readxvg('dist',i,'phosphate'),'Calcium at z='+str(nb2coord(i))[0:5],'Time (ps)','Calcium-P distance (nm)')