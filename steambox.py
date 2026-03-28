# ================== PROTEÇÃO CONTRA ENGENHARIA REVERSA ==================
import sys
import os
import hashlib
import time
import platform
import ctypes
if platform.system() == "Windows":
    try:
        from ctypes import windll
    except ImportError:
        pass

class SecuritySystem:
    def __init__(self):
        self.app_start_time = time.time()
        self.security_breach = False
        
    def debugger_detection(self):
        """Detecta debuggers e ferramentas de reversão"""
        try:
            if platform.system() == "Windows" and hasattr(ctypes, 'windll'):
                if ctypes.windll.kernel32.IsDebuggerPresent():
                    return False
        except:
            pass
        return True
    
    def integrity_check(self):
        """Verifica integridade do executável"""
        try:
            if getattr(sys, 'frozen', False):
                exe_path = sys.executable
                if not exe_path.lower().endswith('.exe'):
                    return False
        except:
            return False
        return True
    
    def timing_attack_detection(self):
        """Detecta manipulação de tempo"""
        current_time = time.time()
        if current_time < self.app_start_time:
            return False
        return True
    
    def run_security_checks(self):
        """Executa verificações de segurança"""
        time.sleep(0.3)  # Delay anti-detecção
        
        security_checks = [
            self.debugger_detection(),
            self.integrity_check(),
            self.timing_attack_detection()
        ]
        
        if not all(security_checks):
            self.security_breach = True
            self.emergency_shutdown()
            return False
            
        return True
    
    def emergency_shutdown(self):
        """Desligamento de emergência"""
        try:
            if hasattr(sys, 'frozen'):
                os._exit(0)
            else:
                sys.exit(0)
        except:
            pass

# Inicializar sistema de segurança
security = SecuritySystem()
if not security.run_security_checks():
    print("Sistema de segurança violado.")
    sys.exit(1)
# ================== FIM DAS PROTEÇÕES ==================

import flet as ft
import requests
import hashlib
import uuid
import subprocess
import os
import sys
import zipfile
import tempfile
import shutil
import time
import threading
import json
import re
import configparser
from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter
import base64
import platform
import psutil
import random

# Importação condicional para Windows
if platform.system() == "Windows":
    try:
        import winreg
    except ImportError:
        winreg = None
else:
    winreg = None

# ================== CONFIGURAÇÕES DO SERVIDOR ==================
OBFUSCATED_URL_1 = "https://generator.ryuu.lol"
OBFUSCATED_AUTH = "RYUUMANIFESTsl9z9u"
OBFUSCATED_URL_2 = "https://generator.ryuu.lol"

# API ENDPOINTS RYUU (FORNECIDOS)
API_MANIFEST = f"{OBFUSCATED_URL_1}/secure_download"
API_LUA = f"{OBFUSCATED_URL_1}/resellerlua"
API_REQUEST_UPDATE = f"{OBFUSCATED_URL_1}/resellerrequestupdate"
API_REQUEST_GAME = f"{OBFUSCATED_URL_1}/resellerrequest"
API_UPDATE_GAME = f"{OBFUSCATED_URL_1}/resellerupdate"

# ===== CONFIGURAÇÕES DO SISTEMA DE LICENÇA =====
OBFUSCATED_LICENSE_SERVER = "http://72.60.254.19:5003"

# ================== SUPORTE A PYINSTALLER ==================
def resource_path(relative_path):
    """Path absoluto de recurso, funciona em dev e PyInstaller."""
    try:
        base_path = sys._MEIPASS  # type: ignore
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ================== FUNÇÃO PARA CRIAR BACKGROUND GRADIENTE ==================
def create_gradient_background(width, height, color1="#0f172a", color2="#1e293b"):
    """Cria uma imagem de gradiente para background"""
    try:
        # Criar imagem gradiente
        image = Image.new("RGB", (width, height), color1)
        draw = ImageDraw.Draw(image)
        
        # Desenhar gradiente radial
        for i in range(height):
            # Gradiente vertical
            ratio = i / height
            r = int(int(color1[1:3], 16) * (1 - ratio) + int(color2[1:3], 16) * ratio)
            g = int(int(color1[3:5], 16) * (1 - ratio) + int(color2[3:5], 16) * ratio)
            b = int(int(color1[5:7], 16) * (1 - ratio) + int(color2[5:7], 16) * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            draw.line([(0, i), (width, i)], fill=color)
        
        # Adicionar ruído sutil
        pixels = image.load()
        for i in range(width):
            for j in range(height):
                if random.random() < 0.05:  # 5% de chance de ruído
                    r, g, b = pixels[i, j]
                    noise = random.randint(-5, 5)
                    pixels[i, j] = (
                        max(0, min(255, r + noise)),
                        max(0, min(255, g + noise)),
                        max(0, min(255, b + noise))
                    )
        
        # Aplicar blur suave
        image = image.filter(ImageFilter.GaussianBlur(radius=2))
        
        # Converter para base64
        buffered = BytesIO()
        image.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception as e:
        print(f"Erro ao criar gradiente: {e}")
        return None

# ================== FUNÇÃO PARA CRIAR OVERLAY ESCURO ==================
def create_dark_overlay():
    """Cria uma overlay escura para melhor contraste do texto"""
    try:
        overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 180))  # Preto com 70% de opacidade
        buffered = BytesIO()
        overlay.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")
    except Exception:
        return None

# ================== FUNÇÃO PARA ENCONTRAR LOGO EM MÚLTIPLOS CAMINHOS ==================
def find_logo():
    """Procura a logo em múltiplos locais possíveis - PRIORIDADE PARA PNG"""
    
    # Lista de possíveis caminhos para a logo (PNG primeiro)
    possible_paths = [
        # Caminho específico que você mencionou (PNG)
        r"D:\Korea Store\Kenix app\Aplicativo venda\logo.png",
        r"D:\Korea Store\Kenix app\Aplicativo venda\logo.PNG",
        
        # Caminho atual (PNG)
        os.path.join(os.path.abspath("."), "logo.png"),
        os.path.join(os.path.abspath("."), "logo.PNG"),
        
        # Caminho do executável (PNG)
        os.path.join(os.path.dirname(sys.executable), "logo.png") if getattr(sys, 'frozen', False) else None,
        os.path.join(os.path.dirname(sys.executable), "logo.PNG") if getattr(sys, 'frozen', False) else None,
        
        # ICO como último recurso (menor prioridade)
        r"D:\Korea Store\Kenix app\Aplicativo venda\logo.ico",
        os.path.join(os.path.abspath("."), "logo.ico"),
        os.path.join(os.path.dirname(sys.executable), "logo.ico") if getattr(sys, 'frozen', False) else None,
    ]
    
    # Filtrar None values
    possible_paths = [p for p in possible_paths if p is not None]
    
    for path in possible_paths:
        try:
            if os.path.exists(path):
                print(f"✅ Logo encontrada em: {path}")
                
                # Se for ICO, podemos converter para PNG ou usar como está
                if path.lower().endswith('.ico'):
                    try:
                        # Tentar converter ICO para PNG para melhor qualidade
                        img = Image.open(path)
                        # ICO pode ter múltiplos tamanhos, pegar o maior
                        if hasattr(img, 'n_frames') and img.n_frames > 1:
                            # Pegar o frame com maior resolução
                            sizes = []
                            for i in range(img.n_frames):
                                img.seek(i)
                                sizes.append((img.size[0] * img.size[1], i))
                            if sizes:
                                best_frame = max(sizes, key=lambda x: x[0])[1]
                                img.seek(best_frame)
                        
                        # Converter para RGB se necessário
                        if img.mode in ('RGBA', 'LA', 'P'):
                            # Manter transparência
                            pass
                        else:
                            img = img.convert('RGBA')
                        
                        # Salvar em BytesIO como PNG
                        buffered = BytesIO()
                        img.save(buffered, format="PNG", quality=95)
                        return base64.b64encode(buffered.getvalue()).decode("utf-8")
                    except Exception as e:
                        print(f"Erro ao converter ICO: {e}")
                        # Fallback: ler como binário
                        with open(path, "rb") as img_file:
                            return base64.b64encode(img_file.read()).decode("utf-8")
                else:
                    # PNG direto
                    with open(path, "rb") as img_file:
                        return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception as e:
            print(f"Erro ao tentar carregar {path}: {e}")
    
    print("❌ Logo não encontrada em nenhum dos caminhos")
    return None

# ================== SISTEMA DE LICENÇA CORRIGIDO ==================
class LicenseSystem:
    def __init__(self):
        self.server_url = OBFUSCATED_LICENSE_SERVER
        self.license_file = os.path.join(os.path.expanduser("~"), "steambox_license.lic")
        self.hwid_file = os.path.join(os.path.expanduser("~"), "steambox_hwid.bin")
        
    def get_motherboard_id_secure(self):
        """Gera ID ÚNICO e IMUTÁVEL baseado em múltiplas fontes ESTÁVEIS"""
        
        # PRIMEIRO: Tentar carregar HWID salvo (evita mudanças)
        saved_hwid = self.load_saved_hwid()
        if saved_hwid:
            print("✅ HWID carregado do arquivo salvo")
            return saved_hwid
            
        # SEGUNDO: Gerar novo HWID com fontes ESTÁVEIS
        hwid_sources = []
        
        try:
            # 1. SERIAL DA PLACA-MÃE (MAIS ESTÁVEL)
            if platform.system() == "Windows" and winreg:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS")
                    try:
                        serial, _ = winreg.QueryValueEx(key, "BaseBoardSerialNumber")
                        if serial and serial.strip():
                            hwid_sources.append(f"MB_SERIAL:{serial}")
                            print(f"🔧 Serial Placa-Mãe: {serial}")
                    except:
                        pass
                        
                    try:
                        product, _ = winreg.QueryValueEx(key, "BaseBoardProduct")
                        if product and product.strip():
                            hwid_sources.append(f"MB_PRODUCT:{product}")
                    except:
                        pass
                        
                    try:
                        manufacturer, _ = winreg.QueryValueEx(key, "BaseBoardManufacturer")
                        if manufacturer and manufacturer.strip():
                            hwid_sources.append(f"MB_MANUF:{manufacturer}")
                    except:
                        pass
                    winreg.CloseKey(key)
                except Exception as e:
                    print(f"⚠️ Erro registro placa-mãe: {e}")
            
            # 2. SERIAL DO DISCO SISTEMA (MUITO ESTÁVEL)
            try:
                for partition in psutil.disk_partitions():
                    if 'fixed' in partition.opts and 'C:' in partition.device:
                        disk_serial = self.get_disk_serial(partition.device)
                        if disk_serial:
                            hwid_sources.append(f"DISK_SERIAL:{disk_serial}")
                            print(f"💾 Serial Disco C: {disk_serial}")
                            break
            except Exception as e:
                print(f"⚠️ Erro serial disco: {e}")
            
            # 3. UUID DO SISTEMA (Windows)
            try:
                import uuid
                system_uuid = str(uuid.getnode())
                if system_uuid and system_uuid != "0":
                    hwid_sources.append(f"SYSTEM_UUID:{system_uuid}")
            except:
                pass
            
            # 4. ID DO PROCESSADOR (ESTÁVEL)
            try:
                processor_id = self.get_processor_id()
                if processor_id:
                    hwid_sources.append(f"CPU_ID:{processor_id}")
            except:
                pass
            
            # VERIFICAR se temos fontes suficientes
            if len(hwid_sources) < 2:
                raise Exception("Fontes insuficientes para gerar HWID estável")
                
            # GERAR HWID ÚNICO
            hwid_data = "|".join(sorted(hwid_sources))
            motherboard_id = hashlib.sha256(hwid_data.encode()).hexdigest()[:24].upper()
            
            print(f"🔐 Fontes HWID: {len(hwid_sources)}")
            print(f"📋 HWID Gerado: {motherboard_id}")
            
            # SALVAR HWID para uso futuro
            self.save_hwid(motherboard_id)
            
            return motherboard_id
            
        except Exception as e:
            print(f"❌ Erro crítico ao gerar HWID: {e}")
            return self.get_fallback_secure()
    
    def get_disk_serial(self, drive):
        """Obtém serial físico do disco"""
        try:
            if os.name == 'nt':
                import ctypes
                import ctypes.wintypes
                
                kernel32 = ctypes.windll.kernel32
                volume_name = ctypes.create_unicode_buffer(1024)
                serial_number = ctypes.wintypes.DWORD()
                max_component_length = ctypes.wintypes.DWORD()
                file_system_flags = ctypes.wintypes.DWORD()
                file_system_name = ctypes.create_unicode_buffer(1024)
                
                success = kernel32.GetVolumeInformationW(
                    ctypes.c_wchar_p(drive),
                    volume_name,
                    ctypes.sizeof(volume_name),
                    ctypes.byref(serial_number),
                    ctypes.byref(max_component_length),
                    ctypes.byref(file_system_flags),
                    file_system_name,
                    ctypes.sizeof(file_system_name)
                )
                
                if success:
                    return str(serial_number.value)
            return None
        except:
            return None
    
    def get_processor_id(self):
        """Obtém ID do processador"""
        try:
            if platform.system() == "Windows" and winreg:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
                processor_name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
                winreg.CloseKey(key)
                return hashlib.md5(processor_name.encode()).hexdigest()[:12].upper()
            else:
                return hashlib.md5(platform.processor().encode()).hexdigest()[:12].upper()
        except:
            return None
    
    def save_hwid(self, hwid):
        """Salva HWID para evitar mudanças futuras"""
        try:
            with open(self.hwid_file, 'w') as f:
                f.write(hwid)
            print(f"💾 HWID salvo: {self.hwid_file}")
        except Exception as e:
            print(f"⚠️ Erro ao salvar HWID: {e}")
    
    def load_saved_hwid(self):
        """Carrega HWID salvo"""
        try:
            if os.path.exists(self.hwid_file):
                with open(self.hwid_file, 'r') as f:
                    hwid = f.read().strip()
                if len(hwid) == 24:
                    return hwid
        except:
            pass
        return None
    
    def get_fallback_secure(self):
        """Fallback ULTRA SEGURO quando tudo falha"""
        try:
            fallback_sources = []
            
            computer_name = os.getenv("COMPUTERNAME", "UNKNOWN")
            user_name = os.getenv("USERNAME", "UNKNOWN")
            fallback_sources.append(f"COMP:{computer_name}")
            fallback_sources.append(f"USER:{user_name}")
            
            try:
                for partition in psutil.disk_partitions():
                    if 'fixed' in partition.opts:
                        try:
                            usage = psutil.disk_usage(partition.mountpoint)
                            fallback_sources.append(f"DISK:{partition.device}:{usage.total}")
                        except:
                            pass
            except:
                pass
                
            try:
                import socket
                hostname = socket.gethostname()
                fallback_sources.append(f"HOST:{hostname}")
            except:
                pass
            
            fallback_data = "|".join(sorted(fallback_sources))
            fallback_id = hashlib.sha256(fallback_data.encode()).hexdigest()[:24].upper()
            
            self.save_hwid(fallback_id)
            
            print(f"🔄 Usando Fallback HWID: {fallback_id}")
            return fallback_id
            
        except Exception as e:
            print(f"❌ ERRO CRÍTICO no fallback: {e}")
            emergency_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:24].upper()
            self.save_hwid(emergency_id)
            return emergency_id

    def get_motherboard_id(self):
        return self.get_motherboard_id_secure()
    
    def save_license(self, license_key):
        """Salva a licença ativada"""
        try:
            license_data = {
                'license_key': license_key,
                'motherboard_id': self.get_motherboard_id(),
                'activated_at': time.time()
            }
                
            with open(self.license_file, 'w') as f:
                json.dump(license_data, f)
            print(f"✅ Licença salva em: {self.license_file}")
            return True
        except Exception as e:
            print(f"❌ Erro ao salvar licença: {e}")
            return False
    
    def load_license(self):
        """Carrega a licença salva"""
        try:
            if os.path.exists(self.license_file):
                with open(self.license_file, 'r') as f:
                    data = json.load(f)
                print(f"✅ Licença carregada: {data.get('license_key', '')[:8]}...")
                return data
            else:
                print("❌ Arquivo de licença não encontrado")
        except Exception as e:
            print(f"❌ Erro ao carregar licença: {e}")
        return None

    def validate_license(self, license_key=None):
        """VALIDAÇÃO CORRETA - igual ao app Tkinter"""
        try:
            # Se não fornecer license_key, tenta carregar a salva
            if license_key is None:
                saved_license = self.load_license()
                if not saved_license:
                    return False, "Nenhuma licença ativa encontrada"
                license_key = saved_license['license_key']
            
            # Dados para validação - EXATAMENTE IGUAL AO TKINTER
            payload = {
                'license_key': license_key.upper().strip(),
                'motherboard_id': self.get_motherboard_id(),
                'action': 'validate'
            }
            
            print(f"🔍 Validando licença: {license_key[:8]}...")
            
            response = requests.post(
                f"{self.server_url}/api/validate_license",  # ✅ MESMO ENDPOINT
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('valid'):  # ✅ VERIFICA 'valid' E NÃO 'success'
                    print("✅ Licença válida no servidor")
                    # SALVAR A LICENÇA SEMPRE QUE FOR VÁLIDA
                    if not self.load_license():  # Se não tem licença salva, salvar
                        self.save_license(license_key)
                        print("💾 Licença salva após validação")
                    return True, "Licença válida"
                else:
                    print(f"❌ Licença inválida: {data.get('message')}")
                    return False, data.get('message', 'Licença inválida')
            else:
                print(f"❌ Erro servidor: {response.status_code}")
                return False, f"Erro no servidor: {response.status_code}"
                
        except Exception as e:
            print(f"❌ Erro conexão: {str(e)}")
            return False, f"Erro de conexão: {str(e)}"
    
    def activate_license(self, license_key):
        """ATIVAÇÃO CORRETA - igual ao app Tkinter"""
        print(f"🚀 Ativando licença: {license_key[:8]}...")
        success, message = self.validate_license(license_key)  # ✅ USA VALIDAÇÃO
        
        # SE A VALIDAÇÃO FOR BEM SUCEDIDA, SALVAR A LICENÇA
        if success:
            print("💾 Salvando licença após ativação...")
            self.save_license(license_key)
        
        return success, message

    def revoke_license(self):
        """Revoga a licença local"""
        try:
            if os.path.exists(self.license_file):
                os.remove(self.license_file)
                print("🗑️ Licença revogada localmente")
            return True
        except Exception as e:
            print(f"❌ Erro ao revogar licença: {e}")
            return False

# ================== SISTEMA DE VERIFICAÇÃO DE HWID AVANÇADO ==================
class AdvancedLicenseManager:
    def __init__(self):
        self.license_system = LicenseSystem()
        self.hwid = self.license_system.get_motherboard_id()
        self.state_file = os.path.join(os.path.expanduser("~"), "steambox_state.json")
        self.was_activated = self.load_activation_state()

    def load_activation_state(self):
        """Carrega o estado de ativação do arquivo"""
        try:
            saved_license = self.license_system.load_license()
            if saved_license:
                # Verificar se o HWID ainda é o mesmo
                if saved_license.get('motherboard_id') == self.hwid:
                    return True
        except:
            pass
        return False

    def save_activation_state(self):
        """Salva o estado de ativação no arquivo"""
        try:
            state = {
                'was_activated': self.was_activated,
                'hwid': self.hwid,
                'timestamp': time.time(),
                'motherboard_verified': True
            }
            with open(self.state_file, 'w') as f:
                json.dump(state, f)
        except:
            pass

    def clear_activation_state(self):
        """Limpa o estado de ativação"""
        try:
            self.was_activated = False
            self.license_system.revoke_license()
            if os.path.exists(self.state_file):
                os.remove(self.state_file)
        except:
            pass

    def verify_hwid_integrity(self):
        """Verifica se o HWID atual ainda é válido"""
        try:
            current_hwid = self.license_system.get_motherboard_id()
            if current_hwid != self.hwid:
                print(f"HWID mudou: {self.hwid} -> {current_hwid}")
                return False
            return True
        except:
            return True  # Em caso de erro, assume que está OK

    def check_license(self):
        """Verifica a licença no servidor com verificação de integridade"""
        try:
            # Primeiro verificar integridade do HWID
            if not self.verify_hwid_integrity():
                return "hwid_changed"
            
            # Usar o sistema de licença existente
            success, message = self.license_system.validate_license()
            
            if success:
                self.was_activated = True
                self.save_activation_state()
                return "active"
            else:
                # Analisar a mensagem para determinar o tipo de erro
                if "já ativada" in message.lower() or "dispositivos" in message.lower():
                    return "revoked"
                elif "não encontrada" in message.lower():
                    return "invalid"
                else:
                    return "connection_error"
                    
        except Exception as e:
            print(f"Erro ao verificar licença: {e}")
            return "connection_error"

    def handle_license_revocation(self):
        """Executa quando a licença é revogada"""
        try:
            # Remover todos os jogos instalados
            steam_path = self.find_steam()
            if steam_path:
                folders = [
                    os.path.join(steam_path, "config", "stplug-in"),
                    os.path.join(steam_path, "config", "depotcache"),
                ]
                
                for folder in folders:
                    if os.path.exists(folder):
                        shutil.rmtree(folder, ignore_errors=True)
                        
                # Recriar pastas vazias para evitar erros na Steam
                for folder in folders:
                    os.makedirs(folder, exist_ok=True)
            
            # Resetar flag e LIMPAR estado salvo
            self.clear_activation_state()
            return True
            
        except Exception as e:
            print(f"Erro durante revogação: {e}")
            return False

    def find_steam(self):
        """Encontra o caminho da Steam no Windows ou Linux"""
        try:
            if platform.system() == "Windows":
                import winreg
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam")
                    steam_exe, _ = winreg.QueryValueEx(key, "SteamExe")
                    winreg.CloseKey(key)
                    steam_dir = os.path.dirname(steam_exe)
                    if os.path.exists(os.path.join(steam_dir, "steam.exe")):
                        return steam_dir
                except:
                    pass

                common_paths = [
                    os.path.expandvars(r"%ProgramFiles(x86)%\Steam"),
                    os.path.expandvars(r"%ProgramFiles%\Steam"),
                    r"C:\Program Files (x86)\Steam",
                    r"C:\Program Files\Steam",
                ]
                
                for path in common_paths:
                    if os.path.exists(os.path.join(path, "steam.exe")):
                        return path
            else:
                # Caminhos Linux
                linux_paths = [
                    os.path.expanduser("~/.steam/steam"),
                    os.path.expanduser("~/.local/share/Steam"),
                    os.path.expanduser("~/.var/app/com.valvesoftware.Steam/data/Steam"), # Flatpak
                ]
                for path in linux_paths:
                    if os.path.exists(path):
                        return path
                
            return None
        except Exception as e:
            print(f"Erro ao encontrar Steam: {e}")
            return None

    def activate_license(self, license_key):
        """Ativa uma licença usando o sistema existente"""
        return self.license_system.activate_license(license_key)

# ================== SISTEMA DE ÍCONES UNIVERSAL ==================
class IconsFallback:
    HOME = "HOME"
    GAMES = "GAMES"
    PUBLIC = "PUBLIC"
    SETTINGS = "SETTINGS"
    SECURITY = "SECURITY"
    STAR = "STAR"
    REFRESH = "REFRESH"
    DOWNLOAD = "DOWNLOAD"
    DELETE = "DELETE"
    SEARCH = "SEARCH"
    DOWNLOAD_FOR_OFFLINE = "DOWNLOAD_FOR_OFFLINE"
    ERROR = "ERROR"
    UPDATE = "UPDATE"
    SHIELD = "SHIELD"
    WARNING = "WARNING"
    BUG_REPORT = "BUG_REPORT"
    ONLINE_PREDICTION = "ONLINE_PREDICTION"
    MUSIC_NOTE = "MUSIC_NOTE"
    PLAY_ARROW = "PLAY_ARROW"
    PAUSE = "PAUSE"
    SKIP_NEXT = "SKIP_NEXT"
    SKIP_PREVIOUS = "SKIP_PREVIOUS"
    VOLUME_UP = "VOLUME_UP"
    PLAYLIST_PLAY = "PLAYLIST_PLAY"

try:
    ICONS = IconsFallback()
except AttributeError:
    ICONS = IconsFallback()

# ================== SISTEMA DE CARRINHO DE JOGOS ==================
# ================== SISTEMA DE CARRINHO DE JOGOS (MELHORADO) ==================
# ================== SISTEMA DE CARRINHO DE JOGOS (MELHORADO E CORRIGIDO) ==================
class GameCart:
    def __init__(self):
        self.items = []  # Lista de jogos no carrinho
        self.cart_file = os.path.join(os.path.expanduser("~"), "steambox_cart.json")
        self.load_cart()
    
    def add_game(self, appid, name, image=None, dlc_list=None):
        """Adiciona um jogo ao carrinho com suas DLCs"""
        # Verificar se já existe
        for item in self.items:
            if item['appid'] == appid:
                return False, "Jogo já está no carrinho!"
        
        self.items.append({
            'appid': appid,
            'name': name,
            'image': image,  # Foto do jogo em base64
            'dlc_list': dlc_list or [],  # Lista de DLCs disponíveis
            'install_dlcs': False,  # Flag para instalar DLCs
            'added_at': time.time()
        })
        self.save_cart()
        return True, f"{name} adicionado ao carrinho!"
    
    def toggle_dlc_install(self, appid):
        """Alterna se deve instalar DLCs para este jogo"""
        for item in self.items:
            if item['appid'] == appid:
                item['install_dlcs'] = not item['install_dlcs']
                self.save_cart()
                return True, f"DLCs {'serão' if item['install_dlcs'] else 'não serão'} instaladas"
        return False, "Jogo não encontrado"
    
    def remove_game(self, appid):
        """Remove um jogo do carrinho"""
        self.items = [item for item in self.items if item['appid'] != appid]
        self.save_cart()
    
    def clear_cart(self):
        """Limpa o carrinho"""
        self.items = []
        self.save_cart()
    
    def get_total(self):
        """Retorna total de itens no carrinho"""
        return len(self.items)
    
    def get_total_with_dlcs(self):
        """Retorna total de itens considerando DLCs"""
        total = 0
        for item in self.items:
            total += 1  # O jogo principal
            if item['install_dlcs'] and item['dlc_list']:
                total += len(item['dlc_list'])  # Mais as DLCs
        return total
    
    def get_items(self):
        """Retorna lista de itens"""
        return self.items.copy()
    
    def get_install_list(self):
        """Retorna lista de todos os APPIDs a serem instalados (incluindo DLCs)"""
        install_list = []
        for item in self.items:
            install_list.append({
                'appid': item['appid'],
                'name': item['name'],
                'is_dlc': False
            })
            if item['install_dlcs'] and item['dlc_list']:
                for dlc_id in item['dlc_list']:
                    install_list.append({
                        'appid': dlc_id,
                        'name': f"DLC de {item['name']}",
                        'is_dlc': True,
                        'parent_appid': item['appid']
                    })
        return install_list
    
    def save_cart(self):
        """Salva o carrinho em arquivo"""
        try:
            # Não salvar imagens no arquivo para não ocupar muito espaço
            cart_to_save = []
            for item in self.items:
                item_copy = item.copy()
                item_copy['image'] = None  # Remove a imagem para salvar
                cart_to_save.append(item_copy)
            
            with open(self.cart_file, 'w') as f:
                json.dump(cart_to_save, f)
        except:
            pass
    
    def load_cart(self):
        """Carrega o carrinho do arquivo"""
        try:
            if os.path.exists(self.cart_file):
                with open(self.cart_file, 'r') as f:
                    self.items = json.load(f)
                # Garantir que todos os itens tenham os campos necessários
                for item in self.items:
                    if 'install_dlcs' not in item:
                        item['install_dlcs'] = False
                    if 'dlc_list' not in item:
                        item['dlc_list'] = []
        except:
            self.items = []

# ================== GAME MANAGER (STEAM / DOWNLOAD) ==================
class GameManager:
    def __init__(self):
        self.license_manager = AdvancedLicenseManager()
        self.hwid = self.license_manager.hwid
        self.steam_path = self.find_steam()
        self.current_dlc_list = []
        self.failed_appids = set()

    def get_hwid(self):
        return self.license_manager.hwid

    def find_steam(self):
        """Encontra o caminho da Steam (Redireciona para o método correto)"""
        return self.license_manager.find_steam()

    def check_license_status(self):
        """Verifica o status da licença"""
        return self.license_manager.check_license()

    def handle_license_revocation(self):
        """Lida com a revogação da licença"""
        return self.license_manager.handle_license_revocation()

    def extract_appid_from_input(self, user_input):
        """Extrai o APPID do input do usuário"""
        user_input = user_input.strip()
        
        if user_input.isdigit():
            return user_input
        
        patterns = [
            r'store\.steampowered\.com/app/(\d+)',
            r'steamcommunity\.com/app/(\d+)',
            r'steampowered\.com/app/(\d+)',
            r'app/(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input)
            if match:
                return match.group(1)
        
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            return numbers[0]
        
        return None

    def close_steam_safely(self):
        """Fecha Steam de forma multiplataforma"""
        try:
            if platform.system() == "Windows":
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.run(
                    ["taskkill", "/f", "/im", "steam.exe"],
                    timeout=10,
                    capture_output=True,
                    startupinfo=startupinfo,
                )
            else:
                subprocess.run(["pkill", "-f", "steam"], timeout=10, capture_output=True)
            time.sleep(2)
        except Exception:
            pass

    def fetch_game_info(self, user_input: str):
        """Busca nome, imagem, DLCs e disponibilidade no Ryuu."""
        try:
            appid = self.extract_appid_from_input(user_input)
            if not appid:
                raise Exception("Não foi possível encontrar o APPID. Digite um APPID válido ou cole a URL da Steam.")
            
            if appid in self.failed_appids:
                raise Exception(f"APPID {appid} já falhou em tentativas anteriores. Tentando método alternativo.")

            game_name = "Carregando..."
            game_image = None
            dlc_list: list[str] = []
            original_input = user_input

            try:
                steam_api_url = (
                    f"https://store.steampowered.com/api/appdetails?appids={appid}"
                )
                steam_response = requests.get(steam_api_url, timeout=10)
                if steam_response.status_code == 200:
                    data = steam_response.json()
                    if str(appid) in data and data[str(appid)]["success"]:
                        game_data = data[str(appid)]["data"]
                        game_name = game_data.get("name", f"Jogo {appid}")

                        if "dlc" in game_data and game_data["dlc"]:
                            dlc_list = game_data["dlc"]

                        img_url = game_data.get(
                            "header_image",
                            f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg",
                        )
                        img_response = requests.get(img_url, timeout=10)
                        if img_response.status_code == 200:
                            image_data = img_response.content
                            game_image = base64.b64encode(image_data).decode("utf-8")
            except Exception:
                pass

            ryuu_found = False
            ryuu_sources = []

            ryuu_endpoints = [
                f"{OBFUSCATED_URL_1}/secure_download?appid={appid}&auth_code={OBFUSCATED_AUTH}",
                f"{OBFUSCATED_URL_1}/resellerlua/{appid}?auth_code={OBFUSCATED_AUTH}",
                f"{OBFUSCATED_URL_2}/secure_download?appid={appid}",
                f"{OBFUSCATED_URL_2}/api/game/{appid}",
                f"{OBFUSCATED_URL_2}/game/{appid}/manifest",
            ]

            for endpoint in ryuu_endpoints:
                try:
                    response = requests.head(endpoint, timeout=5, allow_redirects=True)
                    if response.status_code == 200:
                        ryuu_found = True
                        ryuu_sources.append(endpoint)
                        break
                except Exception:
                    continue

            if not ryuu_found:
                for endpoint in ryuu_endpoints[:3]:
                    try:
                        response = requests.get(endpoint, timeout=8, stream=True)
                        if response.status_code == 200:
                            content_type = response.headers.get('content-type', '')
                            content_length = response.headers.get('content-length', '0')
                            
                            if 'text/html' not in content_type and int(content_length) > 100:
                                ryuu_found = True
                                ryuu_sources.append(endpoint)
                                break
                    except Exception:
                        continue

            if not game_image:
                try:
                    placeholder = Image.new("RGB", (200, 100), color="#374151")
                    draw = ImageDraw.Draw(placeholder)
                    draw.text((100, 50), f"APPID: {appid}", fill="white", anchor="mm")
                    buffered = BytesIO()
                    placeholder.save(buffered, format="PNG")
                    game_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
                    if game_name == "Carregando...":
                        game_name = f"Jogo {appid}"
                except Exception:
                    game_image = None
                    game_name = f"Jogo {appid}"

            return {
                "appid": appid,
                "name": game_name,
                "image": game_image,
                "dlc_list": dlc_list,
                "available": ryuu_found,
                "original_input": original_input,
                "sources": ryuu_sources
            }
        except Exception as e:
            appid = self.extract_appid_from_input(user_input)
            if appid:
                self.failed_appids.add(appid)
            raise Exception(f"Erro ao buscar jogo: {str(e)}")

    def download_game_files(self, appid, progress_callback=None):
        """Baixa arquivos lua/manifest da API Ryuu (Suporte a ZIP e Novos Endpoints)"""
        try:
            if progress_callback:
                progress_callback(10, "Conectando à API Ryuu...")

            # URLs ATUALIZADAS (Formatadas conforme os dados do Bryan)
            manifest_url = f"{API_MANIFEST}?appid={appid}&auth_code={OBFUSCATED_AUTH}"
            lua_url = f"{API_LUA}?appid={appid}&auth_code={OBFUSCATED_AUTH}"
            
            # Diretórios Steam
            stplugin_dir = os.path.join(self.steam_path, "config", "stplug-in")
            depotcache_dir = os.path.join(self.steam_path, "config", "depotcache")
            os.makedirs(stplugin_dir, exist_ok=True)
            os.makedirs(depotcache_dir, exist_ok=True)

            # 1. BAIXAR LUA
            if progress_callback:
                progress_callback(20, "Baixando Script LUA...")
            
            lua_response = requests.get(lua_url, timeout=30)
            if lua_response.status_code == 200:
                lua_path = os.path.join(stplugin_dir, f"{appid}.lua")
                with open(lua_path, 'wb') as f:
                    f.write(lua_response.content)
                print(f"✅ Arquivo LUA salvo: {lua_path}")
            else:
                print(f"⚠️ Falha ao baixar LUA (Status: {lua_response.status_code})")

            # 2. BAIXAR MANIFESTO (Pode ser um ZIP)
            if progress_callback:
                progress_callback(40, "Baixando Manifesto...")

            manifest_response = requests.get(manifest_url, timeout=30)
            
            if manifest_response.status_code == 200:
                # Verificar se é um ZIP
                content_type = manifest_response.headers.get('Content-Type', '')
                is_zip = 'zip' in content_type or manifest_response.content[:2] == b'PK'
                
                # Nome padrão se não for ZIP
                manifest_filename = f"{appid}.manifest"
                
                if is_zip:
                    if progress_callback:
                        progress_callback(60, "Extraindo manifesto do ZIP...")
                    
                    with zipfile.ZipFile(BytesIO(manifest_response.content)) as z:
                        # Procurar por arquivo .manifest dentro do ZIP
                        manifest_files = [f for f in z.namelist() if f.endswith('.manifest')]
                        if manifest_files:
                            # Preservar o NOME REAL do manifesto (ex: 731_12345.manifest)
                            manifest_filename = manifest_files[0]
                            filepath = os.path.join(depotcache_dir, manifest_filename)
                            with open(filepath, 'wb') as f:
                                f.write(z.read(manifest_filename))
                        else:
                            # Se não achar .manifest, extrair o primeiro arquivo disponível
                            manifest_filename = z.namelist()[0]
                            filepath = os.path.join(depotcache_dir, manifest_filename)
                            with open(filepath, 'wb') as f:
                                f.write(z.read(manifest_filename))
                    print(f"✅ Manifesto extraído e salvo: {manifest_filename}")
                else:
                    # Se não for ZIP, salva normalmente
                    filepath = os.path.join(depotcache_dir, manifest_filename)
                    with open(filepath, 'wb') as f:
                        f.write(manifest_response.content)
                    print(f"✅ Manifesto salvo diretamente: {manifest_filename}")
                
                if progress_callback:
                    progress_callback(90, "Download concluído com sucesso!")
                
                # Sincroniza o LUA com o nome real do manifesto
                return self.create_advanced_fallback_files(appid, progress_callback, manifest_filename=manifest_filename)
            
            # Se falhou, tentar solicitar atualização (Auto-Request)
            print(f"❌ Falha no download do manifesto. Solicitando atualização...")
            try:
                requests.get(f"{API_REQUEST_UPDATE}?appid={appid}&auth_code={OBFUSCATED_AUTH}", timeout=5)
            except:
                pass

            if progress_callback:
                progress_callback(80, "Criando configuração de emergência...")
            return self.create_advanced_fallback_files(appid, progress_callback)

        except Exception as e:
            print(f"❌ Erro ao baixar jogo {appid}: {e}")
            if progress_callback:
                progress_callback(0, f"Erro: {str(e)}")
            return False

    def download_and_install_game(self, appid):
        return self.download_game_files(appid)

    def create_advanced_fallback_files(self, appid, progress_callback=None, manifest_filename=None):
        """Cria arquivos fallback e sincroniza o LUA com o manifesto mais recente"""
        try:
            if progress_callback:
                progress_callback(50, "Sincronizando configuração LUA...")

            stplugin_dir = os.path.join(self.steam_path, "config", "stplug-in")
            depotcache_dir = os.path.join(self.steam_path, "config", "depotcache")
            os.makedirs(stplugin_dir, exist_ok=True)
            os.makedirs(depotcache_dir, exist_ok=True)

            # Usa o nome real do manifesto ou fallback para appid.manifest
            real_manifest_name = manifest_filename if manifest_filename else f"{appid}.manifest"

            lua_content = f"""appid = {appid}
name = "Jogo {appid}"
manifest = "depotcache/{real_manifest_name}"

function Install()
    print("Instalando jogo {appid} via SteamBox...")
    return true
end
"""
            lua_path = os.path.join(stplugin_dir, f"{appid}.lua")
            with open(lua_path, "w", encoding="utf-8") as f:
                f.write(lua_content)

            manifest_content = f"""# Configuração alternativa para AppID: {appid}
AppID: {appid}
Name: Jogo {appid}
Status: Active
"""
            manifest_path = os.path.join(depotcache_dir, f"{appid}.manifest")
            with open(manifest_path, "w", encoding="utf-8") as f:
                f.write(manifest_content)

            if progress_callback:
                progress_callback(100, "Configuração alternativa criada!")
            return True
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"Erro na configuração: {str(e)}")
            return False

    def install_single_game(
        self, appid, game_name, include_dlcs=False, dlc_list=None, progress_callback=None
    ):
        if dlc_list is None:
            dlc_list = []

        if not self.steam_path:
            raise Exception("Steam não encontrada! Instale a Steam primeiro.")

        try:
            if progress_callback:
                progress_callback(0, f"Iniciando instalação de {game_name}...")

            if progress_callback:
                progress_callback(10, "Fechando Steam...")
            self.close_steam_safely()

            if progress_callback:
                progress_callback(20, "Instalando jogo na sua conta Steam...")
            success = self.download_game_files(appid, progress_callback)
            if not success:
                raise Exception("Não foi possível baixar o jogo principal.")

            if include_dlcs and dlc_list:
                total_dlcs = len(dlc_list)
                for index, dlc_id in enumerate(dlc_list):
                    progress = 80 + int((index / total_dlcs) * 15)
                    if progress_callback:
                        progress_callback(
                            progress, f"Instalando DLC {index+1}/{total_dlcs}..."
                        )
                    try:
                        self.download_game_files(dlc_id)
                    except Exception:
                        if progress_callback:
                            progress_callback(
                                progress, f"Erro na DLC {dlc_id}, continuando..."
                            )

            if progress_callback:
                progress_callback(95, "Abrindo Steam com o jogo já instalado...")

            steam_exe = os.path.join(self.steam_path, "steam.exe")
            if os.path.exists(steam_exe):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.Popen([steam_exe], startupinfo=startupinfo)
                if progress_callback:
                    progress_callback(100, "Jogo instalado! Steam aberta.")
            else:
                if progress_callback:
                    progress_callback(100, "Jogo instalado! Não encontrei steam.exe.")

            return True
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"Erro: {str(e)}")
            raise Exception(f"Falha na instalação: {str(e)}")

    def remove_single_game(self, appid, game_name, progress_callback=None):
        if not self.steam_path:
            raise Exception("Steam não encontrada!")

        try:
            if progress_callback:
                progress_callback(10, "Fechando Steam...")
            self.close_steam_safely()

            if progress_callback:
                progress_callback(30, "Removendo arquivos do jogo...")

            stplugin_dir = os.path.join(self.steam_path, "config", "stplug-in")
            depotcache_dir = os.path.join(self.steam_path, "config", "depotcache")

            lua_file = os.path.join(stplugin_dir, f"{appid}.lua")
            manifest_file = os.path.join(depotcache_dir, f"{appid}.manifest")

            removed_files = []
            if os.path.exists(lua_file):
                os.remove(lua_file)
                removed_files.append("lua")
            if progress_callback:
                progress_callback(60, "Arquivo Lua removido...")
                
            if os.path.exists(manifest_file):
                os.remove(manifest_file)
                removed_files.append("manifest")
            if progress_callback:
                progress_callback(80, "Manifest removido...")

            if progress_callback:
                progress_callback(90, "Abrindo Steam sem esse jogo...")

            steam_exe = os.path.join(self.steam_path, "steam.exe")
            if os.path.exists(steam_exe):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.Popen([steam_exe], startupinfo=startupinfo)
                if progress_callback:
                    progress_callback(100, "Jogo removido! Steam aberta.")
            else:
                if progress_callback:
                    progress_callback(100, "Jogo removido! Não encontrei steam.exe.")

            return True, removed_files
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"Erro: {str(e)}")
            raise Exception(f"Falha ao remover jogo: {str(e)}")

    # ================== FUNÇÃO PARA INSTALAR O PACK DE JOGOS ==================
    def install_game_pack(self, progress_callback=None):
        """Instala o pack de jogos usando o arquivo Steambox.zip"""
        if not self.steam_path:
            raise Exception("Steam não encontrada! Instale a Steam primeiro.")

        try:
            if progress_callback:
                progress_callback(5, "Verificando arquivo local...")

            # Lista de possíveis caminhos para o Steambox.zip
            possible_zip_paths = [
                # Caminho atual
                os.path.join(os.path.abspath("."), "Steambox.zip"),
                # Caminho específico que você mencionou
                r"D:\Korea Store\Kenix app\Aplicativo venda\Steambox.zip",
                # Pasta do executável
                os.path.join(os.path.dirname(sys.executable), "Steambox.zip") if getattr(sys, 'frozen', False) else None,
                # Pasta temporária
                os.path.join(tempfile.gettempdir(), "Steambox.zip"),
            ]
            
            # Filtrar None values
            possible_zip_paths = [p for p in possible_zip_paths if p is not None]
            
            steambox_zip_path = None
            for path in possible_zip_paths:
                if os.path.exists(path):
                    steambox_zip_path = path
                    print(f"✅ Steambox.zip encontrado em: {path}")
                    break
            
            if not steambox_zip_path:
                raise Exception(
                    "Arquivo Steambox.zip não encontrado!\n\n"
                    "Procurei nos seguintes locais:\n"
                    + "\n".join([f"• {p}" for p in possible_zip_paths if p])
                )

            if progress_callback:
                progress_callback(15, "Fechando Steam...")
            self.close_steam_safely()

            if progress_callback:
                progress_callback(25, "Preparando extração para pasta config...")

            config_path = os.path.join(self.steam_path, "config")
            
            if not os.path.exists(config_path):
                os.makedirs(config_path, exist_ok=True)

            if progress_callback:
                progress_callback(40, "Verificando tamanho do arquivo...")
            
            # Verificar tamanho do arquivo
            file_size = os.path.getsize(steambox_zip_path)
            file_size_mb = file_size / (1024 * 1024)
            
            if progress_callback:
                progress_callback(50, f"Extraindo {file_size_mb:.1f} MB de jogos...")

            with zipfile.ZipFile(steambox_zip_path, "r") as zip_ref:
                file_list = zip_ref.namelist()
                total_files = len(file_list)
                
                # Estimar número de jogos (assumindo que cada arquivo .lua é um jogo)
                game_count = sum(1 for f in file_list if f.endswith('.lua'))
                
                if progress_callback:
                    progress_callback(60, f"Extraindo aproximadamente {game_count} jogos...")
                
                for i, file in enumerate(file_list):
                    try:
                        zip_ref.extract(file, config_path)
                        
                        # Atualizar progresso a cada 50 arquivos para não sobrecarregar
                        if i % 50 == 0:
                            progress = 60 + int((i / total_files) * 35)
                            if progress_callback:
                                progress_callback(
                                    progress, 
                                    f"Extraindo arquivo {i+1}/{total_files}...\n"
                                    f"Jogos processados: {min(game_count, i//2)}"
                                )
                    except Exception as e:
                        print(f"Erro ao extrair {file}: {e}")
                        continue

            if progress_callback:
                progress_callback(95, "Abrindo Steam com o pack instalado...")

            steam_exe = os.path.join(self.steam_path, "steam.exe")
            if os.path.exists(steam_exe):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.Popen([steam_exe], startupinfo=startupinfo)
                if progress_callback:
                    progress_callback(100, f"✅ {game_count} jogos instalados! Steam aberta.")
            else:
                if progress_callback:
                    progress_callback(100, f"✅ {game_count} jogos instalados!")

            return True
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"Erro: {str(e)}")
            raise Exception(f"Falha na instalação do pack: {str(e)}")

    def uninstall_all_games(self, progress_callback=None):
        if not self.steam_path:
            raise Exception("Steam não encontrada!")

        try:
            if progress_callback:
                progress_callback(10, "Fechando Steam...")
            self.close_steam_safely()

            if progress_callback:
                progress_callback(30, "Removendo todos os jogos...")

            folders = [
                os.path.join(self.steam_path, "config", "stplug-in"),
                os.path.join(self.steam_path, "config", "depotcache"),
            ]

            removed_count = 0
            for i, folder in enumerate(folders):
                if os.path.exists(folder):
                    # Contar arquivos antes de remover
                    for _, _, files in os.walk(folder):
                        removed_count += len(files)
                    shutil.rmtree(folder, ignore_errors=True)
                    os.makedirs(folder, exist_ok=True)
                    
                progress = 30 + int((i / len(folders)) * 50)
                if progress_callback:
                    progress_callback(progress, f"Limpando pasta {i+1}/{len(folders)}...")

            if progress_callback:
                progress_callback(90, "Abrindo Steam limpa...")

            steam_exe = os.path.join(self.steam_path, "steam.exe")
            if os.path.exists(steam_exe):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.Popen([steam_exe], startupinfo=startupinfo)
                if progress_callback:
                    progress_callback(
                        100,
                        f"Todos os jogos removidos! ({removed_count} arquivos) Steam aberta.",
                    )
            else:
                if progress_callback:
                    progress_callback(
                        100, f"Jogos removidos ({removed_count} arquivos)!"
                    )

            return True, removed_count
        except Exception as e:
            if progress_callback:
                progress_callback(0, f"Erro: {str(e)}")
            raise Exception(f"Falha ao remover jogos: {str(e)}")

# ================== APP FLET COM VERIFICAÇÃO DE HWID AVANÇADA ==================
class App:
    def __init__(self):
        self.page: ft.Page | None = None
        self.current_page = "activation"  # Começa na tela de ativação
        self.game_manager = GameManager()
        self.license_valid = False  # Flag para verificar se a licença é válida
        self.cart = GameCart()  # Sistema de carrinho

        self.search_field: ft.TextField | None = None
        self.game_info_container: ft.Container | None = None
        self.license_entry: ft.TextField | None = None
        self.logo_base64 = None  # Cache da logo
        self.background_base64 = None  # Cache do background
        self.overlay_base64 = None  # Cache da overlay
        self.cart_badge: ft.Badge | None = None  # Badge do carrinho
        self.cart_view_visible = False  # Controle da visualização do carrinho

        self.progress_dialog: ft.AlertDialog | None = None
        self.progress_text: ft.Text | None = None
        self.progress_bar: ft.ProgressBar | None = None
        self.progress_status: ft.Text | None = None
        self.progress_details: ft.Text | None = None

        # Carregar background
        self.load_background()

    # ---------- CARREGAR BACKGROUND ----------
    def load_background(self):
        """Carrega ou cria o background da janela"""
        if self.background_base64:
            return self.background_base64
        
        # Criar background gradiente
        self.background_base64 = create_gradient_background(1920, 1080, "#100025", "#34A8BD")
        return self.background_base64

    def load_overlay(self):
        """Carrega a overlay escura"""
        if self.overlay_base64:
            return self.overlay_base64
        
        self.overlay_base64 = create_dark_overlay()
        return self.overlay_base64

    # ---------- CARREGAR LOGO ----------
    def load_logo(self):
        """Carrega a logo.png da pasta usando busca em múltiplos caminhos"""
        if self.logo_base64:
            return self.logo_base64
            
        # Usar a função find_logo que busca em múltiplos locais
        self.logo_base64 = find_logo()
        return self.logo_base64

    # ---------- EXECUTAR NA UI ----------
    def run_on_ui(self, fn):
        if not self.page:
            return
        try:
            self.page.run_task(fn)
        except AttributeError:
            try:
                fn()
                self.page.update()
            except Exception:
                pass

    # ---------- ATUALIZAR BADGE DO CARRINHO ----------
    def update_cart_badge(self):
        """Atualiza o número no badge do carrinho"""
        if self.cart_badge and self.page:
            total = self.cart.get_total()
            self.cart_badge.text = str(total) if total > 0 else ""
            self.page.update()

    # ---------- CRIAR VISUALIZAÇÃO DO CARRINHO ----------
    # ---------- CRIAR VISUALIZAÇÃO DO CARRINHO (MELHORADA) ----------
    # ---------- CRIAR VISUALIZAÇÃO DO CARRINHO (MELHORADA E CORRIGIDA) ----------
    def create_cart_view(self):
        """Cria a visualização do carrinho de compras com fotos e DLCs"""
        items = self.cart.get_items()
        
        if not items:
            return ft.Container(
                visible=self.cart_view_visible,
                padding=20,
                bgcolor=ft.colors.with_opacity(0.1, "#1a1a1a"),
                border=ft.border.all(1, ft.colors.with_opacity(0.1, "white")),
                border_radius=10,
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.SHOPPING_CART, size=50, color="#9ca3af"),
                        ft.Container(height=10),
                        ft.Text(
                            "Seu carrinho está vazio",
                            size=18,
                            weight="bold",
                            color="white",
                        ),
                        ft.Text(
                            "Adicione jogos para instalar todos de uma vez",
                            size=14,
                            color="#9ca3af",
                        ),
                    ],
                    horizontal_alignment="center",
                ),
            )
        
        # Criar lista de itens do carrinho
        cart_items = []
        for item in items:
            # Miniatura do jogo
            if item['image']:
                game_thumbnail = ft.Container(
                    width=50,
                    height=50,
                    border_radius=5,
                    content=ft.Image(
                        src=item['image'],
                        fit="cover",
                        error_content=ft.Container(
                            width=50,
                            height=50,
                            bgcolor=ft.colors.with_opacity(0.2, "#ff6b00"),
                            content=ft.Text(
                                item['appid'][:4],
                                color="white",
                                size=10,
                                text_align="center",
                            ),
                        ),
                    )
                )
            else:
                game_thumbnail = ft.Container(
                    width=50,
                    height=50,
                    bgcolor=ft.colors.with_opacity(0.2, "#ff6b00"),
                    border_radius=5,
                    content=ft.Text(
                        item['appid'][:4],
                        color="white",
                        size=10,
                        text_align="center",
                    ),
                )
            
            # Informações do jogo
            game_info = ft.Column(
                [
                    ft.Text(
                        item['name'][:40] + "..." if len(item['name']) > 40 else item['name'],
                        size=14,
                        weight="bold",
                        color="white",
                    ),
                    ft.Text(
                        f"APPID: {item['appid']}",
                        size=10,
                        color="#9ca3af",
                    ),
                ],
                spacing=2,
                expand=True,
            )
            
            # Opções de DLC (se houver)
            dlc_options = []
            if item['dlc_list']:
                dlc_count = len(item['dlc_list'])
                dlc_options.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Checkbox(
                                    value=item['install_dlcs'],
                                    on_change=lambda e, a=item['appid']: self.toggle_cart_dlc(a),
                                    active_color="#ff6b00",
                                    check_color="white",
                                ),
                                ft.Text(
                                    f"Instalar {dlc_count} DLC{'s' if dlc_count > 1 else ''}",
                                    size=12,
                                    color="#a6b8ff" if item['install_dlcs'] else "#9ca3af",
                                ),
                                ft.Icon(
                                    ft.icons.INFO_OUTLINE,  # CORRIGIDO: era ft.books.INFO_OUTLINE
                                    size=14,
                                    color="#9ca3af",
                                ),
                            ],
                            spacing=5,
                        ),
                        padding=ft.padding.only(left=60, top=5),
                    )
                )
            
            # Botão remover
            remove_button = ft.IconButton(
                icon=ft.icons.REMOVE_CIRCLE_OUTLINE,
                icon_color="#ef4444",
                icon_size=20,
                tooltip="Remover do carrinho",
                on_click=lambda e, a=item['appid']: self.remove_from_cart(a),
            )
            
            # Montar item completo
            cart_items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [game_thumbnail, game_info, remove_button],
                                alignment=ft.MainAxisAlignment.START,
                                vertical_alignment="center",
                            ),
                            *dlc_options,
                        ],
                        spacing=5,
                    ),
                    padding=10,
                    border=ft.border.all(1, ft.colors.with_opacity(0.1, "white")),
                    border_radius=5,
                    margin=ft.margin.only(bottom=5),
                )
            )
        
        # Calcular totais
        total_jogos = len(items)
        total_com_dlcs = self.cart.get_total_with_dlcs()
        
        # Adicionar botões de ação
        cart_items.extend([
            ft.Divider(height=20, color=ft.colors.with_opacity(0.2, "white")),
            ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(
                                    "Resumo da Instalação:",
                                    size=16,
                                    weight="bold",
                                    color="white",
                                ),
                            ],
                        ),
                        ft.Row(
                            [
                                ft.Text(
                                    f"• Jogos principais: {total_jogos}",
                                    size=14,
                                    color="#9ca3af",
                                ),
                            ],
                        ),
                        ft.Row(
                            [
                                ft.Text(
                                    f"• Total com DLCs: {total_com_dlcs} itens",
                                    size=14,
                                    color="#a6b8ff" if total_com_dlcs > total_jogos else "#9ca3af",
                                ),
                            ],
                        ),
                        ft.Container(height=10),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "Limpar Carrinho",
                                    icon=ft.icons.DELETE_SWEEP,
                                    style=ft.ButtonStyle(
                                        color="white",
                                        bgcolor={
                                            ft.MaterialState.DEFAULT: "#6b7280",
                                            ft.MaterialState.HOVERED: "#4b5563",
                                        },
                                    ),
                                    on_click=self.clear_cart,
                                ),
                                ft.Container(width=10),
                                ft.ElevatedButton(
                                    f"Instalar {total_com_dlcs} Item(ns)",
                                    icon=ft.icons.DOWNLOAD_DONE,
                                    style=ft.ButtonStyle(
                                        color="white",
                                        bgcolor={
                                            ft.MaterialState.DEFAULT: "#22c55e",
                                            ft.MaterialState.HOVERED: "#16a34a",
                                        },
                                    ),
                                    on_click=self.install_all_from_cart,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.END,
                        ),
                    ],
                    spacing=5,
                ),
                padding=10,
            ),
        ])
        
        return ft.Container(
            visible=self.cart_view_visible,
            padding=20,
            bgcolor=ft.colors.with_opacity(0.1, "#1a1a1a"),
            border=ft.border.all(1, ft.colors.with_opacity(0.1, "white")),
            border_radius=10,
            content=ft.Column(cart_items, scroll=ft.ScrollMode.AUTO, height=400),
        )
# ---------- ALTERNAR DLC NO CARRINHO ----------
    # ---------- ALTERNAR DLC NO CARRINHO ----------
    def toggle_cart_dlc(self, appid):
        """Alterna instalação de DLCs para um jogo no carrinho"""
        success, message = self.cart.toggle_dlc_install(appid)
        if success:
            self.update_cart_badge()
            # Forçar atualização da UI
            if self.page:
                self.page.run_task(self.update_content)
            self.show_snackbar(message)

    # ---------- ALTERNAR VISUALIZAÇÃO DO CARRINHO ----------
    def toggle_cart_view(self, e):
        """Alterna entre mostrar/esconder o carrinho"""
        self.cart_view_visible = not self.cart_view_visible
        self.update_content()

    # ---------- ADICIONAR AO CARRINHO (COM DLCs) ----------
    # ---------- ADICIONAR AO CARRINHO (COM DLCs) ----------
    def add_to_cart(self, appid, name, image=None, dlc_list=None):
        """Adiciona um jogo ao carrinho com suas DLCs"""
        success, message = self.cart.add_game(appid, name, image, dlc_list)
        self.update_cart_badge()
        
        if success:
            if dlc_list and len(dlc_list) > 0:
                message += f" (+{len(dlc_list)} DLCs disponíveis)"
            self.show_success_notification("✅ Adicionado ao carrinho", message)
        else:
            self.show_warning_notification("⚠️ Atenção", message)

    # ---------- REMOVER DO CARRINHO ----------
    def remove_from_cart(self, appid):
        """Remove um jogo do carrinho"""
        self.cart.remove_game(appid)
        self.update_cart_badge()
        self.update_content()
        self.show_snackbar("Jogo removido do carrinho")

    # ---------- LIMPAR CARRINHO ----------
    def clear_cart(self, e):
        """Limpa todo o carrinho"""
        self.cart.clear_cart()
        self.update_cart_badge()
        self.update_content()
        self.show_snackbar("Carrinho limpo")

    # ---------- INSTALAR TODOS DO CARRINHO (COM DLCs) ----------
    def install_all_from_cart(self, e):
        """Instala todos os jogos do carrinho, incluindo DLCs selecionadas"""
        install_list = self.cart.get_install_list()
        if not install_list:
            self.show_warning_notification("Carrinho vazio", "Adicione jogos ao carrinho primeiro")
            return
        
        total = len(install_list)
        jogos_principais = sum(1 for item in install_list if not item['is_dlc'])
        dlcs = sum(1 for item in install_list if item['is_dlc'])
        
        self.show_progress_dialog(
            f"Instalando {total} item(ns)",
            f"{jogos_principais} jogo(s) principal(is) e {dlcs} DLC(s)"
        )
        
        def worker():
            success_count = 0
            fail_count = 0
            installed_games = []
            installed_dlcs = []
            
            for i, item in enumerate(install_list):
                try:
                    def progress_cb(progress, status):
                        item_type = "DLC" if item['is_dlc'] else "Jogo"
                        self.update_progress_dialog(
                            int((i / total) * 100 + (progress / total)),
                            f"Instalando {item_type}: {item['name']} ({i+1}/{total})",
                            f"Progresso: {progress}%"
                        )
                    
                    self.game_manager.install_single_game(
                        item['appid'], item['name'], False, [], progress_cb
                    )
                    
                    if item['is_dlc']:
                        installed_dlcs.append(item['name'])
                    else:
                        installed_games.append(item['name'])
                    
                    success_count += 1
                except Exception as ex:
                    print(f"Erro ao instalar {item['name']}: {ex}")
                    fail_count += 1
            
            self.close_progress_dialog()
            
            # Limpar carrinho após instalação bem-sucedida
            self.cart.clear_cart()
            self.update_cart_badge()
            self.cart_view_visible = False
            self.update_content()
            
            # Mostrar resumo detalhado
            resumo = f"✅ Jogos: {len(installed_games)}\n"
            if installed_dlcs:
                resumo += f"🎮 DLCs: {len(installed_dlcs)}"
            
            self.show_success_notification(
                "✅ Instalação em massa concluída",
                f"{resumo}\n❌ Falhas: {fail_count}"
            )
        
        threading.Thread(target=worker, daemon=True).start()

    # ---------- NAVEGAÇÃO COM VERIFICAÇÃO DE LICENÇA ----------
    def change_page(self, e, page_name):
        # Verificar se a licença é válida antes de permitir navegação
        if not self.license_valid and page_name != "activation":
            self.show_license_required_dialog()
            return
            
        self.current_page = page_name
        self.update_content()

    def show_license_required_dialog(self):
        """Mostra diálogo quando tentam acessar sem licença"""
        content = ft.Column([
            ft.Icon(ft.icons.WARNING_AMBER, color="#ef4444", size=50),
            ft.Text("LICENÇA REQUERIDA", size=20, weight="bold", color="#ef4444"),
            ft.Container(height=10),
            ft.Text(
                "Você não tem licença para acessar o aplicativo.\n\n"
                "É necessário ativar uma licença válida para usar todas as funcionalidades.",
                size=16,
                color="white",
                text_align="center"
            ),
            ft.Container(height=20),
            ft.ElevatedButton(
                "Ativar Licença",
                icon=ft.icons.VERIFIED,
                style=ft.ButtonStyle(color="white", bgcolor="#ff6b00"),
                on_click=lambda e: self.change_page(e, "activation")
            )
        ])
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Acesso Restrito"),
            content=content,
            actions_alignment="center"
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def update_content(self):
        if not self.page:
            return
            
        self.page.controls.clear()

        # Carregar background
        background = self.load_background()
        overlay = self.load_overlay()

        if self.current_page == "activation":
            # Container principal com background
            main_content = ft.Container(
                expand=True,
                image_src=background,
                image_fit="cover",
                content=ft.Container(
                    expand=True,
                    image_src=overlay if overlay else None,
                    image_fit="cover",
                    content=self.create_activation_content(),
                ),
            )
            self.page.add(main_content)
        else:
            # Verificar licença antes de mostrar conteúdo principal
            if not self.license_valid:
                main_content = ft.Container(
                    expand=True,
                    image_src=background,
                    image_fit="cover",
                    content=ft.Container(
                        expand=True,
                        image_src=overlay if overlay else None,
                        image_fit="cover",
                        content=self.create_activation_content(),
                    ),
                )
                self.page.add(main_content)
            else:
                sidebar = self.create_sidebar()
                
                if self.current_page == "jogos":
                    main_content = self.create_games_content()
                else:
                    main_content = self.create_games_content()

                # Row com sidebar e conteúdo principal com background
                self.page.add(
                    ft.Container(
                        expand=True,
                        image_src=background,
                        image_fit="cover",
                        content=ft.Container(
                            expand=True,
                            image_src=overlay if overlay else None,
                            image_fit="cover",
                            content=ft.Row(
                                [sidebar, ft.VerticalDivider(width=1, color="#444444"), main_content],
                                expand=True
                            ),
                        ),
                    )
                )
        
        self.page.update()

    # ---------- FUNÇÃO PARA ABRIR SITE ----------
    def open_website(self, e):
        """Abre o site da Steambox no navegador padrão"""
        import webbrowser
        website_url = "https://steambox.store/?utm_term=1771350888093_17713510862035&utm_content=direto&utm_source=direto"
        webbrowser.open(website_url)
        self.show_snackbar(f"Abrindo {website_url}...")

    # ---------- TELA DE ATIVAÇÃO ----------
    def create_activation_content(self):
        """Cria a tela de ativação com HWID e logo"""
        hwid = self.game_manager.get_hwid()
        logo_base64 = self.load_logo()
        
        # Campo de entrada da licença
        self.license_entry = ft.TextField(
            label="Chave de Licença",
            hint_text="Digite sua chave de licença...",
            border_color="#ff6b00",
            focused_border_color="#ff6b00",
            color="white",
            bgcolor="#1a1a1a",
            width=400,
            text_size=14,
            password=True,
            can_reveal_password=True,
            text_align="center"
        )

        return ft.Container(
            expand=True,
            padding=1,
            content=ft.Column(
                [
                    # Logo
                    ft.Container(
                        content=ft.Container(
                            content=ft.Image(
                                src=logo_base64 if logo_base64 else resource_path("logo.png"),
                                width=280,
                                height=280,
                                fit="contain",
                            ) if (logo_base64 or os.path.exists(resource_path("logo.png"))) else ft.Container(
                                width=150,
                                height=150,
                                bgcolor="#ff6b00",
                                border_radius=75,
                                content=ft.Icon(ft.icons.STORE, size=80, color="white"),
                            ),
                        ),
                        alignment="center",
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Título
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "SteamBox",
                                size=40,
                                weight="bold",
                                color="white",
                                text_align="center",
                            ),
                            ft.Text(
                                "O melhor aplicativo para jogos",
                                size=14,
                                color="#ff6b00",
                                weight="bold",
                                text_align="center"
                            ),
                        ],
                        horizontal_alignment="center"),
                        alignment="center",
                        margin=ft.margin.only(bottom=10)
                    ),
                    
                    # Subtítulo
                    ft.Container(
                        content=ft.Text(
                            "27 MIL JOGOS NA SUA STEAM - ATIVE SUA LICENÇA E APROVEITE!",
                            size=13,
                            weight="bold",
                            color="#cccccc",
                            text_align="center"
                        ),
                        alignment="center",
                        margin=ft.margin.only(bottom=40)
                    ),
                    
                    # HWID Display
                    ft.Container(
                        content=ft.Column([
                            ft.Container(height=10),
                            ft.Container(
                                content=ft.Row([
                                    ft.Text(
                                        hwid,
                                        size=14,
                                        weight="bold",
                                        color="white",
                                        selectable=True,
                                        text_align="center"
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.COPY,
                                        icon_color="white",
                                        on_click=lambda e: self.copy_hwid(hwid),
                                        tooltip="Copiar HWID"
                                    )
                                ],
                                alignment="center"),
                                padding=5,
                                bgcolor=ft.colors.with_opacity(0.2, "#1d4ed8"),
                                border=ft.border.all(2, "#3b82f6"),
                                border_radius=10,
                                width=450,
                            ),
                            ft.Container(height=10),
                            ft.Text(
                                "Copie o HWID acima e envie para o vendedor",
                                size=12,
                                color="#9ca3af",
                                text_align="center"
                            )
                        ],
                        horizontal_alignment="center"),
                        alignment="center",
                        margin=ft.margin.only(bottom=30)
                    ),
                    
                    # Campo de Licença
                    ft.Container(
                        content=ft.Column([
                            ft.Text("DIGITE SUA CHAVE DE LICENÇA", size=16, weight="bold", color="white", text_align="center"),
                            ft.Container(height=10),
                            self.license_entry,
                        ],
                        horizontal_alignment="center"),
                        alignment="center",
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Botão de Ativação
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Verificar e Ativar Licença",
                            icon=ft.icons.VERIFIED,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor={
                                    ft.MaterialState.DEFAULT: "#25c279",
                                    ft.MaterialState.HOVERED: "#1e9b60",
                                },
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation={
                                    ft.MaterialState.DEFAULT: 5,
                                    ft.MaterialState.HOVERED: 8,
                                },
                            ),
                            on_click=self.activate_license
                        ),
                        alignment="center",
                        margin=ft.margin.only(bottom=10)
                    ),
                    
                    # Botão de Verificação de Licença Salva
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Verificar Licença Salva",
                            icon=ft.icons.SEARCH,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor={
                                    ft.MaterialState.DEFAULT: "#3b82f6",
                                    ft.MaterialState.HOVERED: "#2563eb",
                                },
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation={
                                    ft.MaterialState.DEFAULT: 5,
                                    ft.MaterialState.HOVERED: 8,
                                },
                            ),
                            on_click=self.check_license
                        ),
                        alignment="center",
                        margin=ft.margin.only(bottom=10)
                    ),
                    
                    # Botão para Comprar Licença
                    ft.Container(
                        content=ft.ElevatedButton(
                            "Comprar Licença na steambox.store",
                            icon=ft.icons.SHOPPING_CART,
                            style=ft.ButtonStyle(
                                color="white",
                                bgcolor={
                                    ft.MaterialState.DEFAULT: "#ff6b00",
                                    ft.MaterialState.HOVERED: "#e05a00",
                                },
                                padding=20,
                                shape=ft.RoundedRectangleBorder(radius=10),
                                elevation={
                                    ft.MaterialState.DEFAULT: 5,
                                    ft.MaterialState.HOVERED: 8,
                                },
                            ),
                            on_click=self.open_website
                        ),
                        alignment="center",
                        margin=ft.margin.only(bottom=20)
                    ),
                    
                    # Texto adicional
                    ft.Container(
                        content=ft.Text(
                            "Compre já a sua licença na steambox.store",
                            size=12,
                            color="#9ca3af",
                            text_align="center",
                            italic=True
                        ),
                        alignment="center",
                    )
                ],
                horizontal_alignment="center",
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
        )

    def copy_hwid(self, hwid):
        """Copia o HWID para a área de transferência"""
        self.page.set_clipboard(hwid)
        self.show_snackbar("HWID copiado para a área de transferência!")

    def activate_license(self, e=None):
        """Ativa uma licença - VERSÃO CORRIGIDA"""
        license_key = self.license_entry.value.strip() if self.license_entry else ""
        
        if not license_key:
            self.show_error_notification("Erro", "Digite uma chave de licença!")
            return
        
        self.show_progress_dialog("Ativando Licença", "Validando chave...")
        
        def worker():
            try:
                success, message = self.game_manager.license_manager.activate_license(license_key)
                
                if success:
                    self.license_valid = True
                    self.close_progress_dialog()
                    self.show_success_notification(
                        "✅ Licença Ativada com Sucesso",
                        message
                    )
                    # Mudar para a tela principal
                    self.current_page = "jogos"
                    self.run_on_ui(self.update_content)
                else:
                    self.license_valid = False
                    self.close_progress_dialog()
                    
                    if "já ativada" in message.lower() or "dispositivos" in message.lower():
                        self.show_error_notification(
                            "🚫 Licença em Uso", 
                            "Esta licença já está ativa em outro computador.\n\n"
                            "Cada licença funciona em apenas UM PC por vez.\n"
                            "Se você trocou de computador, entre em contato conosco."
                        )
                    else:
                        self.show_error_notification("❌ Falha na Ativação", message)
                        
            except Exception as e:
                self.license_valid = False
                self.close_progress_dialog()
                self.show_error_notification(
                    "❌ Erro no Sistema",
                    f"Erro ao ativar licença: {str(e)}"
                )
        
        threading.Thread(target=worker, daemon=True).start()

    def check_license(self, e=None):
        """Verifica a licença - VERSÃO CORRIGIDA"""
        self.show_progress_dialog("Verificando Licença", "Conectando ao servidor...")
        
        def worker():
            try:
                status = self.game_manager.check_license_status()
                
                if status == "active":
                    self.license_valid = True
                    self.close_progress_dialog()
                    self.show_success_notification(
                        "✅ Licença Ativa",
                        "Licença validada! Acessando a loja premium..."
                    )
                    self.current_page = "jogos"
                    self.run_on_ui(self.update_content)
                    
                elif status == "revoked":
                    self.license_valid = False
                    self.close_progress_dialog()
                    self.show_error_notification(
                        "🚫 Licença em Uso em Outro PC",
                        "Esta licença já está ativa em outro computador.\n\n"
                        "Cada licença funciona em apenas UM PC por vez."
                    )
                    
                elif status == "invalid":
                    self.license_valid = False
                    self.close_progress_dialog()
                    self.show_error_notification(
                        "❌ Licença Inválida",
                        "Licença não encontrada ou HWID não autorizado."
                    )
                    
                else:
                    self.license_valid = False
                    self.close_progress_dialog()
                    self.show_error_notification(
                        "❌ Erro de Conexão",
                        "Não foi possível conectar ao servidor.\n"
                        "Verifique sua internet e tente novamente."
                    )
                    
            except Exception as e:
                self.license_valid = False
                self.close_progress_dialog()
                self.show_error_notification(
                    "❌ Erro no Sistema",
                    f"Erro ao verificar licença: {str(e)}"
                )
        
        threading.Thread(target=worker, daemon=True).start()

    def show_revocation_dialog(self):
        """Mostra diálogo quando a licença é revogada"""
        content = ft.Column([
            ft.Icon(ft.icons.WARNING_AMBER, color="#ef4444", size=50),
            ft.Text("LICENÇA CANCELADA", size=20, weight="bold", color="#ef4444"),
            ft.Container(height=10),
            ft.Text(
                "Sua licença foi cancelada pelo administrador.\n"
                "Todos os jogos serão removidos do sistema.",
                size=16,
                color="white",
                text_align="center"
            ),
            ft.Container(height=20),
            ft.ProgressRing(color="#ef4444"),
            ft.Container(height=10),
            ft.Text("Removendo jogos e redefinindo sistema...", size=14, color="#9ca3af")
        ])
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Aviso do Sistema de Segurança"),
            content=content,
            actions=[]
        )
        
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
        
        def process_revocation():
            success = self.game_manager.handle_license_revocation()
            self.run_on_ui(lambda: self.finish_revocation(success))
        
        threading.Thread(target=process_revocation, daemon=True).start()

    def finish_revocation(self, success):
        """Finaliza o processo de revogação"""
        if self.page.dialog:
            self.page.dialog.open = False
        
        if success:
            self.show_error_notification(
                "🔧 Sistema Reinicializado",
                "Todos os jogos foram removidos devido ao cancelamento da licença.\n"
                "Entre em contato com o suporte para mais informações."
            )
        else:
            self.show_error_notification(
                "❌ Erro na Reinicialização",
                "Ocorreu um erro durante la remoção dos jogos.\n"
                "Recomendamos reinstalar a Steam manualmente."
            )
        
        self.current_page = "activation"
        self.update_content()

    # ---------- SIDEBAR (após ativação) ----------
    def create_sidebar(self):
        logo_base64 = self.load_logo()

        return ft.Container(
            width=220,
            padding=20,
            bgcolor=ft.colors.with_opacity(0.9, "#161515"),
            border=ft.border.all(1, ft.colors.with_opacity(0.1, "white")),
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Container(
                                    content=ft.Image(
                                        src=logo_base64 if logo_base64 else resource_path("logo.png"),
                                        width=180,
                                        height=180,
                                        fit="contain",
                                    ) if (logo_base64 or os.path.exists(resource_path("logo.png"))) else ft.Container(
                                        width=180,
                                        height=180,
                                        bgcolor="#ff6b00",
                                        border_radius=90,
                                        content=ft.Icon(ft.icons.STORE, size=100, color="white"),
                                    ),
                                    alignment="center",
                                    margin=ft.margin.only(bottom=10)
                                ),
                                
                                ft.Text(
                                    "STEAMBOX", 
                                    size=24, 
                                    weight="bold", 
                                    color="white", 
                                    text_align="center"
                                ),
                                
                                ft.Container(height=5),
                                
                                ft.Text(
                                    "Premium v2.0", 
                                    size=14, 
                                    color="#ff6b00", 
                                    weight="bold", 
                                    text_align="center"
                                ),
                                
                                ft.Container(height=10),
                                
                                ft.Container(
                                    content=ft.Row([
                                        ft.Icon(ft.icons.VERIFIED, size=18, color="#25c279"),
                                        ft.Text("Licença Ativa", size=14, color="#25c279", weight="bold"),
                                    ],
                                    alignment="center",
                                    spacing=5),
                                ),
                                
                                ft.Container(height=20),
                            ],
                            horizontal_alignment="center",
                            spacing=0,
                        ),
                        alignment="center",
                        margin=ft.margin.only(bottom=15)
                    ),
                    
                    ft.Divider(height=20, color=ft.colors.with_opacity(0.2, "white")),
                    
                    ft.Container(height=10),
                    
                    ft.ElevatedButton(
                        "Jogos",
                        icon=ICONS.GAMES,
                        width=180,
                        on_click=lambda e: self.change_page(e, "jogos"),
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor={
                                ft.MaterialState.DEFAULT: "#2180c0",
                                ft.MaterialState.HOVERED: "#1a6a9e",
                            },
                            elevation={
                                ft.MaterialState.DEFAULT: 5,
                                ft.MaterialState.HOVERED: 8,
                            },
                        ),
                    ),
                    
                    ft.Container(height=15),
                    
                    ft.ElevatedButton(
                        "Restart Steam",
                        icon=ICONS.REFRESH,
                        width=180,
                        on_click=lambda e: self.restart_steam(),
                        style=ft.ButtonStyle(
                            color="white",
                            bgcolor={
                                ft.MaterialState.DEFAULT: "#ff6b00",
                                ft.MaterialState.HOVERED: "#e05a00",
                            },
                            elevation={
                                ft.MaterialState.DEFAULT: 5,
                                ft.MaterialState.HOVERED: 8,
                            },
                        ),
                    ),
                    
                    ft.Container(height=20),
                ],
                horizontal_alignment="center",
                spacing=0,
            ),
        )

    # ---------- PÁGINA JOGOS ----------
    def create_games_content(self):
        self.search_field = ft.TextField(
            label="URL do jogo da Steam",
            hint_text="Cole a URL da Steam ou digite o APPID",
            border_color="#ff6b00",
            focused_border_color="#ff6b00",
            color="white",
            bgcolor=ft.colors.with_opacity(0.1, "#1a1a1a"),
            expand=True,
            multiline=True,
            min_lines=1,
            max_lines=3,
        )

        self.game_info_container = ft.Container(padding=20, visible=False)
        
        # Criar badge do carrinho
        self.cart_badge = ft.Badge(
            text=str(self.cart.get_total()) if self.cart.get_total() > 0 else "",
            bgcolor="#ff6b00",
            text_style=ft.TextStyle(size=10, weight="bold", color="white"),
        )

        return ft.Container(
            expand=True,
            padding=30,
            content=ft.Column(
                [
                    # Cabeçalho com título e carrinho
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Sua Biblioteca Premium",
                                        size=32,
                                        weight="bold",
                                        color="white",
                                    ),
                                    ft.Container(height=5),
                                    ft.Text(
                                        "Adicione jogos ao carrinho e instale todos de uma vez!",
                                        size=16,
                                        color="#25c279",
                                    ),
                                ],
                                expand=True,
                            ),
                            # Ícone do carrinho
                            ft.Container(
                                content=ft.Stack(
                                    [
                                        ft.IconButton(
                                            icon=ft.icons.SHOPPING_CART,
                                            icon_size=30,
                                            icon_color="white",
                                            tooltip="Ver carrinho",
                                            on_click=self.toggle_cart_view,
                                        ),
                                        ft.Container(
                                            content=self.cart_badge,
                                            right=0,
                                            top=0,
                                        ),
                                    ]
                                ),
                                margin=ft.margin.only(right=10),
                            ),
                        ],
                        alignment="space_between",
                    ),
                    
                    ft.Container(height=20),
                    
                    # Visualização do carrinho
                    self.create_cart_view(),
                    
                    ft.Container(height=20),
                    
                    # Pack de jogos
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "Mais de 27000 jogos adicionados automaticamente à sua Steam!",
                                    size=20,
                                    weight="bold",
                                    color="white",
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Instale o pack completo clicando abaixo",
                                    size=14,
                                    color="#aaaaaa",
                                ),
                                ft.Container(height=15),
                                ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "Instalar 27000 Jogos",
                                            icon=ICONS.DOWNLOAD,
                                            style=ft.ButtonStyle(
                                                color="white",
                                                bgcolor={
                                                    ft.MaterialState.DEFAULT: "#22c55e",
                                                    ft.MaterialState.HOVERED: "#16a34a",
                                                },
                                                padding=20,
                                                elevation={
                                                    ft.MaterialState.DEFAULT: 5,
                                                    ft.MaterialState.HOVERED: 8,
                                                },
                                            ),
                                            on_click=self.install_game_pack_with_progress,
                                        ),
                                        ft.Container(width=10),
                                        ft.ElevatedButton(
                                            "Remover Todos os Jogos",
                                            icon=ICONS.DELETE,
                                            style=ft.ButtonStyle(
                                                color="white",
                                                bgcolor={
                                                    ft.MaterialState.DEFAULT: "#ef4444",
                                                    ft.MaterialState.HOVERED: "#dc2626",
                                                },
                                                padding=20,
                                                elevation={
                                                    ft.MaterialState.DEFAULT: 5,
                                                    ft.MaterialState.HOVERED: 8,
                                                },
                                            ),
                                            on_click=self.confirm_uninstall_all,
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        padding=25,
                        bgcolor=ft.colors.with_opacity(0.1, "#1a1a1a"),
                        border=ft.border.all(1, ft.colors.with_opacity(0.1, "white")),
                        border_radius=10,
                        margin=ft.margin.only(bottom=20),
                    ),
                    
                    # Busca individual
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    "100 MIL JOGOS - INSTALE INDIVIDUALMENTE OU ADICIONE AO CARRINHO",
                                    size=20,
                                    weight="bold",
                                    color="white",
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "Cole a URL da Steam ou digite o APPID do jogo",
                                    size=14,
                                    color="#aaaaaa",
                                ),
                                ft.Container(height=15),
                                ft.Row(
                                    [
                                        self.search_field,
                                        ft.Container(width=10),
                                        ft.ElevatedButton(
                                            "Pesquisar",
                                            icon=ICONS.SEARCH,
                                            style=ft.ButtonStyle(
                                                color="white",
                                                bgcolor={
                                                    ft.MaterialState.DEFAULT: "#ff6b00",
                                                    ft.MaterialState.HOVERED: "#e05a00",
                                                },
                                                padding=15,
                                                elevation={
                                                    ft.MaterialState.DEFAULT: 5,
                                                    ft.MaterialState.HOVERED: 8,
                                                },
                                            ),
                                            on_click=self.search_appid,
                                        ),
                                    ]
                                ),
                                ft.Container(height=10),
                                ft.Text(
                                    "💡 Dica: Copie a URL do jogo na Steam e cole aqui!",
                                    size=12,
                                    color="#ffffff",
                                    italic=True
                                ),
                                ft.Container(height=20),
                                self.game_info_container,
                            ]
                        ),
                        padding=25,
                        bgcolor=ft.colors.with_opacity(0.1, "#1a1a1a"),
                        border=ft.border.all(1, ft.colors.with_opacity(0.1, "white")),
                        border_radius=10,
                    ),
                ],
                scroll=ft.ScrollMode.ADAPTIVE,
            ),
        )

    # ---------- FUNÇÕES DE JOGOS ----------
    def search_appid(self, e=None):
        if not self.license_valid:
            self.show_license_required_dialog()
            return
            
        user_input = (self.search_field.value or "").strip()
        if not user_input:
            self.show_warning_notification("Atenção", "Digite um APPID ou cole a URL do jogo!")
            return

        self.show_loading()

        threading.Thread(
            target=self.fetch_and_display_game, args=(user_input,), daemon=True
        ).start()

    def show_loading(self):
        self.game_info_container.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.ProgressRing(color="#ff6b00"),
                        ft.Container(width=10),
                        ft.Text("Carregando informações do jogo...", color="white")
                    ]
                )
            ]
        )
        self.game_info_container.visible = True
        self.page.update()

    def fetch_and_display_game(self, user_input):
        try:
            game_info = self.game_manager.fetch_game_info(user_input)
            self.run_on_ui(lambda gi=game_info: self.update_ui_with_game_info(gi))
        except Exception as e:
            self.run_on_ui(lambda msg=str(e): self.update_ui_with_error(msg))

    def update_ui_with_game_info(self, game_info):
        image_content = None
        if game_info["image"]:
            image_content = ft.Image(
                src=game_info["image"],
                width=200,
                height=100,
                fit="cover",
                border_radius=10,
            )

        status_color = "#22c55e" if game_info["available"] else "#f59e0b"
        status_icon = "✅" if game_info["available"] else "⚠️"
        status_text = (
            "Disponível para instalação" if game_info["available"] else "Pode exigir configuração adicional"
        )

        content_controls = []
        if image_content:
            content_controls.append(image_content)
            content_controls.append(ft.Container(height=10))

        content_controls.extend(
            [
                ft.Text(game_info["name"], size=18, weight="bold", color="white"),
                ft.Container(height=5),
                ft.Text(f"APPID: {game_info['appid']}", size=12, color="#9ca3af"),
                ft.Container(height=5),
                ft.Row(
                    [
                        ft.Text(status_icon, size=16),
                        ft.Text(status_text, size=14, color=status_color),
                    ]
                ),
            ]
        )

        if game_info["dlc_list"]:
            content_controls.extend(
                [
                    ft.Container(height=5),
                    ft.Text(
                        f"{len(game_info['dlc_list'])} DLCs disponíveis",
                        size=12,
                        color="#a6b8ff",
                    ),
                ]
            )

        buttons_row = []
        
        # Botão para adicionar ao carrinho
        # No método update_ui_with_game_info, modifique o botão "Adicionar ao Carrinho":

        buttons_row.append(
    ft.ElevatedButton(
        "Adicionar ao Carrinho",
        icon=ft.icons.ADD_SHOPPING_CART,
        style=ft.ButtonStyle(
            color="white", 
            bgcolor={
                ft.MaterialState.DEFAULT: "#ff6b00",
                ft.MaterialState.HOVERED: "#e05a00"
            },
            padding=15,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        on_click=lambda e, a=game_info["appid"], n=game_info["name"], i=game_info["image"], d=game_info["dlc_list"]: 
            self.add_to_cart(a, n, i, d),
    )
)
        
        buttons_row.append(ft.Container(width=10))
        
        buttons_row.append(
            ft.ElevatedButton(
                "Instalar Agora",
                icon=ICONS.DOWNLOAD,
                style=ft.ButtonStyle(
                    color="white", 
                    bgcolor={
                        ft.MaterialState.DEFAULT: "#22c55e",
                        ft.MaterialState.HOVERED: "#16a34a"
                    },
                    padding=15,
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                on_click=lambda e, a=game_info["appid"], n=game_info["name"]: self.install_game(
                    a, n
                ),
            )
        )

        if game_info["dlc_list"]:
            buttons_row.append(ft.Container(width=10))
            buttons_row.append(
                ft.ElevatedButton(
                    "Instalar com DLCs",
                    icon=ICONS.DOWNLOAD_FOR_OFFLINE,
                    style=ft.ButtonStyle(
                        color="white", 
                        bgcolor={
                            ft.MaterialState.DEFAULT: "#3b82f6",
                            ft.MaterialState.HOVERED: "#2563eb"
                        },
                        padding=15,
                        shape=ft.RoundedRectangleBorder(radius=10)
                    ),
                    on_click=lambda e, a=game_info["appid"], n=game_info["name"], d=game_info[
                        "dlc_list"
                    ]: self.install_game_with_dlcs(a, n, d),
                )
            )

        buttons_row.append(ft.Container(width=10))
        buttons_row.append(
            ft.ElevatedButton(
                "Remover Jogo",
                icon=ICONS.DELETE,
                style=ft.ButtonStyle(
                    color="white", 
                    bgcolor={
                        ft.MaterialState.DEFAULT: "#ef4444",
                        ft.MaterialState.HOVERED: "#dc2626"
                    },
                    padding=15,
                    shape=ft.RoundedRectangleBorder(radius=10)
                ),
                on_click=lambda e, a=game_info["appid"], n=game_info["name"]: self.confirm_remove_game(
                    a, n
                ),
            )
        )

        content_controls.extend([ft.Container(height=20), ft.Row(buttons_row, wrap=True)])

        self.game_info_container.content = ft.Column(content_controls)
        self.game_info_container.visible = True
        self.page.update()

    def update_ui_with_error(self, error_message):
        self.game_info_container.content = ft.Column(
            [
                ft.Row(
                    [
                        ft.Icon(ft.icons.ERROR_OUTLINE, color="#ef4444", size=40),
                        ft.Column(
                            [
                                ft.Text("Erro na Busca", size=16, weight="bold", color="#ef4444"),
                                ft.Text(error_message, color="white", size=14),
                            ]
                        )
                    ]
                )
            ]
        )
        self.game_info_container.visible = True
        self.page.update()

    def install_game(self, appid, name):
        if not self.license_valid:
            self.show_license_required_dialog()
            return
            
        self.show_progress_dialog(
            "Instalando Jogo", 
            f"Preparando instalação de {name}"
        )

        def worker():
            try:
                def progress_cb(progress, status):
                    self.update_progress_dialog(progress, status, f"Progresso: {progress}%")

                self.game_manager.install_single_game(
                    appid, name, False, [], progress_cb
                )
                self.close_progress_dialog()
                self.show_success_notification(
                    "Instalação Concluída", 
                    f"{name} foi instalado com sucesso!"
                )
            except Exception as e:
                self.close_progress_dialog()
                self.show_retry_dialog(appid, name, str(e))

        threading.Thread(target=worker, daemon=True).start()

    def install_game_with_dlcs(self, appid, name, dlc_list):
        if not self.license_valid:
            self.show_license_required_dialog()
            return
            
        self.show_progress_dialog(
            "Instalando com DLCs", 
            f"Preparando {name} + {len(dlc_list)} DLCs"
        )

        def worker():
            try:
                def progress_cb(progress, status):
                    self.update_progress_dialog(progress, status, f"Progresso: {progress}%")

                self.game_manager.install_single_game(
                    appid, name, True, dlc_list, progress_cb
                )
                self.close_progress_dialog()
                self.show_success_notification(
                    "Instalação Completa Concluída", 
                    f"{name} + {len(dlc_list)} DLCs instalados com sucesso!"
                )
            except Exception as e:
                self.close_progress_dialog()
                self.show_retry_dialog(appid, name, str(e))

        threading.Thread(target=worker, daemon=True).start()

    def show_retry_dialog(self, appid, name, error_msg):
        def on_retry(e):
            dlg.open = False
            self.page.update()
            self.install_game_with_fallback(appid, name)
        
        def on_cancel(e):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Método Alternativo Necessário"),
            content=ft.Column([
                ft.Text(f"Problema com {name}:", size=16, color="white"),
                ft.Text(error_msg, size=14, color="#9ca3af"),
                ft.Container(height=10),
                ft.Text("Deseja tentar método alternativo?", size=14, color="white"),
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.TextButton("Tentar Alternativo", on_click=on_retry),
            ],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def install_game_with_fallback(self, appid, name):
        self.show_progress_dialog("Instalação Alternativa", f"Usando método alternativo para {name}")
        
        def worker():
            try:
                def progress_cb(progress, status):
                    self.update_progress_dialog(progress, status, f"Método alternativo: {progress}%")
                
                success = self.game_manager.create_advanced_fallback_files(appid, progress_cb)
                
                self.close_progress_dialog()
                if success:
                    self.show_success_notification("Instalação Alternativa Concluída", 
                        f"{name} foi configurado com método alternativo!")
                else:
                    self.show_error_notification("Falha no Método Alternativo", 
                        "Não foi possível configurar o jogo.")
                    
            except Exception as e:
                self.close_progress_dialog()
                self.show_error_notification("Erro", f"Falha completa: {str(e)}")
        
        threading.Thread(target=worker, daemon=True).start()

    def confirm_remove_game(self, appid, name):
        def on_confirm(e):
            dlg.open = False
            self.page.update()
            self.remove_game(appid, name)

        def on_cancel(e):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar Remoção"),
            content=ft.Column(
                [
                    ft.Text(f"Tem certeza que deseja remover {name}?", size=16, color="white"),
                    ft.Container(height=10),
                    ft.Text(
                        "Esta ação removerá os arquivos de configuração do jogo da sua Steam.",
                        size=14,
                        color="#9ca3af"
                    ),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.TextButton(
                    "Remover", 
                    on_click=on_confirm, 
                    style=ft.ButtonStyle(color="#ef4444")
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def remove_game(self, appid, name):
        if not self.license_valid:
            self.show_license_required_dialog()
            return
            
        self.show_progress_dialog(
            "Removendo Jogo", 
            f"Preparando remoção de {name}"
        )

        def worker():
            try:
                def progress_cb(progress, status):
                    self.update_progress_dialog(progress, status, f"Progresso: {progress}%")

                self.game_manager.remove_single_game(appid, name, progress_cb)
                self.close_progress_dialog()
                self.show_success_notification(
                    "✅ Remoção Concluída", 
                    f"{name} foi removido com sucesso!"
                )
            except Exception as e:
                self.close_progress_dialog()
                self.show_error_notification(
                    "❌ Erro na Remoção", 
                    str(e)
                )

        threading.Thread(target=worker, daemon=True).start()

    def install_game_pack_with_progress(self, e):
        if not self.license_valid:
            self.show_license_required_dialog()
            return
            
        self.show_progress_dialog(
            "Adicionando 27000 jogos na sua Steam", 
            "Procurando arquivo Steambox.zip..."
        )

        def worker():
            try:
                def progress_cb(progress, status):
                    self.update_progress_dialog(progress, status, f"Progresso: {progress}%")

                self.game_manager.install_game_pack(progress_cb)
                self.close_progress_dialog()
                self.show_success_notification(
                    "🎉 Pack Instalado com Sucesso!", 
                    "Pack de jogos foi extraído para a pasta config da Steam!"
                )
            except Exception as ex:
                self.close_progress_dialog()
                self.show_error_notification(
                    "❌ Erro na Instalação", 
                    str(ex)
                )

        threading.Thread(target=worker, daemon=True).start()

    def confirm_uninstall_all(self, e):
        if not self.license_valid:
            self.show_license_required_dialog()
            return
            
        def on_confirm(ev):
            dlg.open = False
            self.page.update()
            self.perform_uninstall_all()

        def on_cancel(ev):
            dlg.open = False
            self.page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Row([ft.Icon(ft.icons.WARNING, color="#f59e0b"), ft.Text("ATENÇÃO")]),
            content=ft.Column(
                [
                    ft.Text(
                        "REMOÇÃO COMPLETA DE TODOS OS JOGOS",
                        size=16,
                        weight="bold",
                        color="#ef4444",
                    ),
                    ft.Container(height=15),
                    ft.Text("Esta ação irá:", size=14, color="white", weight="bold"),
                    ft.Container(height=5),
                    ft.Text("• Remover tudo instalado", size=12, color="#9ca3af"),
                    ft.Text("• Excluir todos os scripts de instalação", size=12, color="#9ca3af"),
                    ft.Text("• Limpar todas as configurações de jogos", size=12, color="#9ca3af"),
                    ft.Container(height=15),
                    ft.Text("Tem certeza que deseja continuar?", size=14, color="white"),
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.TextButton(
                    "SIM, REMOVER TUDO",
                    on_click=on_confirm,
                    style=ft.ButtonStyle(color="#ef4444"),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()

    def perform_uninstall_all(self):
        self.show_progress_dialog(
            "Limpando Biblioteca", 
            "Removendo todos os jogos instalados"
        )

        def worker():
            try:
                def progress_cb(progress, status):
                    self.update_progress_dialog(progress, status, f"Progresso: {progress}%")

                ok, removed = self.game_manager.uninstall_all_games(progress_cb)
                self.close_progress_dialog()
                if ok:
                    self.show_success_notification(
                        "🧹 Limpeza Concluída", 
                        f"Todos os jogos foram removidos! ({removed} arquivos excluídos)"
                    )
                else:
                    self.show_error_notification(
                        "❌ Falha na Limpeza", 
                        "Não foi possível remover todos os jogos"
                    )
            except Exception as e:
                self.close_progress_dialog()
                self.show_error_notification(
                    "❌ Erro na Limpeza", 
                    str(e)
                )

        threading.Thread(target=worker, daemon=True).start()

    # ---------- FUNÇÕES UTILITÁRIAS ----------
    def restart_steam(self):
        if not self.license_valid:
            self.show_license_required_dialog()
            return
            
        try:
            self.game_manager.close_steam_safely()
            steam_exe = os.path.join(self.game_manager.steam_path or "", "steam.exe")
            if os.path.exists(steam_exe):
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = 0
                subprocess.Popen([steam_exe], startupinfo=startupinfo)
                self.show_snackbar("Steam reiniciada manualmente.")
            else:
                self.show_snackbar("Steam não encontrada para reiniciar.")
        except Exception as e:
            self.show_snackbar(f"Erro ao reiniciar Steam: {e}")

    def close_dialog(self, e=None):
        if self.page.dialog:
            self.page.dialog.open = False
            self.page.update()

    # ---------- FUNÇÕES DE PROGRESSO E NOTIFICAÇÕES ----------
    def create_progress_dialog(self, title: str, subtitle: str = ""):
        self.progress_bar = ft.ProgressBar(
            value=0,
            color="#ff6b00",
            bgcolor="#374151",
            height=8,
            width=400
        )
        
        self.progress_status = ft.Text(
            subtitle,
            size=16,
            color="white",
            weight="bold"
        )
        
        self.progress_details = ft.Text(
            "Preparando...",
            size=14,
            color="#9ca3af"
        )

        return ft.AlertDialog(
            modal=True,
            shape=ft.RoundedRectangleBorder(radius=15),
            content=ft.Container(
                width=500,
                padding=30,
                bgcolor=ft.colors.with_opacity(0.95, "#1a1a1a"),
                border=ft.border.all(1, ft.colors.with_opacity(0.2, "#ff6b00")),
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.ProgressRing(color="#ff6b00", width=20, height=20),
                                ft.Text(title, size=20, weight="bold", color="white"),
                            ],
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        ft.Container(height=20),
                        self.progress_status,
                        ft.Container(height=10),
                        self.progress_bar,
                        ft.Container(height=10),
                        self.progress_details,
                        ft.Container(height=20),
                        ft.Row(
                            [
                                ft.Text(
                                    "Não feche este aplicativo durante o processo",
                                    size=12,
                                    color="#f59e0b",
                                    weight="bold"
                                )
                            ]
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
            ),
        )

    def update_progress_dialog(self, progress: int, status: str, details: str = ""):
        def _update():
            if self.progress_bar:
                self.progress_bar.value = progress / 100.0
            if self.progress_status:
                self.progress_status.value = status
            if self.progress_details:
                self.progress_details.value = details
            if self.page:
                self.page.update()

        self.run_on_ui(_update)

    def show_progress_dialog(self, title: str, subtitle: str = ""):
        def _show():
            self.progress_dialog = self.create_progress_dialog(title, subtitle)
            self.page.dialog = self.progress_dialog
            self.progress_dialog.open = True
            self.page.update()

        self.run_on_ui(_show)

    def close_progress_dialog(self):
        def _close():
            if self.progress_dialog:
                self.progress_dialog.open = False
            self.page.update()

        self.run_on_ui(_close)

    def show_success_notification(self, title: str, message: str):
        def _show():
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.CHECK_CIRCLE, color="#22c55e", size=24),
                        ft.Container(width=10),
                        ft.Column(
                            [
                                ft.Text(title, size=14, weight="bold", color="white"),
                                ft.Text(message, size=12, color="#d1d5db"),
                            ],
                            tight=True,
                        ),
                    ]
                ),
                bgcolor="#1a1a1a",
                duration=4000,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=15,
            )
            self.page.snack_bar.open = True
            self.page.update()

        self.run_on_ui(_show)

    def show_error_notification(self, title: str, message: str):
        def _show():
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.ERROR, color="#ef4444", size=24),
                        ft.Container(width=10),
                        ft.Column(
                            [
                                ft.Text(title, size=14, weight="bold", color="white"),
                                ft.Text(message, size=12, color="#d1d5db"),
                            ],
                            tight=True,
                        ),
                    ]
                ),
                bgcolor="#1a1a1a",
                duration=5000,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=15,
            )
            self.page.snack_bar.open = True
            self.page.update()

        self.run_on_ui(_show)

    def show_warning_notification(self, title: str, message: str):
        def _show():
            self.page.snack_bar = ft.SnackBar(
                content=ft.Row(
                    [
                        ft.Icon(ft.icons.WARNING, color="#f59e0b", size=24),
                        ft.Container(width=10),
                        ft.Column(
                            [
                                ft.Text(title, size=14, weight="bold", color="white"),
                                ft.Text(message, size=12, color="#d1d5db"),
                            ],
                            tight=True,
                        ),
                    ]
                ),
                bgcolor="#1a1a1a",
                duration=4000,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=15,
            )
            self.page.snack_bar.open = True
            self.page.update()

        self.run_on_ui(_show)

    def show_snackbar(self, message):
        if "✅" in message:
            self.show_success_notification("Sucesso", message.replace("✅", "").strip())
        elif "❌" in message:
            self.show_error_notification("Erro", message.replace("❌", "").strip())
        else:
            self.show_success_notification("Info", message)

    # ---------- MAIN ----------
    def main(self, page: ft.Page):
        self.page = page
        page.title = "SteamBox - Sua Biblioteca Premium"
        page.theme_mode = ft.ThemeMode.DARK
        page.padding = 0
        page.bgcolor = "#0a0f1a"

        # Configurações de janela (Apenas Desktop Windows)
        try:
            page.window_width = 1500
            page.window_height = 1000
            page.window_min_width = 1000
            page.window_min_height = 700
            page.window_center()
            page.window_resizable = False
            page.window_maximizable = True
            page.window_full_screen = False
        except Exception:
            # Ignora erros de janela no modo Web/Linux
            pass
        
        try:
            specific_png = r"D:\Korea Store\Kenix app\Aplicativo venda\logo.png"
            if os.path.exists(specific_png):
                page.window_icon = specific_png
                print(f"✅ Ícone da janela carregado de: {specific_png}")
            else:
                specific_icon = r"D:\Korea Store\Kenix app\Aplicativo venda\logo.ico"
                if os.path.exists(specific_icon):
                    page.window_icon = specific_icon
                    print(f"✅ Ícone da janela carregado de: {specific_icon}")
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        page.update()
        self.update_content()

# =============== ENTRYPOINT ===============
if __name__ == "__main__":
    app_instance = App()
    # Execução multiplataforma
    if platform.system() == "Windows":
        ft.app(target=app_instance.main)
    else:
        # No linux/servidor, prefere modo web para visualização externa se necessário
        ft.app(target=app_instance.main, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=8080)