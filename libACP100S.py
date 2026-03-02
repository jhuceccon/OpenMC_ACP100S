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
import openmc.model
from datetime import datetime
import os

# Criar pasta e mudar para a pasta criada:
def mkdir(nome="teste_sem_nome",data=True,voltar=False,chdir=True):
    if (voltar==True):
        os.chdir("../")
    if (data==True):
        agora = datetime.now()
        nome = agora.strftime(nome+"_%Y%m%d_%H%M%S")
    if not os.path.exists(nome):
        os.makedirs(nome)
    if chdir:
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




    def materiais(self):
        print("################################################")
        print("#######     Definição de Materiais        ######")
        print("################################################")
        self.lista_materiais = openmc.Materials()
        self.m_cores = {}

        # Água
        self.m_agua=openmc.Material(name = "Água leve")
        self.m_agua.add_nuclide('H1',2)
        self.m_agua.add_nuclide('O16',1)
        self.m_agua.set_density('g/cm3', 1)
        self.lista_materiais.append(self.m_agua)
        self.m_cores[self.m_agua] = "blue"

        # Gás Hélio
        self.m_helio = openmc.Material(name='Gás Hélio')
        self.m_helio.add_element('He', 1.0, percent_type='ao')
        self.m_helio.set_density('g/cm3', 0.0001786) #Densidade do gás Hélio a 1 atm e 0°C
        self.lista_materiais.append(self.m_helio)
        self.m_cores[self.m_helio] = "lightpink"

        # Ar
        self.m_ar = openmc.Material(name='Ar', )
        self.m_ar.add_nuclide('N14' , 7.7826E-01 , percent_type='ao')
        self.m_ar.add_nuclide('N15' , 2.8589E-03 , percent_type='ao')
        self.m_ar.add_nuclide('O16' , 1.0794E-01 , percent_type='ao')
        self.m_ar.add_nuclide('O17' , 1.0156E-01 , percent_type='ao')
        #self.m_ar.add_nuclide('O18' , 3.8829E-05 , percent_type='ao') #Comentado pois ENDF 7.1 não possui essa tabela de seção de choque
        self.m_ar.add_nuclide('Ar36', 2.6789E-03 , percent_type='ao')
        self.m_ar.add_nuclide('Ar38', 3.4177E-03 , percent_type='ao')
        self.m_ar.add_nuclide('Ar40', 3.2467E-03 , percent_type='ao')
        self.m_ar.set_density('g/cm3', 0.001225)
        self.lista_materiais.append(self.m_ar)
        self.m_cores[self.m_ar] = "white"

        # Zircaloy-4
        self.m_zircaloy = openmc.Material(name="Zircaloy-4")
        self.m_zircaloy.add_element('Zr', 0.98185, percent_type='wo')
        self.m_zircaloy.add_element('Sn', 0.01500, percent_type='wo')
        self.m_zircaloy.add_element('Fe', 0.00200, percent_type='wo')
        self.m_zircaloy.add_element('Cr', 0.00100, percent_type='wo')
        self.m_zircaloy.add_element('O',  0.00015, percent_type='wo')
        self.m_zircaloy.set_density('g/cm3', 6.55)
        self.lista_materiais.append(self.m_zircaloy)
        self.m_cores[self.m_zircaloy] = "gray"

        # Urânio Enriquecido a 1.9% (FA1)
        self.m_uranio19 = openmc.Material(name="Uranio Enriquecido 1.9%")
        self.m_uranio19.add_element('U', 1.0, enrichment=1.9)
        self.m_uranio19.add_element('O', 2.0)
        self.m_uranio19.set_density('g/cm3', 10.257)
        self.lista_materiais.append(self.m_uranio19)
        self.m_cores[self.m_uranio19] = "orange"

        # Urânio Enriquecido a 3.1% (FA2, FA3) 
        self.m_uranio31 = openmc.Material(name="Uranio Enriquecido 3.1%")
        self.m_uranio31.add_element('U', 1.0, enrichment=3.1)
        self.m_uranio31.add_element('O', 2.0)
        self.m_uranio31.set_density('g/cm3', 10.257)
        self.lista_materiais.append(self.m_uranio31)
        self.m_cores[self.m_uranio31] = "yellow"

        # Urânio Enriquecido a 3.1% com Veneno Queimável (8% Gd2O3) 
        self.m_uranio31_gadolina = openmc.Material(name="Uranio Enriquecido 3.1% + 8% Gd2O3")
        self.m_uranio31_gadolina.add_element('U', 0.92, enrichment=3.1)
        self.m_uranio31_gadolina.add_element('Gd', 0.08)
        self.m_uranio31_gadolina.add_element('O', 2.0)
        self.m_uranio31_gadolina.set_density('g/cm3', 10.1)
        self.lista_materiais.append(self.m_uranio31_gadolina)
        self.m_cores[self.m_uranio31_gadolina] = "green"







    def geometria(self, alturaBarra = 0, plotar_interno=False):
        print("################################################")
        print("#######     Definição de Geometria        ######")
        print("################################################")

        # Estratégia de desenho:
        ## Superfícies e regiões podem ser reaproveitadas em mais de uma célula
        ## Entretanto cada célula só pode estar dentro de um universo
        ## Para não ter que digitar o código de criação de duas células iguais, a célula pode ser clonada.
        ## Universos podem ser reaproveitados em mais de um lattice


        ######################################################
        ######################################################
        ####  Definições gerais de uma vareta combustível ####
        ######################################################
        ######################################################

        pitch_varetas = 1.26

        # Definições do pallet combustível (iguais para todas varetas e elementos combustíveis)
        pallet_altura    = 1
        pallet_raio      = 0.4095
        pallet_cilindro  = openmc.ZCylinder(r = pallet_raio)
        pallet_planoInf = openmc.ZPlane(z0 = -pallet_altura/2, boundary_type= 'reflective') #Temporariamente reflexivo, até desenhar o reator em 3D (desenhar a parte superior e inferior)
        pallet_planoSup = openmc.ZPlane(z0 =  pallet_altura/2, boundary_type= 'reflective')
        pallet_regiao    =                   -pallet_cilindro & +pallet_planoInf & -pallet_planoSup
        # pallet_celula: cada célula do pallet será definida com um material diferente
        

        # Definições do gap ao redor do pallet combustível (iguais para todas varetas e elementos combustíveis)
        gapRadial_raio      = 0.418
        gapRadial_cilindro  = openmc.ZCylinder(r = gapRadial_raio)
        # O gap axial fica 100% na parte superior (a naõ ser que tenha mola em baixo)
        #gapSuperior_raio
        #gapSuperior_planoSup
        #gapSuperior_planoInf
        #gapSuperior_regiao
        gapRadial_regiao    = +pallet_cilindro & -gapRadial_cilindro    & +pallet_planoInf & -pallet_planoSup # A limitação sup e inf do gapRadial é a mesma do pallet
        gap_regiao          = gapRadial_regiao # + União com gapSuperior_regiao
        gap_celula          = openmc.Cell(fill = self.m_helio, region = gap_regiao)


        # Definições do revestimento (iguais para todas varetas e elementos combustíveis)
        revestimentoRadial_raio = 0.475
        revestimentoRadial_comprimento = pallet_altura #Colocar aqui o comprimento total do revestimento
        revestimentoRadial_cilindro = openmc.ZCylinder(r = revestimentoRadial_raio)
        # Desenhar o revestimentoSup e revestimentoInf, isto é, o endplug. Seguir modelo do gap para facilitar
        # Não usar os planos do pallet, pois o revestimento é maior que os pallets
        revestimentoRadial_planoInf = openmc.ZPlane(z0 = -revestimentoRadial_comprimento/2, boundary_type= 'reflective') #Temporariamente reflexivo, até desenhar o reator em 3D (desenhar a parte superior e inferior)
        revestimentoRadial_planoSup = openmc.ZPlane(z0 =  revestimentoRadial_comprimento/2, boundary_type= 'reflective')
        revestimento_regiao     = +gapRadial_cilindro    & -revestimentoRadial_cilindro   & +revestimentoRadial_planoInf & -revestimentoRadial_planoSup
        revestimento_celula = openmc.Cell(fill=self.m_zircaloy, region=revestimento_regiao)


        # Definições do refrigerante ao redor do revestimento (iguais para todas varetas e elementos combustíveis)
        # Definir a região do refrigerante como infinita externa ao revestimento em todas as direções (radialmente e axialmente)
        refrigerente_regiao   = +revestimentoRadial_cilindro                      & +revestimentoRadial_planoInf & -revestimentoRadial_planoSup      
        refrigerente_celula   = openmc.Cell(fill=self.m_agua, region=refrigerente_regiao)


        # Plotando vareta completa para debug
        if plotar_interno:
            # Esta celula daqui serve apenas para plotar a geometria de uma vareta
            pallet_celula_plot   = openmc.Cell(fill=self.m_uranio31, region=pallet_regiao)

            # Criando uma célula refrigerante que seja limitada apenas para o plot
            ## Detalhe: O limite XY da caixa é baseado no pitch da vareta
            limite_xy_plot = openmc.model.RectangularPrism(axis="z", width=pitch_varetas, height=pitch_varetas)
            refrigerente_regiao_plot = +revestimentoRadial_cilindro & -limite_xy_plot & +revestimentoRadial_planoInf & -revestimentoRadial_planoSup      
            refrigerente_celula_plot = openmc.Cell(fill=self.m_agua, region=refrigerente_regiao_plot)

            # Criando um universo contendo
            vareta_universo_plot = openmc.Universe()
            vareta_universo_plot.add_cell(pallet_celula_plot)
            vareta_universo_plot.add_cell(gap_celula)
            vareta_universo_plot.add_cell(revestimento_celula)
            vareta_universo_plot.add_cell(refrigerente_celula_plot)

            # Criando uma geometria apenas para o plot
            geometria_vareta_plot = openmc.Geometry()
            geometria_vareta_plot.root_universe = vareta_universo_plot

            # Plotando várias vistas
            pasta_plots = "vareta_combustível"
            mkdir(pasta_plots, data=False, chdir=False) #Crie a pasta mas não mude para dentro da pasta
            self.plotar(geometria=geometria_vareta_plot,filename=f"{pasta_plots}/centro_xy",width=(pitch_varetas,pitch_varetas),pixels=(500,500),basis="xy")
            self.plotar(geometria=geometria_vareta_plot,filename=f"{pasta_plots}/centro_xz",width=(pitch_varetas,pitch_varetas),pixels=(500,500),basis="xz")
            
        ######################################################
        ######################################################
        ####   Definições gerais das barras de controle   ####
        ######################################################
        ######################################################

        # Definições do tubo guia da barra de controle (iguais para todos tubos guia, e também para o tubo de instrumentação)
        tuboGuiaRadial_raioInt = 0.5715
        tuboGuiaRadial_raioExt = 0.612
        tuboGuiaRadial_cilindroInt = openmc.ZCylinder(r=tuboGuiaRadial_raioInt)
        tuboGuiaRadial_cilindroExt = openmc.ZCylinder(r=tuboGuiaRadial_raioExt)
        # Igual o revestimento, tem que desenhar a parte superior e inferior.
        # Entretanto salvo engano ele deve ser aberto em baixo, e a parte superior tem o dobro do tamanho
        tuboGuia_regiao = +tuboGuiaRadial_cilindroInt & -tuboGuiaRadial_cilindroExt & +pallet_planoInf & -pallet_planoSup
        tuboGuia_celula = openmc.Cell(fill=self.m_zircaloy, region=tuboGuia_regiao)

        # Definições do refrigerante ao redor do tubo guia (iguais para todos tubos guia, e também para o tubo de instrumentação)
        # Definir a região do refrigerante como infinita externa ao revestimento em todas as direções (radialmente e axialmente)
        refrigerenteTuboGuia_regiao   = +tuboGuiaRadial_cilindroExt                      & +pallet_planoInf & -pallet_planoSup      
        refrigerenteTuboGuia_celula   = openmc.Cell(fill=self.m_agua, region=refrigerenteTuboGuia_regiao)

        # Definições da barra de controle
        # é preciso usar o parâmetro alturaBarra para definir a altura de um plano.
        # Para baixo dele é agua, para cima é barra absorvedora
        # Não esqueça do gap de água entre o tubo guia e a barra
        # Depois a gente separa as barras em bancos e usa diferentes parâmetros (alturaBarraBanco1, alturaBarraBanco2, etc.) para controlar a altura de cada um
        barraControle_aguaInf_regiao = -tuboGuiaRadial_cilindroInt & +pallet_planoInf & -pallet_planoSup
        barraControle_aguaInf_celula = openmc.Cell(fill=self.m_agua, region=barraControle_aguaInf_regiao)

        # Plotando vareta completa para debug
        if plotar_interno:
            # Criando uma célula refrigerante que seja limitada apenas para o plot
            ## Detalhe: O limite XY da caixa é baseado no pitch da vareta
            limite_xy_plot = openmc.model.RectangularPrism(axis="z", width=pitch_varetas, height=pitch_varetas)
            barraControle_aguaInf_regiao_plot = +tuboGuiaRadial_cilindroExt & -limite_xy_plot & +pallet_planoInf & -pallet_planoSup      
            barraControle_aguaInf_celula_plot = openmc.Cell(fill=self.m_agua, region=barraControle_aguaInf_regiao_plot)

            # Criando um universo contendo
            guia_universo_plot = openmc.Universe()
            guia_universo_plot.add_cell(barraControle_aguaInf_celula)
            guia_universo_plot.add_cell(tuboGuia_celula)
            guia_universo_plot.add_cell(barraControle_aguaInf_celula_plot)

            # Criando uma geometria apenas para o plot
            geometria_guia_plot = openmc.Geometry()
            geometria_guia_plot.root_universe = guia_universo_plot

            # Plotando várias vistas
            pasta_plots = "tubo_guia"
            mkdir(pasta_plots, data=False, chdir=False) #Crie a pasta mas não mude para dentro da pasta
            self.plotar(geometria=geometria_guia_plot,filename=f"{pasta_plots}/centro_xy",width=(pitch_varetas,pitch_varetas),pixels=(500,500),basis="xy")
            self.plotar(geometria=geometria_guia_plot,filename=f"{pasta_plots}/centro_xz",width=(pitch_varetas,pitch_varetas),pixels=(500,500),basis="xz")

        ######################################################
        ######################################################
        #############   Universo Agua   ######################
        ######################################################
        ######################################################
        
        # Estou pensando sobre isso ainda
        universoAgua_regiao = +pallet_planoInf & -pallet_planoSup
        universoAgua_celula = openmc.Cell(name='Preenchimento com água',
                                fill=self.m_agua,
                                region=universoAgua_regiao)
        universoAgua_universo = openmc.Universe(cells=[universoAgua_celula])
        


        ######################################################
        ######################################################
        #############   Elemento RefRad  #####################
        ######################################################
        ######################################################

        # Sobre isso também
        elementoRefRad_regiao   = +pallet_planoInf & -pallet_planoSup
        elementoRefRad_celula   = openmc.Cell(name='Refletor Radial', fill=self.m_agua, region=elementoRefRad_regiao)
        elementoRefRad_universo = openmc.Universe(cells=[elementoRefRad_celula])


        ######################################################
        ######################################################
        #########   Comum aos Elementos 31Gxx  ##############
        ######################################################
        ######################################################

        # 31G08 = Elemento com enriquecimento de 3.1% + 8 varetas dopadas com gadolina

        # Criando universo Vareta Combustível com Enriquecimento de 3.1%
        elemento31Gxx_pallet31_celula   = openmc.Cell(fill=self.m_uranio31, region= pallet_regiao)
        elemento31Gxx_vareta31_universo = openmc.Universe()
        elemento31Gxx_vareta31_universo.add_cell(elemento31Gxx_pallet31_celula)
        elemento31Gxx_vareta31_universo.add_cell(gap_celula)
        elemento31Gxx_vareta31_universo.add_cell(revestimento_celula)
        elemento31Gxx_vareta31_universo.add_cell(refrigerente_celula)

        # Criando universo Vareta Combustível com Enriquecimento de 3.1% + gadolina
        elemento31Gxx_pallet31Gadolina_celula          = openmc.Cell(fill=self.m_uranio31_gadolina, region=pallet_regiao)
        elemento31Gxx_vareta31Gadolina_universo = openmc.Universe()
        elemento31Gxx_vareta31Gadolina_universo.add_cell(elemento31Gxx_pallet31Gadolina_celula)
        elemento31Gxx_vareta31Gadolina_universo.add_cell(gap_celula)
        elemento31Gxx_vareta31Gadolina_universo.add_cell(revestimento_celula)
        elemento31Gxx_vareta31Gadolina_universo.add_cell(refrigerente_celula)


        ######################################################
        ######################################################
        #############   Elemento 31G08   #####################
        ######################################################
        ######################################################


        # Criando universo Tubo Guia para elemento 31G08 (falta desenhar o restante da geometria da barra)
        elemento31G08_tuboGuia_universo =  openmc.Universe()
        elemento31G08_tuboGuia_universo.add_cell(tuboGuia_celula)
        elemento31G08_tuboGuia_universo.add_cell(refrigerenteTuboGuia_celula)
        elemento31G08_tuboGuia_universo.add_cell(barraControle_aguaInf_celula)

        # Definindo abreviações
        C = elemento31Gxx_vareta31_universo                 # Combustível
        G = elemento31Gxx_vareta31Gadolina_universo         # Gadolina (8 varetas)
        T = elemento31G08_tuboGuia_universo                 # Tubo de Guia
        I = elemento31G08_tuboGuia_universo                 # Instrumentação (mesma dimensão do GT) 

        # Matriz 17x17 baseada na Figura 3b do documento 
        elemento31G08_matriz = [
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, T, C, C, G, C, C, C, G, C, C, T, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, T, C, C, T, C, C, I, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, G, C, C, C, C, C, C, C, C, C, G, C, C, C],
            [C, C, T, C, C, T, C, C, T, C, C, T, C, C, T, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, T, C, C, G, C, C, C, G, C, C, T, C, C, C],
            [C, C, C, C, C, T, C, C, T, C, C, T, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C],
            [C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C, C]
        ]

        # Definindo lattice do elemento 31G08

        elemento31G08_lattice = openmc.RectLattice(name='Elemento Combustivel FA3')
        elemento31G08_lattice.pitch = (pitch_varetas, pitch_varetas) # Cell Pitch de 1.26 cm 
        elemento31G08_lattice.universes = elemento31G08_matriz
        elemento31G08_lattice.lower_left = [-pitch_varetas * len(elemento31G08_matriz) / 2, -pitch_varetas * len(elemento31G08_matriz) / 2]
        elemento31G08_lattice.outer = universoAgua_universo

        elemento31G08_lattice_celula = openmc.Cell(name="Celula FA3", fill=elemento31G08_lattice)
        elemento31G08_lattice_universo = openmc.Universe(cells=[elemento31G08_lattice_celula])



        ######################################################
        ######################################################
        ###############   Elemento 31G16  ####################
        ######################################################
        ######################################################

        # 31G16 = Elemento com enriquecimento de 3.1% + 16 varetas dopadas com gadolina

        # Criando universo Tubo Guia para elemento 31G16 (falta desenhar o restante da geometria da barra)
        # Depois tem que ver a alocação do banco de barras, acho que as barras aqui estão em um banco diferente do elemento31G08
        elemento31G16_tuboGuia_universo =  openmc.Universe()
        elemento31G16_tuboGuia_universo.add_cell(tuboGuia_celula)
        elemento31G16_tuboGuia_universo.add_cell(refrigerenteTuboGuia_celula)
        elemento31G16_tuboGuia_universo.add_cell(barraControle_aguaInf_celula)

        # Reutilizando as definições de varetas que criamos antes
        C = elemento31Gxx_vareta31_universo         # Combustível 3.1%
        G = elemento31Gxx_vareta31Gadolina_universo # Gadolina (Agora serão 16 varetas)
        T = elemento31G16_tuboGuia_universo         # Tubo de Guia
        I = elemento31G16_tuboGuia_universo         # Instrumentação

        # Matriz 17x17 para o FA4 (Disposição típica com 16 BP)
        elemento31G16_matriz = [
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

        elemento31G16_lattice = openmc.RectLattice(name='Elemento Combustivel FA4')
        elemento31G16_lattice.pitch = (pitch_varetas, pitch_varetas)
        elemento31G16_lattice.universes = elemento31G16_matriz
        elemento31G16_lattice.lower_left = [-pitch_varetas * len(elemento31G16_matriz) / 2, -pitch_varetas * len(elemento31G16_matriz) / 2]
        elemento31G16_lattice.outer = universoAgua_universo

        elemento31G16_lattice_celula = openmc.Cell(name="Celula FA4", fill=elemento31G16_lattice)
        elemento31G16_lattice_universo = openmc.Universe(cells=[elemento31G16_lattice_celula])






        ######################################################
        ######################################################
        #############     Elemento 19000   ###################
        ######################################################
        ######################################################

        # Criando universo Vareta Combustível com Enriquecimento de 1.9%
        elemento19000_pallet19_celula   = openmc.Cell(fill=self.m_uranio19, region= pallet_regiao)
        elemento19000_vareta_universo = openmc.Universe()
        elemento19000_vareta_universo.add_cell(elemento19000_pallet19_celula)
        elemento19000_vareta_universo.add_cell(gap_celula)
        elemento19000_vareta_universo.add_cell(revestimento_celula)
        elemento19000_vareta_universo.add_cell(refrigerente_celula)

        # Criando universo Tubo Guia para elemento 19000 (falta desenhar o restante da geometria da barra)
        elemento19000_tuboGuia_universo =  openmc.Universe()
        elemento19000_tuboGuia_universo.add_cell(tuboGuia_celula)
        elemento19000_tuboGuia_universo.add_cell(refrigerenteTuboGuia_celula)
        elemento19000_tuboGuia_universo.add_cell(barraControle_aguaInf_celula)

        # Legendas para a matriz
        M = elemento19000_vareta_universo    # Combustível 1.9% (M de matriz)
        T = elemento19000_tuboGuia_universo
        I = elemento19000_tuboGuia_universo

        # Matriz 17x17 para o FA1 (Sem varetas de Gadolina - Figura 3a)
        elemento19000_matriz = [
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

        elemento19000_lattice = openmc.RectLattice(name='Elemento Combustivel FA1')
        elemento19000_lattice.pitch = (pitch_varetas, pitch_varetas)
        elemento19000_lattice.universes = elemento19000_matriz
        elemento19000_lattice.lower_left = [-pitch_varetas * len(elemento19000_matriz) / 2, -pitch_varetas * len(elemento19000_matriz) / 2]
        elemento19000_lattice.outer = universoAgua_universo

        elemento19000_lattice_celula = openmc.Cell(name="Celula FA1", fill=elemento19000_lattice)
        universo_19000 = openmc.Universe(cells=[elemento19000_lattice_celula])



        ######################################################
        ######################################################
        #############     Elemento 31G16   ###################
        ######################################################
        ######################################################




        C = elemento31Gxx_vareta31_universo          # Combustível 3.1%
        G = elemento31Gxx_vareta31Gadolina_universo  # Gadolina (16 varetas)
        T = elemento31G16_tuboGuia_universo          # Tubo de Guia
        I = elemento31G16_tuboGuia_universo          # Instrumentação

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
        lattice_fa2.outer = universoAgua_universo

        celula_fa2 = openmc.Cell(name="Celula FA2", fill=lattice_fa2)
        universo_31G16 = openmc.Universe(cells=[celula_fa2])



        ######################################################
        ######################################################
        #############   Elemento 31000G08   ##################
        ######################################################
        ######################################################


        C = elemento31Gxx_vareta31_universo          # Combustível 3.1%
        G = elemento31Gxx_vareta31Gadolina_universo # Gadolina (8 varetas)
        T = elemento31G16_tuboGuia_universo       # Tubo de Guia
        I = elemento31G16_tuboGuia_universo       # Instrumentação

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
        lattice_fa5.outer = universoAgua_universo

        celula_fa5 = openmc.Cell(name="Celula FA5", fill=lattice_fa5)
        universo_31000G08 = openmc.Universe(cells=[celula_fa5 ])



        ######################################################
        ######################################################
        #############    universo nucleo     #################
        ######################################################
        ######################################################


        A = universoAgua_universo
        R = elementoRefRad_universo
        V = elemento31G08_lattice_universo
        C = elemento31G16_lattice_universo
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
        lattice_nucleo.outer = universoAgua_universo

        nucleo_cilindro = openmc.ZCylinder(r = 125, boundary_type= 'vacuum')
        regiao_nucleo   =   -nucleo_cilindro & +pallet_planoInf & -pallet_planoSup

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
            geometria=None,
            filename = None,
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
            if geometria is None:
                geometria = self.lista_geometria

            if filename is None:
                filename = 'plot_' + basis + '_' + str(width) + '_' + str(pixels) + '_' + str(origin)

            plot = openmc.Plot.from_geometry(geometria)
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
            geometria.export_to_xml()
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