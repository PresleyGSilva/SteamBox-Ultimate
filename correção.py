import flet as ft
import subprocess
import os
import sys
import time
import requests
import zipfile
import winreg
import shutil
import tempfile

# Função melhorada para obter o caminho correto dos recursos
def resource_path(relative_path):
    """Obtém o caminho absoluto para o recurso, funciona para dev e para PyInstaller"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS2 if hasattr(sys, '_MEIPASS2') else sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    # Se o arquivo existe no caminho base, retorna
    full_path = os.path.join(base_path, relative_path)
    if os.path.exists(full_path):
        return full_path
    
    # Se não encontrou, tenta outros caminhos
    alt_paths = [
        os.path.join(os.getcwd(), relative_path),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path),
        os.path.join(os.path.dirname(sys.executable), relative_path),
        relative_path
    ]
    
    for path in alt_paths:
        if os.path.exists(path):
            return path
    
    # Retorna o caminho original se não encontrou em nenhum lugar
    return full_path

def get_icon_path():
    """Tenta várias estratégias para encontrar o ícone"""
    possible_paths = [
        resource_path("logo.ico"),
        os.path.join(os.path.dirname(sys.executable), "logo.ico"),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico"),
        os.path.join(os.getcwd(), "logo.ico"),
        "logo.ico"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Ícone encontrado em: {path}")
            return path
    
    print("Ícone não encontrado em nenhum local")
    return None

def main(page: ft.Page):
    page.title = "SteamBox - Correção Steam"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#1a1a1a"
    
    # Configurações da janela REDIMENSIONADA
    page.window_width = 560
    page.window_height = 780
    page.window_resizable = False
    page.window_maximizable = False
    page.window_minimizable = True
    page.window_center()
    page.window_title_bar_hidden = False
    
    # Configurar o ícone da janela
    try:
        icon_path = get_icon_path()
        if icon_path and os.path.exists(icon_path):
            abs_icon_path = os.path.abspath(icon_path)
            print(f"Tentando definir ícone: {abs_icon_path}")
            page.window_icon = abs_icon_path
    except Exception as e:
        print(f"Erro ao definir ícone: {e}")
    
    # Elementos da interface
    logo_path = resource_path("logo.png")
    
    if not logo_path or not os.path.exists(logo_path):
        alt_logo_paths = [
            os.path.join(os.path.dirname(sys.executable), "logo.png"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png"),
            os.path.join(os.getcwd(), "logo.png"),
            "logo.png"
        ]
        
        for path in alt_logo_paths:
            if os.path.exists(path):
                logo_path = path
                print(f"Logo encontrada em: {logo_path}")
                break
    
    logo = ft.Image(
        src=logo_path if logo_path and os.path.exists(logo_path) else "https://via.placeholder.com/80",
        width=250,
        height=250,
        fit=ft.ImageFit.CONTAIN,
    )
    
    titulo = ft.Text(
        "STEAMBOX",
        size=30,
        weight=ft.FontWeight.BOLD,
        color="#ffffff",
        text_align=ft.TextAlign.CENTER
    )
    
    subtitulo = ft.Text(
        "Clique abaixo para corrigir a sua steam",
        size=12,
        color="#00ff0d",
        text_align=ft.TextAlign.CENTER
    )
    
    texto_status = ft.Text(
        "Pronto para corrigir a sua Steam",
        size=13,
        color="#ffffff",
        text_align=ft.TextAlign.CENTER
    )
    
    # Barra de progresso REDIMENSIONADA
    barra_progresso = ft.ProgressBar(
        width=300,
        height=8,
        color="#0078d4",
        bgcolor="#333333"
    )
    barra_progresso.visible = False
    
    texto_progresso = ft.Text(
        "",
        size=11,
        color="#0078d4",
        text_align=ft.TextAlign.CENTER
    )
    
    botao_downgrade = ft.ElevatedButton(
        content=ft.Text("CORRIGIR JOGOS DA STEAM", weight=ft.FontWeight.BOLD),
        width=260,
        height=50,
        bgcolor="#0078d4",
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=10
        )
    )
    
    # BOTÃO LIBERAR ATUALIZAÇÕES
    botao_liberar = ft.ElevatedButton(
        content=ft.Text("LIBERAR ATUALIZAÇÕES", weight=ft.FontWeight.BOLD),
        width=260,
        height=50,
        bgcolor="#ffa100",
        color="white",
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=10
        )
    )
    
    def atualizar_status(mensagem, cor="#cccccc"):
        texto_status.value = mensagem
        texto_status.color = cor
        page.update()
    
    def atualizar_progresso(porcentagem, texto=""):
        barra_progresso.value = porcentagem / 100
        texto_progresso.value = texto
        page.update()
    
    def get_steam_path():
        """Obtém o caminho do Steam a partir do registro do Windows"""
        caminhos_registro = [
            (winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Valve\Steam", "InstallPath"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\WOW6432Node\Valve\Steam", "InstallPath")
        ]
        
        for hive, path, value in caminhos_registro:
            try:
                with winreg.OpenKey(hive, path) as key:
                    caminho, _ = winreg.QueryValueEx(key, value)
                    if caminho and os.path.exists(caminho):
                        steam_exe = os.path.join(caminho, "Steam.exe")
                        if os.path.exists(steam_exe):
                            return caminho
            except:
                continue
        
        return None
    
    def kill_steam_processes():
        """Mata todos os processos do Steam"""
        processos = ["steam.exe", "steamservice.exe", "steamwebhelper.exe"]
        for processo in processos:
            try:
                subprocess.run(f"taskkill /F /IM {processo} /T", 
                             shell=True, 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL,
                             creationflags=subprocess.CREATE_NO_WINDOW)
            except:
                pass
        time.sleep(2)
    
    def criar_steam_cfg(caminho_steam):
        """Cria o arquivo steam.cfg para bloquear atualizações"""
        steam_cfg = os.path.join(caminho_steam, "steam.cfg")
        try:
            with open(steam_cfg, 'w', encoding='utf-8') as f:
                f.write("BootStrapperInhibitAll=enable\n")
                f.write("BootStrapperForceSelfUpdate=disable\n")
                f.write("# Este arquivo previne atualizações automáticas do Steam\n")
                f.write("# Remova este arquivo para permitir atualizações novamente\n")
            return True
        except Exception as e:
            print(f"Erro ao criar steam.cfg: {e}")
            return False
    
    def fazer_backup_steam(caminho_steam):
        """Faz backup dos arquivos atuais do Steam"""
        backup_dir = os.path.join(caminho_steam, "backup_steam")
        try:
            if os.path.exists(backup_dir):
                shutil.rmtree(backup_dir)
            
            os.makedirs(backup_dir, exist_ok=True)
            
            arquivos_importantes = ["Steam.exe", "steam.dll", "steamclient.dll", 
                                  "steamui.dll", "steamservice.exe", "hid.dll"]
            
            for arquivo in arquivos_importantes:
                origem = os.path.join(caminho_steam, arquivo)
                if os.path.exists(origem):
                    shutil.copy2(origem, os.path.join(backup_dir, arquivo))
            
            return True
        except Exception as e:
            print(f"Erro ao fazer backup: {e}")
            return False
    
    def extrair_hid_dll_do_steambox_hid(caminho_steam):
        """
        Extrai o hid.dll do arquivo steambox hid.zip seguindo o caminho:
        steambox hid.zip/steambox/steambox.zip/hid.dll para a pasta raiz da Steam
        """
        caminho_steambox_hid_zip = resource_path("steambox hid.zip")
        
        if not os.path.exists(caminho_steambox_hid_zip):
            atualizar_status("❌ steambox hid.zip não encontrado!", "#ff4444")
            print(f"Procurando steambox hid.zip em: {caminho_steambox_hid_zip}")
            return False
        
        try:
            print(f"Encontrado steambox hid.zip em: {caminho_steambox_hid_zip}")
            print(f"Extraindo hid.dll para: {caminho_steam}")
            atualizar_status("📦 Processando steambox hid.zip...", "#0078d4")
            
            # Criar diretório temporário para extração
            temp_dir = tempfile.mkdtemp()
            print(f"📁 Diretório temporário criado: {temp_dir}")
            
            # Extrair steambox hid.zip para o diretório temporário
            with zipfile.ZipFile(caminho_steambox_hid_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
                print(f"📦 Arquivos extraídos do steambox hid.zip: {zip_ref.namelist()}")
            
            # Caminho esperado: steambox/steambox.zip
            steambox_zip_path = os.path.join(temp_dir, "steambox", "steambox.zip")
            
            if not os.path.exists(steambox_zip_path):
                # Procurar por steambox.zip em qualquer lugar dentro do temp_dir
                for root, dirs, files in os.walk(temp_dir):
                    if "steambox.zip" in files:
                        steambox_zip_path = os.path.join(root, "steambox.zip")
                        print(f"✅ steambox.zip encontrado em: {steambox_zip_path}")
                        break
                else:
                    atualizar_status("❌ steambox.zip não encontrado dentro de steambox hid.zip!", "#ff4444")
                    shutil.rmtree(temp_dir)
                    return False
            
            print(f"Processando: {steambox_zip_path}")
            atualizar_status("📦 Extraindo hid.dll de steambox.zip...", "#0078d4")
            
            # Extrair hid.dll do steambox.zip para a pasta da Steam
            hid_encontrado = False
            with zipfile.ZipFile(steambox_zip_path, 'r') as inner_zip:
                print(f"📦 Arquivos dentro de steambox.zip: {inner_zip.namelist()}")
                
                for item in inner_zip.namelist():
                    if item.endswith('hid.dll') or 'hid.dll' in item:
                        # Extrair o hid.dll diretamente para a pasta da Steam
                        hid_dll_dest = os.path.join(caminho_steam, 'hid.dll')
                        
                        # Se já existir um hid.dll na Steam, fazer backup
                        if os.path.exists(hid_dll_dest):
                            backup_hid = os.path.join(caminho_steam, 'hid_backup.dll')
                            try:
                                shutil.copy2(hid_dll_dest, backup_hid)
                                print(f"💾 Backup do hid.dll existente criado: {backup_hid}")
                            except:
                                pass
                        
                        # Extrair o novo hid.dll
                        with open(hid_dll_dest, 'wb') as f:
                            f.write(inner_zip.read(item))
                        
                        print(f"✅ hid.dll extraído para a Steam em: {hid_dll_dest}")
                        atualizar_status("✅ hid.dll extraído com sucesso para a Steam!", "#00ff88")
                        hid_encontrado = True
                        break
            
            # Limpar diretório temporário
            shutil.rmtree(temp_dir)
            print(f"🧹 Diretório temporário removido: {temp_dir}")
            
            if hid_encontrado:
                return True
            else:
                atualizar_status("⚠️ hid.dll não encontrado dentro do steambox.zip", "#ffaa00")
                return False
            
        except Exception as ex:
            print(f"❌ Erro ao extrair hid.dll: {str(ex)}")
            import traceback
            traceback.print_exc()
            return False
    
    def executar_downgrade(e):
        """Função principal que executa o downgrade"""
        botao_downgrade.disabled = True
        botao_liberar.disabled = True
        barra_progresso.visible = True
        
        atualizar_status("🔍 Procurando instalação do Steam...", "#0078d4")
        atualizar_progresso(0, "Iniciando...")
        
        caminho_steam = get_steam_path()
        if not caminho_steam:
            atualizar_status("❌ Steam não encontrado!", "#ff4444")
            barra_progresso.visible = False
            botao_downgrade.disabled = False
            botao_liberar.disabled = False
            return
        
        atualizar_status(f"✅ Steam encontrado em: {caminho_steam}", "#0078d4")
        atualizar_progresso(5, "Fazendo backup dos arquivos atuais...")
        
        fazer_backup_steam(caminho_steam)
        
        atualizar_status("🛑 Fechando Steam...", "#0078d4")
        atualizar_progresso(10, "Fechando processos do Steam...")
        
        kill_steam_processes()
        
        steam_cfg = os.path.join(caminho_steam, "steam.cfg")
        if os.path.exists(steam_cfg):
            try:
                os.remove(steam_cfg)
            except:
                pass
        
        # PASSO 1: Extrair latest32bitsteam.zip
        caminho_zip = resource_path("latest32bitsteam.zip")
        
        if not os.path.exists(caminho_zip):
            atualizar_status("❌ latest32bitsteam.zip não encontrado!", "#ff4444")
            print(f"Procurando latest32bitsteam.zip em: {caminho_zip}")
            barra_progresso.visible = False
            botao_downgrade.disabled = False
            botao_liberar.disabled = False
            return
        
        print(f"Encontrado latest32bitsteam.zip em: {caminho_zip}")
        atualizar_status("📦 Extraindo arquivos da Steam...", "#0078d4")
        atualizar_progresso(30, "Instalando arquivos da Steam...")
        
        # Extrair todos os arquivos do latest32bitsteam.zip e substituir na pasta raiz do Steam
        try:
            with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
                arquivos = [f for f in zip_ref.namelist() if not f.endswith('/')]
                total_arquivos = len(arquivos)
                
                for i, arquivo in enumerate(arquivos, 1):
                    destino = os.path.join(caminho_steam, arquivo)
                    
                    # Se o arquivo já existe, vamos substituir
                    if os.path.exists(destino):
                        os.remove(destino)
                    
                    # Extrair o arquivo
                    zip_ref.extract(arquivo, caminho_steam)
                    
                    # Atualizar progresso
                    porcentagem = 30 + (i / total_arquivos) * 40
                    texto = f"Extraindo... {i}/{total_arquivos} arquivos"
                    atualizar_progresso(porcentagem, texto)
                
                atualizar_status(f"✅ Extraídos {total_arquivos} arquivos da Steam", "#0078d4")
                print(f"Extraídos {total_arquivos} arquivos para: {caminho_steam}")
            
            # PASSO 2: Extrair hid.dll do steambox hid.zip para a pasta da Steam
            atualizar_status("📦 Extraindo hid.dll do steambox hid.zip...", "#0078d4")
            atualizar_progresso(70, "Extraindo hid.dll para a Steam...")
            
            if extrair_hid_dll_do_steambox_hid(caminho_steam):
                atualizar_status(f"✅ hid.dll extraído com sucesso para a Steam!", "#00ff88")
            else:
                atualizar_status("⚠️ Não foi possível extrair hid.dll", "#ffaa00")
            
            atualizar_status("⚙️ Configurando Steam...", "#0078d4")
            atualizar_progresso(90, "Criando configuração...")
            
            criar_steam_cfg(caminho_steam)
            
            atualizar_status("🚀 Iniciando Steam...", "#0078d4")
            atualizar_progresso(95, "Iniciando Steam com versão antiga...")
            steam_exe = os.path.join(caminho_steam, "Steam.exe")
            
            try:
                subprocess.Popen([steam_exe, "-clearbeta"], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL,
                               creationflags=subprocess.CREATE_NO_WINDOW)
                atualizar_status("✅ Correção completa! Steam iniciada.", "#00ff88")
                atualizar_progresso(100, "✅ Processo finalizado!")
            except Exception as e:
                atualizar_status("✅ Correção completa! Inicie a Steam manualmente.", "#00ff88")
                atualizar_progresso(100, "✅ Processo finalizado!")
            
        except Exception as e:
            atualizar_status(f"❌ Erro durante a extração: {str(e)}", "#ff4444")
            print(f"Erro detalhado: {e}")
        
        finally:
            time.sleep(2)
            barra_progresso.visible = False
            texto_progresso.value = ""
            botao_downgrade.disabled = False
            botao_liberar.disabled = False
            page.update()
    
    def liberar_atualizacoes(e):
        """Remove o steam.cfg para permitir atualizações da Steam"""
        botao_liberar.disabled = True
        botao_downgrade.disabled = True
        
        atualizar_status("🔍 Procurando instalação do Steam...", "#ffaa00")
        
        caminho_steam = get_steam_path()
        if not caminho_steam:
            atualizar_status("❌ Steam não encontrado!", "#ff4444")
            botao_liberar.disabled = False
            botao_downgrade.disabled = False
            return
        
        atualizar_status("🛑 Fechando Steam...", "#ffaa00")
        
        kill_steam_processes()
        
        steam_cfg = os.path.join(caminho_steam, "steam.cfg")
        if os.path.exists(steam_cfg):
            try:
                os.remove(steam_cfg)
                atualizar_status("✅ steam.cfg removido! Atualizações liberadas.", "#00ff88")
                
                atualizar_status("🚀 Iniciando Steam para atualização...", "#ffaa00")
                steam_exe = os.path.join(caminho_steam, "Steam.exe")
                
                try:
                    subprocess.Popen([steam_exe], 
                                   stdout=subprocess.DEVNULL, 
                                   stderr=subprocess.DEVNULL,
                                   creationflags=subprocess.CREATE_NO_WINDOW)
                    atualizar_status("✅ Atualização iniciada. Steam abrirá automaticamente.", "#00ff88")
                except:
                    atualizar_status("✅ Atualizações liberadas. Inicie o Steam manualmente.", "#00ff88")
            except Exception as e:
                atualizar_status(f"❌ Erro ao remover steam.cfg: {str(e)}", "#ff4444")
        else:
            atualizar_status("ℹ️ steam.cfg não encontrado. Atualizações já estão liberadas.", "#00ff88")
        
        botao_liberar.disabled = False
        botao_downgrade.disabled = False
        page.update()
    
    # Configurar ações dos botões
    botao_downgrade.on_click = executar_downgrade
    botao_liberar.on_click = liberar_atualizacoes
    
    # Layout da interface
    container = ft.Container(
        expand=True,
        padding=15,
        content=ft.Column(
            [
                ft.Container(
                    content=logo,
                    alignment=ft.alignment.center
                ),
                ft.Container(height=8),
                titulo,
                ft.Container(height=4),
                subtitulo,
                ft.Container(height=15),
                
                ft.Container(
                    content=botao_downgrade,
                    alignment=ft.alignment.center
                ),
                
                ft.Container(height=20),
                
                ft.Container(
                    content=botao_liberar,
                    alignment=ft.alignment.center
                ),
                
                ft.Container(height=15),
                
                barra_progresso,
                ft.Container(height=4),
                texto_progresso,
                
                ft.Container(height=15),
                
                texto_status,
                
                ft.Container(expand=True),
                
                ft.Text(
                    "Versão 1.0.0",
                    size=9,
                    color="#666666",
                    text_align=ft.TextAlign.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )
    
    page.add(container)

def instalar_dependencias():
    """Instala as dependências necessárias"""
    dependencias = ["requests", "flet"]
    
    for dep in dependencias:
        try:
            if dep == "flet":
                __import__("flet")
            elif dep == "requests":
                __import__("requests")
        except ImportError:
            print(f"Instalando {dep}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)

if __name__ == "__main__":
    instalar_dependencias()
    
    try:
        ft.app(target=main, view=ft.FLET_APP)
    except Exception as e:
        print(f"Erro ao iniciar aplicativo: {e}")
        ft.app(target=main)