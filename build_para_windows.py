import os
import sys
import subprocess
import shutil

def run_cmd(cmd):
    print(f"🚀 Rodando: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Erro:\n{result.stderr}")
        return False
    return True

def build():
    print("🛠️ Iniciando Build do SteamBox Ultimate para Windows...")
    
    # Check PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("📦 Instalando PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller flet"])

    # 1. Compilar SteamBox Ultra
    print("🔨 Compilando SteamBox Principal...")
    cmd_app = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--onefile", "--windowed",
        "--name", "SteamBox_Ultimate",
        "--icon", "logo.ico",
        "steambox_ultra.py"
    ]
    if not run_cmd(cmd_app): return

    # 2. Compilar Correção Ultra
    print("🔨 Compilando Correção Steam...")
    cmd_fix = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm", "--onefile", "--console",
        "--name", "Corrigir_Steam",
        "--icon", "logo.ico",
        "correcao_ultra.py"
    ]
    if not run_cmd(cmd_fix): return

    # 3. Organizar pasta final
    output_dir = "SteamBox_Final"
    os.makedirs(output_dir, exist_ok=True)
    
    if os.path.exists("dist/SteamBox_Ultimate.exe"):
        shutil.copy2("dist/SteamBox_Ultimate.exe", f"{output_dir}/SteamBox_Ultimate.exe")
    if os.path.exists("dist/Corrigir_Steam.exe"):
        shutil.copy2("dist/Corrigir_Steam.exe", f"{output_dir}/Corrigir_Steam.exe")

    # 4. Criar instruções
    with open(f"{output_dir}/LEIA_ME.txt", "w", encoding="utf-8") as f:
        f.write("""STEAMBOX ULTIMATE - INSTRUÇÕES (WINDOWS)

BEM-VINDO AO STEAMBOX ULTIMATE!

1. ARQUIVOS INCLUÍDOS:
   - SteamBox_Ultimate.exe: Aplicativo principal de jogos.
   - Corrigir_Steam.exe: Ferramenta para corrigir a Steam e fazer os jogos aparecerem.

2. COMO USAR:
   - Se os jogos não aparecerem na Steam, feche a Steam e rode o 'Corrigir_Steam.exe' como ADMINISTRADOR.
   - Abra a Steam e depois o 'SteamBox_Ultimate.exe'.

3. AVISO:
   - O programa pode ser detectado como vírus por alguns antivírus devido à proteção do código. 
   - É um FALSO POSITIVO. Pode ignorar e executar normalmente.

Aproveite seus jogos!
""")

    print(f"\n✅ CONCLUÍDO! Seu pacote está na pasta: {output_dir}")

if __name__ == "__main__":
    build()
