#######################################################################
####                                                               ####
####        Casos de Simulação do reator MODELO no OpenMC          ####
####                                                               ####
####            UNIVERSIDADE FEDERAL DO RIO DE JANEIRO             ####
####               Departamento de Engenharia Nuclear              ####
####       LABORATÓRIO DE SIMULAÇÃO E MÉTODOS EM ENGENHARIA        ####
####                                                               ####
####                   Jhulia Schmidt Ceccon                       ####
####                                                               ####
#######################################################################

import os
os.system("clear")

import libACP100S

libACP100S.simu = False
libACP100S.plotar = True
libACP100S.verbose = True

ini=3
fin=4
passo=1
for enr in range(ini,fin,passo):
    libACP100S.mkdir(nome=f"resultados_UO2_enriquecimento_{enr}", data=True, voltar=False if enr == ini else True) 
    reator = libACP100S.modelo()
    reator.materiais(enriquecimento=enr/100)
    reator.geometria()
    reator.configuracoes(particulas=1000)
    reator.plotar(width=(100,100),pixels=(1000,1000))
    reator.simular()
