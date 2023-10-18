#Bibliotecas necessárias
import configparser
import h5py
import numpy as np
import pynbody
import pynbody.plot.sph as sph
import matplotlib.pyplot as plt
from sys import argv
from astropy.cosmology import FlatLambdaCDM
cosmo = FlatLambdaCDM(H0=70, Om0=0.3)

'''
galmock.py

This python program adapts hdf5 snapshots from IllustrisTNG galaxies creating the plot of realistic visualizations, that take into account metallicity and age of particles in the simulated subhalo.

Usage:
python3 TNGmockFITS.py [snapshot.hdf5] [param.ini]
'''

########################################################################
# cria o objeto ConfigParser
config = configparser.ConfigParser()

# lê o arquivo .ini
config.read('param.ini')

# obtém os valores da seção "plot"
width = config.get('plot', 'width')
resolution = config.getint('plot', 'resolution')
starsize = config.getfloat('plot', 'starsize')
galrot = config.getint('plot', 'galrot')

# obtém os valores da seção "filters"
r_scale = config.getfloat('filters', 'r_scale')
g_scale = config.getfloat('filters', 'g_scale')
b_scale = config.getfloat('filters', 'b_scale')
dynamic_range = config.getfloat('filters', 'dynamic_range')
                                
########################################################################

# Define ordem do argumento ao iniciar o programa, no caso o argumento é o nome do seu snapshot a ser lido
snapshotIn = str(argv[1])

#Atribuindo o  do argumento 1 para o título do snapshot escolhido para ser lido pelo h5py
s = h5py.File(snapshotIn, "r")

#lendo as partículas tipo stars do arquivo hdf5
s_star = s['PartType4']


#importando tempo do snapshot
s_redshift = s['Header'].attrs['Redshift'] #coleta o tempo do Header do snapshot
s_time = cosmo.age(s_redshift)

#importando informações das partículas tipo stars
star_x = np.array(s_star['Coordinates'][:,0])
star_y = np.array(s_star['Coordinates'][:,1])
star_z = np.array(s_star['Coordinates'][:,2])
star_mass = np.array(s_star['Masses'])
star_metal = np.array(s_star['GFM_Metallicity'])

star_time_sf = np.array(s_star['GFM_StellarFormationTime'])
star_redshift = ((1/(star_time_sf))-1)
star_age = cosmo.age(star_redshift)

    

x = star_x
y = star_y
z = star_z
mass = star_mass
metal = star_metal
age = star_age


#correção de centro de massa do snapshot
#com_x = np.sum(x*mass)/np.sum(mass)
#com_y = np.sum(y*mass)/np.sum(mass)
#com_z = np.sum(z*mass)/np.sum(mass)

#x = (x - com_x)
#y = (y - com_y)
#z = (z - com_z)


#atribuindo Sim.Arrays para o pynobdy
Nstars = len(mass)
p = pynbody.snapshot.new(star=int(Nstars))
p.star['pos'] = pynbody.array.SimArray(np.empty((Nstars, 3)), units="kpc")
p.star['mass'] = pynbody.array.SimArray(np.empty((Nstars)), units="1.00e+10 Msol")
p.star['metals'] = pynbody.array.SimArray(np.empty((Nstars)), units=None)
p.star['age'] = pynbody.array.SimArray(np.empty((Nstars)), units="Gyr")

p.star['pos'][:,0] = x
p.star['pos'][:,1] = y
p.star['pos'][:,2] = z
p.star['mass'] = mass
p.star['metals'] = metal
p.star['age'] = s_time - age #tempo do nascimento das partículas stars para formato esperado pela função do pynbody
p.stars.rotate_x(galrot)

#plotagem
pynbody.plot.stars.render(p, width=width, resolution=resolution, starsize=starsize, r_scale=r_scale, g_scale=g_scale, b_scale=b_scale, dynamic_range=dynamic_range, plot=True)

s_time = s_time.value
#salvando arquivo com a imagem gerada e dando nome de acordo com o tempo do snapshot
plt.savefig('mock_'+str("%.2f"%s_time)+'Gyr.png', bbox_inches='tight', facecolor='white', dpi=300)
