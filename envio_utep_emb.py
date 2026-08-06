from conexao import con
from datetime import datetime
import time
import win32com.client as win32
from pandas import DataFrame
import os


def destinatarios():
    try:
        conn = con()
        cursor = conn.cursor()
        cursor.execute("""
            WITH GERAL AS (
            SELECT
                PSMN.NOTA,
                PSMN.ORDEM_MEDIDA,
                PSMN.MOTIVO,
                PSMN.CRIADA_EM,
                CASE
                    WHEN (
                        PSMN.MOTIVO LIKE '%OUTORGA%'
                    OR PSMN.MOTIVO LIKE '%CLIENTE%'
                    OR PSMN.MOTIVO LIKE '%ART%MEMORIAL%'
                    OR PSMN.MOTIVO LIKE '%ART%'
                    OR PSMN.MOTIVO LIKE '%MEMORIAL%'
                    OR PSMN.MOTIVO LIKE '%DOCUMENTACAO%CONTRATO%'
                    OR PSMN.MOTIVO LIKE '%PONTO%ENTREGA%'
                    )
                    THEN ADD_DAYS(PSMN.CRIADA_EM, 60)
                    WHEN PSMN.MOTIVO LIKE '%NAO%OBTIDO%ACESSO%'
                    THEN ADD_DAYS(PSMN.CRIADA_EM, 15)
                END AS DT_VENCIMENTO,
                CASE
                    WHEN (
                        PSMN.MOTIVO LIKE '%OUTORGA%'
                    OR PSMN.MOTIVO LIKE '%CLIENTE%'
                    OR PSMN.MOTIVO LIKE '%ART%MEMORIAL%'
                    OR PSMN.MOTIVO LIKE '%ART%'
                    OR PSMN.MOTIVO LIKE '%MEMORIAL%'
                    OR PSMN.MOTIVO LIKE '%DOCUMENTACAO%CONTRATO%'
                    OR PSMN.MOTIVO LIKE '%PONTO%ENTREGA%'
                    )
                    AND DAYS_BETWEEN(PSMN.CRIADA_EM, CURRENT_DATE) >= 60
                    THEN 'VENCIDO'
                    WHEN PSMN.MOTIVO LIKE '%NAO%OBTIDO%ACESSO%'
                    AND DAYS_BETWEEN(PSMN.CRIADA_EM, CURRENT_DATE) >= 15
                    THEN 'VENCIDO'
                    WHEN (
                        PSMN.MOTIVO LIKE '%OUTORGA%'
                    OR PSMN.MOTIVO LIKE '%CLIENTE%'
                    OR PSMN.MOTIVO LIKE '%ART%MEMORIAL%'
                    OR PSMN.MOTIVO LIKE '%ART%'
                    OR PSMN.MOTIVO LIKE '%MEMORIAL%'
                    OR PSMN.MOTIVO LIKE '%DOCUMENTACAO%CONTRATO%'
                    OR PSMN.MOTIVO LIKE '%PONTO%ENTREGA%'
                    )
                    AND DAYS_BETWEEN(PSMN.CRIADA_EM, CURRENT_DATE) BETWEEN 55 AND 59
                    THEN 'A VENCER'
                    WHEN PSMN.MOTIVO LIKE '%NAO%OBTIDO%ACESSO%'
                    AND DAYS_BETWEEN(PSMN.CRIADA_EM, CURRENT_DATE) BETWEEN 10 AND 14
                    THEN 'A VENCER'
                    ELSE 'DENTRO DO PRAZO'
                END AS PRAZO,
                AUU.NOME_COMPLETO,
                PES.EMAIL_SOLICITANTE,
                AUU.LIDER_EMAIL
            FROM
                U621267.PRD_EMB_SOLICITACAO PES
            LEFT JOIN U621267.PRD_SEP_MEDIDAS_NINTERRP PSMN
                ON
                PES.NOTA = PSMN.NOTA
            LEFT JOIN U621267.ADM_USR_USUARIOS AUU
                ON
                PES.EMAIL_SOLICITANTE = AUU.EMAIL AND AUU.DESABILITADO_EM IS NULL
            WHERE
                PES.SOLICITADO_EM = (
                SELECT
                    MAX(PES2.SOLICITADO_EM)
                FROM
                    U621267.PRD_EMB_SOLICITACAO PES2
                WHERE
                    PES.NOTA = PES2.NOTA
            --		AND PES.ORDEM_MEDIDA = PES2.ORDEM_MEDIDA
                    AND PES2.AVALIACAO = 'PROCEDENTE'
                    AND (
                    ((PSMN.MOTIVO LIKE '%OUTORGA%'
                        OR PSMN.MOTIVO LIKE '%CLIENTE%'
                        OR PSMN.MOTIVO LIKE '%ART%MEMORIAL%'
                        OR PSMN.MOTIVO LIKE '%ART%'
                        OR PSMN.MOTIVO LIKE '%MEMORIAL%'
                        OR PSMN.MOTIVO LIKE '%DOCUMENTACAO%CONTRATO%'
                        OR PSMN.MOTIVO LIKE '%PONTO%ENTREGA%'
                        )
                    AND DAYS_BETWEEN(
                                CAST(PES2.SOLICITADO_EM AS DATE),
                                CURRENT_DATE
                            ) >= 60
                    )
                        OR
                    (PSMN.MOTIVO LIKE '%NAO%OBTIDO%ACESSO%'
                            AND DAYS_BETWEEN(
                                CAST(PES2.SOLICITADO_EM AS DATE),
                                CURRENT_DATE
                            ) >= 15))
                )
                AND PSMN.CONCLUIDA_EM IS NULL
            )
            SELECT
                *
            FROM
                GERAL
            WHERE
                PRAZO IN ('VENCIDO', 'A VENCER')
                AND GERAL.MOTIVO IN ('CLIENTE LIGADO A REVELIA')
        """)
        resultado = cursor.fetchall()
        colunas = [c[0] for c in cursor.description]
        cursor.close()
        conn.close()

        Dt = DataFrame(resultado, columns=colunas)

        return Dt
    except Exception as e:
        print(f"Erro: {e}")


def enviar_email():
    resultados = []
    df = destinatarios()

    for _, linha in df.iterrows():
        nota = linha["NOTA"]
        ordem = linha["ORDEM_MEDIDA"]
        email_to = linha["EMAIL_SOLICITANTE"]
        email_cc = linha["LIDER_EMAIL"]

        try:
            outlook = win32.Dispatch("Outlook.Application")
            email = outlook.CreateItem(0)

            email.To = email_to
            email.CC = email_cc

            email.Subject = "Notificação: Solicitações de Embargo"

            with open(
                r"C:\Users\u620433\OneDrive - IBERDROLA S.A\HOSTAP\OUTRO\projetos\static\html\index.html",
                "r",
                encoding="utf-8",
            ) as f:
                html = f.read()

            html = html.replace("{{NOTA}}", str(nota))
            html = html.replace("{{ORDEM}}", str(ordem))
            html = html.replace("{{MOTIVO}}", str(linha["MOTIVO"]))
            html = html.replace(
                "{{CRIADA_EM}}", linha["CRIADA_EM"].strftime("%d/%m/%Y")
            )
            html = html.replace(
                "{{DT_VENCIMENTO}}", linha["DT_VENCIMENTO"].strftime("%d/%m/%Y")
            )
            html = html.replace("{{PRAZO}}", str(linha["PRAZO"]))
            html = html.replace("{{NOME_COMPLETO}}", str(linha["NOME_COMPLETO"]))

            anexo = email.Attachments.Add(
                r"C:\Users\u620433\OneDrive - IBERDROLA S.A\HOSTAP\OUTRO\projetos\static\mage\neo.png"
            )

            anexo.PropertyAccessor.SetProperty(
                "http://schemas.microsoft.com/mapi/proptag/0x3712001F", "neo_logo"
            )

            email.HTMLBody = html
            # email.Display()
            email.Send()

            time.sleep(5)

            namespace = outlook.GetNamespace("MAPI")

            itens_enviados = namespace.GetDefaultFolder(5)

            itens = itens_enviados.Items
            itens.Sort("[SentOn]", True)

            ultimo_email = itens.GetFirst()

            evidencia_envio(ultimo_email, nota, ordem)

            log_execucao(
                "SUCESSO",
                nota,
                ordem,
                linha["MOTIVO"],
                linha["NOME_COMPLETO"],
                email_to,
                "Email enviado com sucesso",
            )

            resultados.append(
                {
                    "DATA_HORA": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "STATUS": "SUCESSO",
                    "NOTA": nota,
                    "ORDEM": ordem,
                    "MOTIVO": linha["MOTIVO"],
                    "NOME": linha["NOME_COMPLETO"],
                    "EMAIL": email_to,
                    "DETALHE": "Email enviado com sucesso",
                }
            )

            print("E-mail enviado com sucesso!")

        except Exception as e:

            registrar_erro(nota, ordem, linha["MOTIVO"], email_to, str(e))

            log_execucao(
                "ERRO",
                nota,
                ordem,
                linha["MOTIVO"],
                linha["NOME_COMPLETO"],
                email_to,
                str(e),
            )

            resultados.append(
                {
                    "DATA_HORA": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "STATUS": "ERRO",
                    "NOTA": nota,
                    "ORDEM": ordem,
                    "MOTIVO": linha["MOTIVO"],
                    "NOME": linha["NOME_COMPLETO"],
                    "EMAIL": email_to,
                    "DETALHE": str(e),
                }
            )

            print(f"Erro ao enviar e-mail: {e}")

    gerar_csv_execucao(resultados)


def evidencia_envio(email_enviado, nota, ordem):

    pasta = (
        r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB\ENVIO_UTEP_EMB\ENVIADO"
    )

    os.makedirs(pasta, exist_ok=True)

    data_envio = email_enviado.SentOn.strftime("%Y-%m-%d_%H%M%S")

    caminho = os.path.join(pasta, f"EMB_{nota}_{ordem}_{data_envio}.msg")

    email_enviado.SaveAs(caminho)

    print(f"Evidência salva: {caminho}")


def registrar_erro(nota, ordem, motivo, email, erro):

    pasta = r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB\ENVIO_UTEP_EMB\ERRO"

    os.makedirs(pasta, exist_ok=True)

    arquivo = os.path.join(
        pasta, f"ERRO_{nota}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt"
    )

    with open(arquivo, "w", encoding="utf-8") as f:

        f.write("RELATÓRIO DE ERRO\n")
        f.write("=" * 20 + "\n")
        f.write(f"Data/Hora: {datetime.now()}\n")
        f.write(f"Nota: {nota}\n")
        f.write(f"Ordem: {ordem}\n")
        f.write(f"Motivo: {motivo}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Descrição: {erro}\n")


def log_execucao(status, nota, ordem, motivo, nome, email, detalhe):

    pasta = (
        r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB\ENVIO_UTEP_EMB\LOG\END"
    )

    os.makedirs(pasta, exist_ok=True)

    arquivo = os.path.join(
        pasta, f"LOG_{nota}_{ordem}_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.txt"
    )

    with open(arquivo, "w", encoding="utf-8") as f:

        f.write("RELATÓRIO LOG\n")
        f.write("=" * 20 + "\n")
        f.write(f"Data/Hora: {datetime.now()}\n")
        f.write(f"Status: {status}\n")
        f.write(f"Nota: {nota}\n")
        f.write(f"Ordem: {ordem}\n")
        f.write(f"Motivo: {motivo}\n")
        f.write(f"Nome: {nome}\n")
        f.write(f"Email: {email}\n")
        f.write(f"Detalhe: {detalhe}\n")


def gerar_csv_execucao(resultados):

    pasta = (
        r"C:\Users\u620433\OneDrive - IBERDROLA S.A\EMBARGO_EMB\ENVIO_UTEP_EMB\LOG\CSV"
    )

    os.makedirs(pasta, exist_ok=True)

    arquivo = os.path.join(
        pasta, f"RES_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.csv"
    )

    df = DataFrame(resultados)

    df.to_csv(arquivo, sep=";", index=False, encoding="utf-8-sig")

    print(f"CSV gerado: {arquivo}")


ultima_execucao = None


def agendador():
    global ultima_execucao

    while True:

        agora = datetime.now()

        # if agora.hour == 6 and agora.minute == 30 and ultima_execucao != agora.date():
        if agora.hour == 11 and agora.minute == 24 and ultima_execucao != agora.date():

            enviar_email()

            ultima_execucao = agora.date()

        time.sleep(30)


if __name__ == "__main__":
    print("Aguardando execucao")
    agendador()
