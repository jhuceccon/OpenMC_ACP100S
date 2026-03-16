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
import numpy as np
import libACP100S

#################################################################################
######################### Configurações Iniciais e Pastas #######################
#################################################################################

os.system("clear")
libACP100S.mkdir(nome="resultados", data=False)

libACP100S.simu    = True   
libACP100S.plotar  = True   
libACP100S.verbose = True   
interno            = False

reator = libACP100S.modelo()


#################################################################################
##################### Geometria e Posicionamento das Barras #####################
#################################################################################

PALLET_ALTURA   = 245     # cm  — altura ativa do combustível (pellets)
# Índices: [FA_19000, FA_31G16, 31G08, 31000G16, 31000G08]
alturas_barras = [PALLET_ALTURA, PALLET_ALTURA, PALLET_ALTURA, PALLET_ALTURA, PALLET_ALTURA]
reator.geometria(plotar_interno=interno, alturaBarra=alturas_barras)

# Configurações de transporte de partículas
N_PARTICULAS, N_CICLOS, N_INATIVOS, N_BINS_Z = 100, 50, 5, 20
reator.configuracoes(particulas=N_PARTICULAS, ciclos=N_CICLOS, inativos=N_INATIVOS)


#################################################################################
#####################       Definição do Grid de Energia      ###################
#################################################################################

# Definição do grid: de 0.001 eV (10^-3) até 10 MeV (10^7)
# 1024 intervalos para uma resolução fina no espectro
intervalos_energias = np.logspace(-3, 7, 1024)


#################################################################################
#####################     Configuração de Tallies (Física)    ###################
#################################################################################

reator.contagens(init=True)

# 1. Chama a função original (que vai criar a malha com erro de tamanho)
reator.configurar_tallies_3d(n_bins_z=N_BINS_Z)

# 2. CORREÇÃO MANUAL: Forçamos os limites para os 9 elementos (aprox. 97cm)
# Acessamos o objeto da malha dentro do reator e alteramos os cantos
L_NUCLEO = 97.0
reator._mesh_ref.lower_left  = [-L_NUCLEO, -L_NUCLEO, -107.5]
reator._mesh_ref.upper_right = [ L_NUCLEO,  L_NUCLEO,  107.5]

reator.contagens(export=True)


#################################################################################
#####################        Execução da Simulação            ###################
#################################################################################

reator.plotar(filename="reator_completo", width=(300,300), pixels=(800,800))
reator.simular()



#################################################################################
#####################     Extração e Processamento de Dados     #################
#################################################################################

POTENCIA_NOMINAL = 350e6    # 350 MWt
Z_INF, Z_SUP     = -107.5, 107.5
ALTURA_ATIVA_CM  = Z_SUP - Z_INF 

if libACP100S.simu:
    print("\nExtraindo e normalizando dados para 350 MWt...")
    
    # Extração das matrizes normalizadas e coordenadas
    fluxo, potencia_watts, coords = reator.extrair_dados_normalizados(potencia_ref=POTENCIA_NOMINAL)

    # Cálculo da Potência Linear (W/cm)
    dz_cm = ALTURA_ATIVA_CM / N_BINS_Z
    potencia_w_cm = potencia_watts / dz_cm

    # Ajuste para o Visualizador PyQt5 (Compensação do fator 0.1 da interface)
    # Salvamos (W/cm ) para que a leitura final resulte em kW/m
    potencia_para_visualizador = potencia_w_cm 




#################################################################################
#####################    Salvamento das Matrizes (NPY)      ###################
#################################################################################

    print("Salvando matrizes tridimensionais em /Dados...")

    # --- ADICIONE ESTAS DUAS LINHAS AQUI ---
    os.makedirs("Dados", exist_ok=True) 
    # (O exist_ok=True garante que ele não dê erro se a pasta já existir nas próximas vezes)

    # Salvamento dos dados principais
    np.save("Dados/Fluxo_ncm2s_3D.npy", fluxo)
    np.save("Dados/Potencia_W_cm_3D.npy", potencia_para_visualizador)

    # Salvamento dos eixos de referência
    np.save("Dados/Eixo_X_cm.npy", coords['x'])
    np.save("Dados/Eixo_Y_cm.npy", coords['y'])
    np.save("Dados/Eixo_Z_cm.npy", coords['z'])