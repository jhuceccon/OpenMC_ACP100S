#######################################################################
####                                                               ####
####     Biblioteca de Simulação do reator MODELO no OpenMC      ####
####                                                               ####
####            UNIVERSIDADE FEDERAL DO RIO DE JANEIRO             ####
####               Departamento de Engenharia Nuclear              ####
####       LABORATÓRIO DE SIMULAÇÃO E MÉTODOS EM ENGENHARIA        ####
####                                                               ####
####                   Jhulia Schmidt Ceccon                       ####
####                                                               ####
#######################################################################


import openmc
from datetime import datetime
import os

# Criar pasta e mudar para a pasta criada:
def mkdir(nome="teste_sem_nome",data=True,voltar=False):
    if (voltar==True):
        os.chdir("../")
    if (data==True):
        agora = datetime.now()
        nome = agora.strftime(nome+"_%Y%m%d_%H%M%S")
    if not os.path.exists(nome):
        os.makedirs(nome)
    os.chdir(nome)




# Mudar para a pasta
def chdir(nome=None):
    if (nome != None):
        os.chdir(nome)
    else:
        diretorio_atual = os.getcwd()
        diretorios = [diretorio for diretorio in os.listdir(diretorio_atual) if os.path.isdir(os.path.join(diretorio_atual, diretorio))]

        data_mais_recente = 0
        pasta_mais_recente = None

        for diretorio in diretorios:
            data_criacao = os.path.getctime(os.path.join(diretorio_atual, diretorio))
            if data_criacao > data_mais_recente:
                data_mais_recente = data_criacao
                pasta_mais_recente = diretorio

        if pasta_mais_recente:
            os.chdir(os.path.join(diretorio_atual, pasta_mais_recente))
            print("Diretório mais recente encontrado:", pasta_mais_recente)
        else:
            print("Não foi possível encontrar um diretório mais recente.")


simu = True
plotar = True
verbose = True

class modelo:
    def __init__(self):
        self.materiais()
        self.geometria()
        self.configuracoes()




    def materiais(self, enriquecimento = 20):
        print("################################################")
        print("#######     Definição de Materiais        ######")
        print("################################################")
        self.lista_materiais = openmc.Materials()
        self.m_cores = {}

        #agua
        self.m_agua=openmc.Material(name = "Água leve")
        self.m_agua.add_nuclide('H1',2)
        self.m_agua.add_nuclide('O16',1)
        self.m_agua.set_density('g/cm3', 1)
        self.lista_materiais.append(self.m_agua)
        self.m_cores[self.m_agua] = "blue"
        
        #uanio
        self.m_uranio=openmc.Material(name = "uranio 20\\% \enriquecido")
        self.m_uranio.add_element('U',1,enrichment = enriquecimento)
        self.m_uranio.set_density('g/cm3', 18)
        self.lista_materiais.append(self.m_uranio)
        self.m_cores[self.m_uranio] = "yellow"

        self.m_SS304 = openmc.Material(name='Aço INOX', material_id=5)
        self.m_SS304.add_element('C',  4.3000E-04 , percent_type = 'wo')
        self.m_SS304.add_element('Cr', 1.9560E-01 , percent_type = 'wo')
        self.m_SS304.add_element('Ni', 9.6600E-02 , percent_type = 'wo')
        self.m_SS304.add_element('Mo', 8.9000E-03 , percent_type = 'wo')
        self.m_SS304.add_element('Mn', 5.4000E-04 , percent_type = 'wo')
        self.m_SS304.add_element('Si', 5.0000E-04 , percent_type = 'wo')
        self.m_SS304.add_element('Cu', 2.0000E-05 , percent_type = 'wo')
        self.m_SS304.add_element('Co', 3.0000E-05 , percent_type = 'wo')
        self.m_SS304.add_element('P',  2.7000E-04 , percent_type = 'wo')
        self.m_SS304.add_element('S',  1.0000E-04 , percent_type = 'wo')
        self.m_SS304.add_element('N',  1.4000E-04 , percent_type = 'wo')
        self.m_SS304.add_element('Fe', 6.9687E-01 , percent_type = 'wo')
        self.m_SS304.set_density('g/cm3', 7.92)
        self.lista_materiais.append(self.m_SS304)
        self.m_cores[self.m_SS304] = "gray"

        self.m_ar = openmc.Material(name='Ar', material_id=3)
        self.m_ar.add_nuclide('N14' , 7.7826E-01 , percent_type='ao')
        self.m_ar.add_nuclide('N15' , 2.8589E-03 , percent_type='ao')
        self.m_ar.add_nuclide('O16' , 1.0794E-01 , percent_type='ao')
        self.m_ar.add_nuclide('O17' , 1.0156E-01 , percent_type='ao')
        #self.m_ar.add_nuclide('O18' , 3.8829E-05 , percent_type='ao')
        self.m_ar.add_nuclide('Ar36', 2.6789E-03 , percent_type='ao')
        self.m_ar.add_nuclide('Ar38', 3.4177E-03 , percent_type='ao')
        self.m_ar.add_nuclide('Ar40', 3.2467E-03 , percent_type='ao')
        self.m_ar.set_density('g/cm3', 0.001225)
        self.lista_materiais.append(self.m_ar)
        self.m_cores[self.m_ar] = "white"

        # Urânio Enriquecido a 3.1% (FA2, FA3) 
        self.material_uranio_31 = openmc.Material(name="Uranio Enriquecido 3.1%")
        self.material_uranio_31.add_element('U', 1.0, enrichment=3.1)
        self.material_uranio_31.add_element('O', 2.0)
        self.material_uranio_31.set_density('g/cm3', 10.257)
        self.lista_materiais.append(self.material_uranio_31) # ADICIONE ESTA LINHA
        self.m_cores[self.material_uranio_31] = "yellow"

        # Urânio com Veneno Queimável (8% Gd2O3) 
        self.material_gadolina = openmc.Material(name="UO2 + 8% Gd2O3")
        self.material_gadolina.add_element('U', 0.92, enrichment=3.1)
        self.material_gadolina.add_element('Gd', 0.08)
        self.material_gadolina.add_element('O', 2.0)
        self.material_gadolina.set_density('g/cm3', 10.1)
        self.lista_materiais.append(self.material_gadolina) # ADICIONE ESTA LINHA
        self.m_cores[self.material_gadolina] = "green"

        # Zircaloy-4
        self.material_zircaloy = openmc.Material(name="Zircaloy-4")
        self.material_zircaloy.add_element('Zr', 0.98)
        self.material_zircaloy.add_element('Sn', 0.01)
        self.material_zircaloy.set_density('g/cm3', 6.55)
        self.lista_materiais.append(self.material_zircaloy) # ADICIONE ESTA LINHA
        self.m_cores[self.material_zircaloy] = "gray"

        # Urânio Enriquecido a 1.9% (FA1)
        self.material_uranio_19 = openmc.Material(name="Uranio Enriquecido 1.9%")
        self.material_uranio_19.add_element('U', 1.0, enrichment=1.9)
        self.material_uranio_19.add_element('O', 2.0)
        self.material_uranio_19.set_density('g/cm3', 10.257)
        self.lista_materiais.append(self.material_uranio_19)
        self.m_cores[self.material_uranio_19] = "orange" # Cor distinta para o 1.9%



    def geometria(self):
        print("################################################")
        print("#######     Definição de Geometria        ######")
        print("################################################")

        lista_geometria = []

        pallet_altura = 1
        pallet_cilindro = openmc.ZCylinder(r = 0.4095)
        
        pallet_plano_inf = openmc.ZPlane(z0 = -pallet_altura/2, boundary_type= 'reflective')
        pallet_plano_sup = openmc.ZPlane(z0 = pallet_altura/2, boundary_type= 'reflective')

        gap_cilindro = openmc.ZCylinder(r = 0.418)

        clad_cilindro = openmc.ZCylinder(r = 0.475)



        regiao_pallet   =                    -pallet_cilindro & +pallet_plano_inf & -pallet_plano_sup
        regiao_gap      = +pallet_cilindro & -gap_cilindro    & +pallet_plano_inf & -pallet_plano_sup
        regiao_clad     = +gap_cilindro    & -clad_cilindro   & +pallet_plano_inf & -pallet_plano_sup
        regiao_agua_inf = +clad_cilindro                      & +pallet_plano_inf & -pallet_plano_sup
    


        pallet_celula = openmc.Cell(fill = self.m_uranio, region = regiao_pallet)
        gap_celula = openmc.Cell(fill = self.m_ar, region = regiao_gap)
        clad_celula = openmc.Cell(fill = self.m_SS304, region = regiao_clad)
        
        agua_celula = openmc.Cell(fill=self.m_agua, region=regiao_agua_inf)


        universo_agua_inf = openmc.Universe(cells=[openmc.Cell(fill=self.m_agua)])



        ######################################################
        ######################################################
        #############   Universo Agua   ######################
        ######################################################
        ######################################################
        regiao_agua_total = +pallet_plano_inf & -pallet_plano_sup
        agua_celula2 = openmc.Cell(name='Preenchimento com água',
                                fill=self.m_agua,
                                region=regiao_agua_total)
        universo_agua = openmc.Universe(cells=[agua_celula2])
        


        ######################################################
        ######################################################
        #############   Universo RefRad  #####################
        ######################################################
        ######################################################


        regiao_refrad = +pallet_plano_inf & -pallet_plano_sup
        celula_refrad = openmc.Cell(name='Refletor Radial', fill=self.m_agua, region=regiao_refrad)
        universo_RefRad = openmc.Universe(cells=[celula_refrad])


        ######################################################
        ######################################################
        #############   universo_31G08   #####################
        ######################################################
        ######################################################

        celula_combustivel = openmc.Cell(fill=self.material_uranio_31, region= regiao_pallet)
        celula_revestimento = openmc.Cell(fill=self.material_zircaloy, region=regiao_clad)
        self.universo_vareta_31 = openmc.Universe(cells=[celula_combustivel, gap_celula, celula_revestimento, agua_celula])

        celula_gadolina = openmc.Cell(fill=self.material_gadolina, region=regiao_pallet)
        self.universo_vareta_gadolina = openmc.Universe(cells=[celula_gadolina, gap_celula, celula_revestimento,agua_celula])

        cilindro_guia_interno = openmc.ZCylinder(r=0.5715)
        cilindro_guia_externo = openmc.ZCylinder(r=0.612)


        regiao_guia_agua = -cilindro_guia_interno & +pallet_plano_inf & -pallet_plano_sup
        regiao_guia_parede = +cilindro_guia_interno & -cilindro_guia_externo & +pallet_plano_inf & -pallet_plano_sup
        
        celula_guia_agua = openmc.Cell(fill=self.m_agua, region=regiao_guia_agua)
        celula_guia_parede = openmc.Cell(fill=self.material_zircaloy, region=regiao_guia_parede)
        
        self.universo_tubo_guia = openmc.Universe(cells=[celula_guia_agua, celula_guia_parede,agua_celula])


        C = self.universo_vareta_31       # Combustível
        G = self.universo_vareta_gadolina # Gadolina (8 varetas)
        T = self.universo_tubo_guia       # Tubo de Guia
        I = self.universo_tubo_guia       # Instrumentação (mesma dimensão do GT) 

        # Matriz 17x17 baseada na Figura 3b do documento 
        matriz_fa3 = [
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, T, C, C, C, G, C, G, C, C, C, T, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, T, C, C, T, C, C, I, C, C, T, C, C, T, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, T, C, C, C, G, C, G, C, C, C, T, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C]
        ]

        lattice_fa3 = openmc.RectLattice(name='Elemento Combustivel FA3')
        lattice_fa3.pitch = (1.26, 1.26) # Cell Pitch de 1.26 cm 
        lattice_fa3.universes = matriz_fa3
        lattice_fa3.lower_left = [-1.26 * 17 / 2, -1.26 * 17 / 2]
        
        # Preencher o espaço entre as varetas com o seu universo de água
        lattice_fa3.outer = universo_agua_inf

        celula_fa3 = openmc.Cell(name="Celula FA3", fill=lattice_fa3)
        universo_31G08 = openmc.Universe(cells=[celula_fa3])



        ######################################################
        ######################################################
        #############   universo_31000G16  ###################
        ######################################################
        ######################################################


        # Reutilizando as definições de varetas que criamos antes
        C = self.universo_vareta_31       # Combustível 3.1%
        G = self.universo_vareta_gadolina # Gadolina (Agora serão 16 varetas)
        T = self.universo_tubo_guia       # Tubo de Guia
        I = self.universo_tubo_guia       # Instrumentação

        # Matriz 17x17 para o FA4 (Disposição típica com 16 BP)
        matriz_fa4 = [
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, T, G, C, C, G, C, G, C, C, G, T, C, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, T, C, C, T, C, C, I, C, C, T, C, C, T, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, C, T, G, C, C, G, C, G, C, C, G, T, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C]
        ]

        lattice_fa4 = openmc.RectLattice(name='Elemento Combustivel FA4')
        lattice_fa4.pitch = (1.26, 1.26)
        lattice_fa4.universes = matriz_fa4
        lattice_fa4.lower_left = [-1.26 * 17 / 2, -1.26 * 17 / 2]
        lattice_fa4.outer = universo_agua_inf

        celula_fa4 = openmc.Cell(name="Celula FA4", fill=lattice_fa4)
        universo_31000G16 = openmc.Universe(cells=[celula_fa4, agua_celula])


        nucleo_cilindro = openmc.ZCylinder(r = 125, boundary_type= 'vacuum')
        regiao_nucleo   =   -nucleo_cilindro & +pallet_plano_inf & -pallet_plano_sup



        ######################################################
        ######################################################
        #############     universo_19000   ###################
        ######################################################
        ######################################################


        celula_combustivel_19 = openmc.Cell(fill=self.material_uranio_19, region=regiao_pallet)
        universo_vareta_19 = openmc.Universe(cells=[celula_combustivel_19, gap_celula, celula_revestimento, agua_celula])

        # Legendas para a matriz
        M = universo_vareta_19    # Combustível 1.9% (M de matriz)
        T = self.universo_tubo_guia
        I = self.universo_tubo_guia

        # Matriz 17x17 para o FA1 (Sem varetas de Gadolina - Figura 3a)
        matriz_fa1 = [
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, M, M, M, T, M, M, T, M, M, T, M, M, M, M, M],
            [M, M, M, T, M, M, M, M, M, M, M, M, M, T, M, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, T, M, M, T, M, M, T, M, M, T, M, M, T, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, T, M, M, T, M, M, I, M, M, T, M, M, T, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, T, M, M, T, M, M, T, M, M, T, M, M, T, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, M, T, M, M, M, M, M, M, M, M, M, T, M, M, M],
            [M, M, M, M, M, T, M, M, T, M, M, T, M, M, M, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M],
            [M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M, M]
        ]

        lattice_fa1 = openmc.RectLattice(name='Elemento Combustivel FA1')
        lattice_fa1.pitch = (1.26, 1.26)
        lattice_fa1.universes = matriz_fa1
        lattice_fa1.lower_left = [-1.26 * 17 / 2, -1.26 * 17 / 2]
        lattice_fa1.outer = universo_agua_inf

        celula_fa1 = openmc.Cell(name="Celula FA1", fill=lattice_fa1)
        universo_19000 = openmc.Universe(cells=[celula_fa1, agua_celula])



        ######################################################
        ######################################################
        #############     universo_31G16   ###################
        ######################################################
        ######################################################

        C = self.universo_vareta_31       # Combustível 3.1%
        G = self.universo_vareta_gadolina # Gadolina (16 varetas)
        T = self.universo_tubo_guia       # Tubo de Guia
        I = self.universo_tubo_guia       # Instrumentação

        # Matriz 17x17 para o FA2 (16 varetas BP - Figura 3c)
        matriz_fa2 = [
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, T, G, C, C, G, C, G, C, C, G, T, C, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, T, C, C, T, C, C, I, C, C, T, C, C, T, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, C, T, G, C, C, G, C, G, C, C, G, T, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C]
        ]

        lattice_fa2 = openmc.RectLattice(name='Elemento Combustivel FA2')
        lattice_fa2.pitch = (1.26, 1.26)
        lattice_fa2.universes = matriz_fa2
        lattice_fa2.lower_left = [-1.26 * 17 / 2, -1.26 * 17 / 2]
        lattice_fa2.outer = universo_agua_inf

        celula_fa2 = openmc.Cell(name="Celula FA2", fill=lattice_fa2)
        universo_31G16 = openmc.Universe(cells=[celula_fa2,agua_celula])



        ######################################################
        ######################################################
        #############   universo_31000G08   ##################
        ######################################################
        ######################################################


        C = self.universo_vareta_31       # Combustível 3.1%
        G = self.universo_vareta_gadolina # Gadolina (8 varetas)
        T = self.universo_tubo_guia       # Tubo de Guia
        I = self.universo_tubo_guia       # Instrumentação

        # Matriz 17x17 para o FA5 (8 varetas BP - conforme Figura 3b)
        matriz_fa5 = [
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, T, C, C, C, G, C, G, C, C, C, T, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, T, C, C, T, C, C, I, C, C, T, C, C, T, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, T, C, C, C, G, C, G, C, C, C, T, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C]
        ]

        lattice_fa5 = openmc.RectLattice(name='Elemento Combustivel FA5')
        lattice_fa5.pitch = (1.26, 1.26)
        lattice_fa5.universes = matriz_fa5
        lattice_fa5.lower_left = [-1.26 * 17 / 2, -1.26 * 17 / 2]
        lattice_fa5.outer = universo_agua_inf

        celula_fa5 = openmc.Cell(name="Celula FA5", fill=lattice_fa5)
        universo_31000G08 = openmc.Universe(cells=[celula_fa5, ])



        ######################################################
        ######################################################
        #############    universo nucleo     #################
        ######################################################
        ######################################################


        A = universo_agua
        R = universo_RefRad
        V = universo_31G08
        C = universo_31000G16
        M = universo_19000
        Y = universo_31G16
        T = universo_31000G08

        matriz_nucleo = [
            [A,A,A,R,R,R,R,R,A,A,A],
            [A,A,R,R,V,V,V,R,R,A,A],
            [A,R,R,C,V,Y,V,C,R,R,A],
            [R,R,C,M,Y,C,Y,M,C,R,R],
            [R,V,V,Y,M,M,M,Y,V,V,R],
            [R,V,Y,C,M,T,M,C,Y,V,R],
            [R,V,V,Y,M,M,M,Y,V,V,R],
            [R,R,C,M,Y,C,Y,M,C,R,R],
            [A,R,R,C,V,Y,V,C,R,R,A],
            [A,A,R,R,V,V,V,R,R,A,A],
            [A,A,A,R,R,R,R,R,A,A,A]

        ]

        lattice_nucleo = openmc.RectLattice()
        lattice_nucleo.pitch = (21.42,21.42)
        lattice_nucleo.universes = matriz_nucleo
        lattice_nucleo.lower_left = (- (len(lattice_nucleo.universes[0]) * lattice_nucleo.pitch[0]) / 2.0,     - (len(lattice_nucleo.universes) * lattice_nucleo.pitch[1]) / 2.0)
        lattice_nucleo.outer = universo_agua_inf

        celula_nucleo = openmc.Cell(fill=lattice_nucleo, region=regiao_nucleo)
        universo_nucleo = openmc.Universe(cells=[celula_nucleo])

        #lista_geometria.append(universo_elemento_comb)
        self.lista_geometria = openmc.Geometry()
        self.lista_geometria.root_universe = universo_nucleo
        




    def contagens(self):
        print("################################################")
        print("#######     Definição de Contagens        ######")
        print("################################################")





    def plotar(
            self,
            filename = 'plot.png',
            basis  = 'xy',
            width  = (200, 200),
            pixels = (800, 800),
            origin = None,
            rotacionar = False
            ):
        print("################################################")
        print("###########        Plotagem         ############")
        print("################################################")
        if plotar:
            plot = openmc.Plot()
            plot.filename = filename
            plot.basis = basis
            plot.width = width
            plot.pixels = pixels
            if origin is not None:
                plot.origin = origin
            plot.color_by = 'material'
            plot.colors = self.m_cores
            plots = openmc.Plots([plot])

            self.lista_materiais.export_to_xml()
            self.lista_geometria.export_to_xml()
            plots.export_to_xml()
            openmc.plot_geometry()
            
            #if rotacionar:
                # Rotaciona 90 graus no sentido anti-horário | expand=True: ajusta o tamanho da imagem se não for quadrada
                #Image.open(filename).rotate(90, expand=True).save(filename)



    def configuracoes(
        self,
        particulas = 1000,
        ciclos = 100,
        inativos = 10
    ):
        print("################################################")
        print("####     Definição de Configurações       ######")
        print("################################################")
        self.settings = openmc.Settings()
        self.settings.particles = particulas
        self.settings.batches = ciclos
        self.settings.inactive = inativos
        self.settings.source = openmc.IndependentSource(space=openmc.stats.Point())
        self.settings.output = {'tallies': False}
        

    def simular(self):
        print("################################################")
        print("###########        Executando       ############")
        print("################################################")
        if simu:
            self.lista_materiais.export_to_xml()
            self.lista_geometria.export_to_xml()
            self.settings.export_to_xml()
            openmc.run()