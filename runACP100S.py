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

# Índices: [FA_19000, FA_31G16, 31G08, 31000G16, 31000G08]
alturas_barras = [-118.5, 118.5, -100, 100, 75]
reator.geometria(plotar_interno=interno, alturaBarra=alturas_barras)

# Configurações de transporte de partículas
reator.configuracoes(particulas=1000)


#################################################################################
#####################       Definição do Grid de Energia      ###################
#################################################################################

# Definição do grid: de 0.001 eV (10^-3) até 10 MeV (10^7)
# 1024 intervalos para uma resolução fina no espectro
intervalos_energias = np.logspace(-3, 7, 1024)


#################################################################################
#####################     Configuração de Tallies (Física)    ###################
#################################################################################

# Inicializa a lista de tallies
reator.contagens(init=True)

# 1. Espectro no Combustível (Material Uranio 19)
reator.contagem_espectro_por_material(
    universo_macro = reator.elemento19000_lattice_universo, 
    material_alvo  = reator.m_uranio19, 
    energia        = intervalos_energias,
    nome           = "espectroFluxoCombustivel"
)

# 2. Espectro na Água (Moderador)
reator.contagem_espectro_por_material(
    universo_macro = reator.elemento19000_lattice_universo, 
    material_alvo  = reator.m_agua, 
    energia        = intervalos_energias,
    nome           = "espectroAguaEntreVaretas"
)

# Finaliza e exporta para tallies.xml
reator.contagens(export=True)


#################################################################################
#####################        Execução da Simulação            ###################
#################################################################################

reator.plotar(filename="reator_completo", width=(300,300), pixels=(800,800))
reator.simular()


#################################################################################
#####################     Extração de Dados Pós-Simulação     ###################
#################################################################################

if libACP100S.simu:
    print("\nExtraindo resultados dos arquivos de saída...")
    
    # Extração dos valores de fluxo e erro para o Combustível
    fluxo_comb, erro_comb = reator.contagem_espectro_por_material(
        universo_macro = reator.universo_nucleo,  
        material_alvo  = reator.m_uranio19,             
        get=True, 
        nome="espectroFluxoCombustivel"
    )
    
    # Extração dos valores de fluxo e erro para a Água
    fluxo_agua, erro_agua = reator.contagem_espectro_por_material(
        universo_macro = reator.universo_nucleo,  
        material_alvo  = reator.m_agua,            
        get=True, 
        nome="espectroAguaEntreVaretas"
    )

    # Exibindo os primeiros valores para conferência rápida no terminal
    print(f"\n✅ Extração realizada com sucesso!")
    print(f"Total de pontos de energia: {len(fluxo_comb)}")
    print(f"Primeiros valores de fluxo (Combustível): {fluxo_comb[:3]}")
    print(f"Primeiros valores de fluxo (Água):        {fluxo_agua[:3]}")
    print("="*50)




#################################################################################
#####################       Geração de Gráfico (Visualização)  ###################
#################################################################################

import matplotlib.pyplot as plt

if libACP100S.simu:
    plt.figure(figsize=(10, 6))
    
    # Plotando os dados
    # Usamos intervalos_energias[:-1] porque o fluxo é calculado entre os intervalos
    plt.step(intervalos_energias[:-1], fluxo_comb, where='post', label='Fluxo no Combustível')
    plt.step(intervalos_energias[:-1], fluxo_agua, where='post', label='Fluxo na Água')
    
    # Configurações de escala e labels
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Energia [eV]')
    plt.ylabel('Fluxo [n/cm².s]')
    plt.title('Espectro de Energia Neutrônica - ACP100S')
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.legend()
    
    # Salva o gráfico
    plt.savefig("espectro_energia.png", dpi=300)
    print("✅ Gráfico 'espectro_energia.png' gerado com sucesso!")
    plt.show()



#################################################################################
#####################      Exportação para Arquivo EXCEL      ###################
#################################################################################

import pandas as pd

if libACP100S.simu:
    print("\nGerando planilha Excel...")
    
    # Criando o dicionário com os dados extraídos
    # Nota: usamos intervalos_energias[:-1] para alinhar com o tamanho dos fluxos
    dados = {
        'Energia [eV]': intervalos_energias[:-1],
        'Fluxo (Combustível)': fluxo_comb,
        'Erro Relativo (Comb.)': erro_comb,
        'Fluxo (Água)': fluxo_agua,
        'Erro Relativo (Água)': erro_agua
    }
    
    # Criando o DataFrame (Tabela)
    df = pd.DataFrame(dados)
    
    # Exportando para Excel (.xlsx)
    nome_arquivo = "resultados_simulacao_ACP100S.xlsx"
    df.to_excel(nome_arquivo, index=False, engine='openpyxl')
    
    print(f"✅ Dados exportados com sucesso para: {nome_arquivo}")
