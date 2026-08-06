import sys
import os
from pandas import DataFrame

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from projetos.conexao import con

def filtro01 ():
  conn = con()
  cursor = conn.cursor ()
  cursor.execute("""
    SELECT DISTINCT
    eac.NOTA,
    eac.ORDEM_MEDIDA
    FROM U620433.EMB_AVRES_CLIENTE eac 
    LEFT JOIN  U620433.EMB_TREAT_MOTIVO_CLIENTE_NCLB etmcn 
    ON eac.NOTA = etmcn.NOTA AND eac.ORDEM_MEDIDA = etmcn.ORDEM_MEDIDA
    WHERE etmcn.METODO_ENVIO IN ('COR')
    AND etmcn.CONCLUIDA_EM IS NULL
    AND eac.TIPO IN (8)
    AND eac.RESULTADO IS NULL
    """)
  resultado = cursor.fetchall ()
  colunas = [c[0] for c in cursor.description]
  cursor.close ()
  conn.close()

  Dt = DataFrame(resultado, columns=colunas)

  return Dt

def insert01():
    df = filtro01()

    if df.empty:
            return False

    conn = con()
    cursor = conn.cursor()

    dados = [(row['NOTA'], row['ORDEM_MEDIDA']) for _, row in df.iterrows()]

    try:
      cursor.executemany("""
        DELETE FROM U620433.EMB_AVRES_CLIENTE eac
        WHERE eac.NOTA = ?
        AND eac.ORDEM_MEDIDA = ?
        AND eac.TIPO = 8 ;
      """, dados)
      conn.commit()
      cursor.close()
      conn.close()
      return True
    
    except Exception as e:
        print("Erro ao inserir:", e)
        return False

if __name__ == '__main__':
    while True:
        insert01()
        print('EXECUTADO')