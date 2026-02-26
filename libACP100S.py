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
        self.m_ar.add_nuclide('O18' , 3.8829E-05 , percent_type='ao')
        self.m_ar.add_nuclide('Ar36', 2.6789E-03 , percent_type='ao')
        self.m_ar.add_nuclide('Ar38', 3.4177E-03 , percent_type='ao')
        self.m_ar.add_nuclide('Ar40', 3.2467E-03 , percent_type='ao')
        self.m_ar.set_density('g/cm3', 0.001225)
        self.lista_materiais.append(self.m_ar)
        self.m_cores[self.m_ar] = "white"


    def geometria(self):
        print("################################################")
        print("#######     Definição de Geometria        ######")
        print("################################################")

        lista_geometria = []

        pallet_altura = 1
        pallet_cilindro = openmc.ZCylinder(r = 0.4)
        
        pallet_plano_inf = openmc.ZPlane(z0 = -pallet_altura/2, boundary_type= 'reflective')
        pallet_plano_sup = openmc.ZPlane(z0 = pallet_altura/2, boundary_type= 'reflective')

        gap_cilindro = openmc.ZCylinder(r = 0.45)

        clad_cilindro = openmc.ZCylinder(r = 0.5)



        regiao_pallet   =                    -pallet_cilindro & +pallet_plano_inf & -pallet_plano_sup
        regiao_gap      = +pallet_cilindro & -gap_cilindro    & +pallet_plano_inf & -pallet_plano_sup
        regiao_clad     = +gap_cilindro    & -clad_cilindro   & +pallet_plano_inf & -pallet_plano_sup
        regiao_agua_inf = +clad_cilindro                      & +pallet_plano_inf & -pallet_plano_sup
        regiao_agua     =                                       +pallet_plano_inf & -pallet_plano_sup


        pallet_celula = openmc.Cell(fill = self.m_uranio, region = regiao_pallet)
        gap_celula = openmc.Cell(fill = self.m_ar, region = regiao_gap)
        clad_celula = openmc.Cell(fill = self.m_SS304, region = regiao_clad)
        
        agua_celula = openmc.Cell(fill = self.m_agua, region = regiao_agua_inf)
        agua_celula2 = openmc.Cell(fill = self.m_agua, region = regiao_agua)

        u = openmc.Universe(cells=[pallet_celula, gap_celula, clad_celula, agua_celula])

        ua = openmc.Universe(cells=[agua_celula2])

        lattice = openmc.RectLattice()

        
        lattice.pitch = (1.1, 1.1)
        lattice.universes = [[u, u, u],
                            [u, ua, u],
                            [u, u, u]]
        lattice.lower_left = (- (len(lattice.universes[0]) * lattice.pitch[0]) / 2.0,     - (len(lattice.universes) * lattice.pitch[1]) / 2.0)
        universo_agua_inf = openmc.Universe(cells=[openmc.Cell(fill=self.m_agua)])
        lattice.outer = universo_agua_inf


        celula_elemento_comb = openmc.Cell(fill=lattice)
        universo_elemento_comb = openmc.Universe(cells=[celula_elemento_comb])

        ######################################################
        ######################################################
        #############   Universo Agua   ######################
        ######################################################
        ######################################################
        regiao_agua     =                                       +pallet_plano_inf & -pallet_plano_sup
        agua_celula2 = openmc.Cell(fill = self.m_agua, region = regiao_agua)
        ua = openmc.Universe(cells=[agua_celula2])
  


        ######################################################
        ######################################################
        #############   Lattice Núcleo  ######################
        ######################################################
        ######################################################


        nucleo_cilindro = openmc.ZCylinder(r = 70, boundary_type= 'vacuum')
        regiao_nucleo   =   -nucleo_cilindro & +pallet_plano_inf & -pallet_plano_sup


        #A = universo_agua
        #R = universo_RefRad
        #V = universo_31G08
        #C = universo_31000G16
        #M = universo_19000
        #Y = universo_31G16


        A = ua
        R = universo_elemento_comb
        V = universo_elemento_comb
        C = universo_elemento_comb
        M = universo_elemento_comb
        Y = universo_elemento_comb

        matriz_nucleo = [
            [A,A,A,R,R,R,R,R,A,A,A],
            [A,A,R,R,V,V,V,R,R,A,A],
            [A,R,R,C,V,Y,V,C,R,R,A],
            [R,R,C,M,Y,C,Y,M,C,R,R],
            [R,V,V,Y,M,M,M,Y,V,V,R],
            [R,V,Y,C,M,C,M,C,Y,V,R],
            [R,V,V,Y,M,M,M,Y,V,V,R],
            [R,R,C,M,Y,C,Y,M,C,R,R],
            [A,R,R,C,V,Y,V,C,R,R,A],
            [A,A,R,R,V,V,V,R,R,A,A],
            [A,A,A,R,R,R,R,R,A,A,A]

        ]

        lattice_nucleo = openmc.RectLattice()
        lattice_nucleo.pitch = (3.5,3.5)
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