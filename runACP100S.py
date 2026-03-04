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

libACP100S.mkdir(nome=f"resultados", data=False) 

reator = libACP100S.modelo()
reator.geometria(plotar_interno=True, alturaBarra=2)
reator.configuracoes(particulas=1000)
reator.plotar(filename="reator_completo", width=(250,250),pixels=(10000,10000))
#reator.plotar(filename="zoom1", width=(25,25),pixels=(5000,5000))
reator.simular()