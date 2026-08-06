def get_notas_1(): # Cer_med
    from Conexao import con

    conn = con()

    if conn:
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
        NOTA
        FROM CLB354074.PRD_INS_SEP_MEDIDAS_NINTERRP        
        WHERE NOTA IN (
        '9100181361',
        '9100179451',
        '9100182327',
        '9100182917',
        '9100179444',
        '9100185018',
        '9100188021',
        '9100186550',
        '9100187049',
        '9100185558',
        '9100189549',
        '9100180888',
        '9100212082',
        '9100211586',
        '9100182347',
        '9100178837',
        '9100181349',
        '9100264007')
        AND DT_CONC IS NULL
        """)

        dados = cursor.fetchall()

        cursor.close()
        conn.close()

        return dados

    return []