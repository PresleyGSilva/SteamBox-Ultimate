import os
import re

def generate_steambox_ultra():
    with open("ico_b64.txt", "r") as f: ico_b64 = f.read().strip()
    print("🔧 Gerando steambox_ultra.py...")
    with open('steambox.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    with open('games_b64.txt', 'r') as f:
        games_b64 = f.read().strip()
    with open('logo_b64.txt', 'r') as f:
        logo_b64 = f.read().strip()

    # Injetar assets e função de extração
    assets_code = f'''
# ===== ASSETS EMBUTIDOS (ULTRA VERSION) =====
EMBEDDED_GAMES_ZIP = """{games_b64}"""
EMBEDDED_LOGO_PNG = """{logo_b64}"""

def extract_embedded_zip(destination_path):
    import base64, tempfile, zipfile, os
    try:
        zip_data = base64.b64decode(EMBEDDED_GAMES_ZIP)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".zip") as tmp:
            tmp.write(zip_data)
            tmp_path = tmp.name
        with zipfile.ZipFile(tmp_path, "r") as z:
            count = sum(1 for f in z.namelist() if f.endswith(".lua"))
            z.extractall(destination_path)
        os.unlink(tmp_path)
        return True, count
    except Exception as e:
        print(f"Erro na extração: {{e}}")
        return False, 0

def find_logo():
    import base64, tempfile
    try:
        data = base64.b64decode(EMBEDDED_LOGO_PNG)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
            tmp.write(data)
            return tmp.name
    except: return None
'''
    
    # Injetar no topo após os imports
    import_match = re.search(r'^(import.*?\n)+', code, re.MULTILINE)
    if import_match:
        pos = import_match.end()
        code = code[:pos] + assets_code + code[pos:]
    else:
        code = assets_code + code

    # Substituir install_game_pack
    new_install = '''    def install_game_pack(self, progress_callback=None):
        if not self.steam_path: self.steam_path = self.find_steam()
        try:
            if progress_callback: progress_callback(10, "Preparando...")
            self.close_steam_safely()
            config_path = os.path.join(self.steam_path, "config")
            os.makedirs(config_path, exist_ok=True)
            if progress_callback: progress_callback(40, "Extraindo jogos embutidos...")
            success, count = extract_embedded_zip(config_path)
            if success:
                if progress_callback: progress_callback(100, f"✅ {count} jogos instalados!")
                return True
            return False
        except Exception as e:
            if progress_callback: progress_callback(0, f"Erro: {e}")
            return False'''
    
    pattern = r'    def install_game_pack\(self, progress_callback=None\):.*?(?=\n    def|\Z|\nclass)'
    code = re.sub(pattern, new_install, code, flags=re.DOTALL)

    with open('steambox_ultra.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ steambox_ultra.py gerado.")

def generate_correcao_ultra():
    print("🔧 Gerando correcao_ultra.py...")
    with open('correção.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    with open('steam_b64.txt', 'r') as f:
        steam_b64 = f.read().strip()
    with open('hid_b64.txt', 'r') as f:
        hid_b64 = f.read().strip()
    with open('logo_b64.txt', 'r') as f:
        logo_b64 = f.read().strip()

    assets_code = f'''
# ===== ASSETS CORREÇÃO (ULTRA VERSION) =====
EMBEDDED_STEAM_ZIP = """{steam_b64}"""
EMBEDDED_HID_ZIP = """{hid_b64}"""
EMBEDDED_LOGO_PNG = """{logo_b64}"""

def get_embedded_resource(b64_data, suffix):
    import base64, tempfile
    try:
        data = base64.b64decode(b64_data)
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(data)
            return tmp.name
    except: return None
'''
    
    # Injetar assets
    import_match = re.search(r'^(import.*?\n)+', code, re.MULTILINE)
    if import_match:
        pos = import_match.end()
        code = code[:pos] + assets_code + code[pos:]
    else:
        code = assets_code + code

    # Substituir resource_path para usar as versões embutidas quando necessário
    # Esta parte é mais complexa, vou apenas garantir que o código use as funções de extração
    # para os arquivos latest32bitsteam.zip e steambox hid.zip
    
    code = code.replace('resource_path("latest32bitsteam.zip")', 'get_embedded_resource(EMBEDDED_STEAM_ZIP, ".zip")')
    code = code.replace('resource_path("steambox hid.zip")', 'get_embedded_resource(EMBEDDED_HID_ZIP, ".zip")')
    code = code.replace('resource_path("logo.png")', 'get_embedded_resource(EMBEDDED_LOGO_PNG, ".png")')

    with open('correcao_ultra.py', 'w', encoding='utf-8') as f:
        f.write(code)
    print("✅ correcao_ultra.py gerado.")

if __name__ == "__main__":
    generate_steambox_ultra()
    generate_correcao_ultra()
