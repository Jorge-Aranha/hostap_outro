import os, zipfile, time, shutil
from datetime import datetime

# V_ENV
ENVIO_FINAL = r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB_CLIENTE\EMB_CLIENTE_CANC\V_ENV\ENVIO_FINAL"
TEMPORARIO_ZIP = r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB_CLIENTE\EMB_CLIENTE_CANC\V_ENV\TEMPORARIO_ZIP"
TEMPORARIO_CSV = r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB_CLIENTE\EMB_CLIENTE_CANC\V_ENV\TEMPORARIO_CSV"

# G_ENV
END_FINAL = r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB_CLIENTE\EMB_CLIENTE_CANC\G_ENV\END_FINAL"


for pasta in [ENVIO_FINAL, TEMPORARIO_ZIP, TEMPORARIO_CSV, END_FINAL]:
    os.makedirs(pasta, exist_ok=True)


def zipar_envio():
    erro = False

    
    arquivos_zip = os.listdir(TEMPORARIO_ZIP)
    arquivos_csv = os.listdir(TEMPORARIO_CSV)

    if not arquivos_zip and not arquivos_csv:
        print("Não há arquivos para compactar")
        return


    agora = datetime.now()
    data = agora.strftime("%Y-%m-%d-%H-%M-%S")

    nome_zip = f"ENVIO_FINAL_{data}.zip"
    caminho_zip = os.path.join(ENVIO_FINAL, nome_zip)

    try:
        with zipfile.ZipFile(caminho_zip, 'w') as zipf:

            # TEMPORARIO_ZIP
            for arquivo in os.listdir(TEMPORARIO_ZIP):
                caminho = os.path.join(TEMPORARIO_ZIP, arquivo)
                if os.path.isfile(caminho):
                    zipf.write(caminho, arcname=arquivo)

            # TEMPORARIO_CSV
            for arquivo in os.listdir(TEMPORARIO_CSV):
                caminho = os.path.join(TEMPORARIO_CSV, arquivo)
                if os.path.isfile(caminho):
                    zipf.write(caminho, arcname=arquivo)

    except:
        erro = True

    # copiar para END_FINAL
    try:
        destino = os.path.join(END_FINAL, nome_zip)
        shutil.copy(caminho_zip, destino)
    except:
        erro = True

    if erro:
        print("Não feito ZIP")
    else:
        print("ZIP gerado")


def limpar_envio_final():
    erro = False

    for arquivo in os.listdir(ENVIO_FINAL):
        caminho = os.path.join(ENVIO_FINAL, arquivo)
        try:
            os.remove(caminho)
        except:
            erro = True

    if erro:
        print("Não limpou")
    else:
        print("ENVIO_FINAL limpo")


executado_zip = False
executado_limpeza = False

def agendador():
    global executado_zip, executado_limpeza

    while True:
        agora = datetime.now()

        # Domingo
        if (
            agora.weekday() == 6 and
            agora.hour == 14 and
            agora.minute == 20 and
            not executado_zip
        ):
            zipar_envio()
            executado_zip = True
            print("Executado zipar_envio")

        # Terça
        if (
            agora.weekday() == 5 and  #DIA - HORA - MINUTO - SEG 
            agora.hour == 9 and
            agora.minute == 0 and
            not executado_limpeza
        ):
            limpar_envio_final()
            executado_limpeza = True
            print("Executado limpar_envio_final")

        if agora.minute != 20:
            executado_zip = False

        if agora.minute != 0:
            executado_limpeza = False


        time.sleep(30)

if __name__ == "__main__":
    print("Aguardando execucao")
    agendador() 