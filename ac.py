from datetime import datetime
import time

executado = False
def agendador():
    global executado

    while True:
        agora = datetime.now()

        # if (
        #     agora.weekday() == 0 and  #DIA - HORA - MINUTO - SEG
        #     agora.hour == 4 and
        #     agora.minute == 30 and
        #     not executado
        # ):


        if (
            agora.weekday() == 0 and  #DIA - HORA - MINUTO - SEG
            agora.hour == 9 and
            agora.minute == 26 and
            not executado
        ):
            executado = True

        print('feitoS')


if __name__ == '__main__':
  print('Aguaradando')
  agendador()