#######################################################################
####                                                               ####
####    Visualização Customizada: Mapa 2D, Vareta e EC Isolado     ####
####                                                               ####
####            UNIVERSIDADE FEDERAL DO RIO DE JANEIRO             ####
####                Departamento de Engenharia Nuclear             ####
####                                                               ####
####                    Jhulia Schmidt Ceccon                      ####
####                (Adaptado para Visualização de EC)             ####
#######################################################################

import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.patches as patches

# --- Configurações de Pastas ---
pasta_res = "resultados/Dados"

# --- Carga dos Dados ---
try:
    potencia_3d = np.load(f"{pasta_res}/Potencia_W_cm_3D.npy") * 0.1 # converte para KW/m
    z_coords = np.load(f"{pasta_res}/Eixo_Z_cm.npy")
    x_coords = np.load(f"{pasta_res}/Eixo_X_cm.npy")
    y_coords = np.load(f"{pasta_res}/Eixo_Y_cm.npy")
except FileNotFoundError:
    print("❌ Erro: Arquivos não encontrados. Rode a simulação primeiro!")
    exit()

#################################################################################
#######  SELEÇÃO DA VARETA (0 a N_BINS)                                 #########
#################################################################################
indice_x_vareta_selecionada = 98
indice_y_vareta_selecionada = 93

#################################################################################
#######  CONFIGURAÇÃO E SELEÇÃO DO ELEMENTO COMBUSTÍVEL (EC)            #########
#################################################################################
tamanho_malha_ec = 17 

# Número total de ECs ao longo do eixo X e Y
n_ecs_x = potencia_3d.shape[2] // tamanho_malha_ec
n_ecs_y = potencia_3d.shape[1] // tamanho_malha_ec

# Escolha o índice do Elemento Combustível (0 a n_ecs-1):
indice_x_ec_selecionado = 5
indice_y_ec_selecionado = 5

# --- Lógica de Coordenadas do EC Selecionado ---
x_start_ec = indice_x_ec_selecionado * tamanho_malha_ec
x_end_ec = x_start_ec + tamanho_malha_ec - 1
y_start_ec = indice_y_ec_selecionado * tamanho_malha_ec
y_end_ec = y_start_ec + tamanho_malha_ec - 1
#################################################################################

fatia_z = potencia_3d.shape[0] // 2

# =====================================================================
# 1. GERANDO O MAPA 2D RADIAL GLOBAL
# =====================================================================
print(f"🎨 Gerando Mapa Radial Global (Z Central)...")
plt.figure(figsize=(10, 8))

mapa = plt.pcolormesh(x_coords, y_coords, potencia_3d[fatia_z], cmap='jet', shading='auto', vmin=0, vmax=60)
plt.colorbar(mapa, label='Potência Linear [KW/m]')

# Marca a vareta
plt.plot(x_coords[indice_x_vareta_selecionada], y_coords[indice_y_vareta_selecionada], 
         'wx', markersize=12, markeredgewidth=2, label='Vareta Selecionada')

# Desenha o retângulo do EC
ax = plt.gca()
rect = patches.Rectangle((x_coords[x_start_ec], y_coords[y_start_ec]),
                        (x_coords[x_end_ec] - x_coords[x_start_ec]),
                        (y_coords[y_end_ec] - y_coords[y_start_ec]),
                        linewidth=3, edgecolor='r', facecolor='none', label='EC Selecionado')
ax.add_patch(rect)

plt.title(f'Distribuição Radial Global (Z={z_coords[fatia_z]:.1f} cm)')
plt.xlabel('X [cm]'); plt.ylabel('Y [cm]')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left') 
plt.tight_layout()
plt.savefig(f"{pasta_res}/MAPA_2D_GLOBAL_COM_EC.png", dpi=300)
plt.close()

# =====================================================================
# 2. GERANDO O PERFIL AXIAL DA VARETA SELECIONADA
# =====================================================================
print(f"📈 Gerando Perfil Axial da Vareta...")
perfil_vareta_escolhido = potencia_3d[:, indice_y_vareta_selecionada, indice_x_vareta_selecionada]

plt.figure(figsize=(10, 6))
plt.plot(z_coords, perfil_vareta_escolhido, color='blue', marker='o', linewidth=2)
plt.fill_between(z_coords, perfil_vareta_escolhido, color='blue', alpha=0.1)

plt.xlim(-107.5, 107.5) 
plt.ylim(0, np.max(potencia_3d) * 1.1) 
plt.title(f'Perfil Axial: Vareta Selecionada (X={indice_x_vareta_selecionada}, Y={indice_y_vareta_selecionada})')
plt.xlabel('Posição Axial [cm]'); plt.ylabel('Potência Linear [KW/m]')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig(f"{pasta_res}/PERFIL_VARETA.png", dpi=300)
plt.close()

# =====================================================================
# 3. GERANDO O PERFIL AXIAL DO ELEMENTO COMBUSTÍVEL SELECIONADO (MÉDIA)
# =====================================================================
print(f"📊 Gerando Perfil Axial Médio do EC...")
potencia_ec = potencia_3d[:, y_start_ec:y_end_ec+1, x_start_ec:x_end_ec+1]
perfil_medio_ec = np.mean(potencia_ec, axis=(1, 2))

plt.figure(figsize=(10, 6))
plt.plot(z_coords, perfil_medio_ec, color='red', marker='s', linewidth=2.5, label='Potência Média do EC')
plt.fill_between(z_coords, perfil_medio_ec, color='red', alpha=0.1)

plt.xlim(-107.5, 107.5) 
plt.ylim(0, np.max(potencia_3d) * 1.1)
plt.title(f'Perfil Axial Médio: EC (X={indice_x_ec_selecionado}, Y={indice_y_ec_selecionado})')
plt.xlabel('Posição Axial [cm]'); plt.ylabel('Potência Linear Média [KW/m]')
plt.grid(True, linestyle='-', alpha=0.8)
plt.legend()
plt.savefig(f"{pasta_res}/PERFIL_EC_MEDIO.png", dpi=300)
plt.close()

# =====================================================================
# 4. NOVO: GERANDO O MAPA 2D ISOLADO DO ELEMENTO COMBUSTÍVEL (ZOOM)
# =====================================================================
print(f"🔍 Gerando Mapa 2D Isolado (Zoom) do Elemento Combustível...")
plt.figure(figsize=(8, 7))

# Extrai a fatia Z central apenas para o EC
mapa_2d_ec = potencia_ec[fatia_z, :, :]

# Ajusta os limites físicos para o gráfico
extent_ec = [x_coords[x_start_ec], x_coords[x_end_ec], 
             y_coords[y_start_ec], y_coords[y_end_ec]]

# Usamos imshow para desenhar um grid bem definido para as varetas do EC
im = plt.imshow(mapa_2d_ec, cmap='jet', origin='lower', extent=extent_ec, 
                vmin=np.min(potencia_3d[fatia_z]), vmax=np.max(potencia_3d[fatia_z]))

plt.colorbar(im, label='Potência Linear [KW/m]')

# Se a vareta selecionada estiver dentro deste EC, vamos marcá-la!
if (x_start_ec <= indice_x_vareta_selecionada <= x_end_ec) and \
   (y_start_ec <= indice_y_vareta_selecionada <= y_end_ec):
    plt.plot(x_coords[indice_x_vareta_selecionada], y_coords[indice_y_vareta_selecionada], 
             'wx', markersize=16, markeredgewidth=3, label='Sua Vareta')
    plt.legend(loc='upper right')

plt.title(f'Mapa 2D do EC Selecionado (Índices: X={indice_x_ec_selecionado}, Y={indice_y_ec_selecionado})\nZ = {z_coords[fatia_z]:.1f} cm (Centro do Núcleo)')
plt.xlabel('X [cm]')
plt.ylabel('Y [cm]')
plt.grid(color='black', linestyle='-', linewidth=0.5, alpha=0.3) # Adiciona linhas de grade suaves

plt.savefig(f"{pasta_res}/MAPA_2D_EC_ISOLADO.png", dpi=300)
plt.close()


print("\n" + "="*70)
print(f"✅ Arquivos gerados em /{pasta_res}:")
print(f"   1. MAPA_2D_GLOBAL_COM_EC.png  (Visão geral do reator)")
print(f"   2. MAPA_2D_EC_ISOLADO.png     (🔍 ZOOM no EC selecionado)")
print(f"   3. PERFIL_VARETA.png          (Gráfico de linha da vareta)")
print(f"   4. PERFIL_EC_MEDIO.png        (Gráfico de linha do EC)")
print("="*70)