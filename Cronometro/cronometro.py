import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
import mysql.connector
from datetime import datetime

class Cronometro(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("cronometro.ui", self)

        self.tempo_segundos = 0
        self.esta_rodando = False

        self.label_tempo.setText("00:00:00")
        self.botao_pausar.setEnabled(False)

        self.botao_iniciar.clicked.connect(self.iniciar_cronometro)
        self.botao_pausar.clicked.connect(self.pausar_cronometro)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_tempo)

        self.db_config = {
            'user': 'root',
            'password': '34863794', 
            'host': '127.0.0.1',
            'port': '3306',
            'database': 'contadordetempo'
        }

    def iniciar_cronometro(self):
        if not self.esta_rodando:
            self.esta_rodando = True
            self.timer.start(1000)  
            self.botao_iniciar.setEnabled(False)
            self.botao_pausar.setEnabled(True)

    def pausar_cronometro(self):
        print("Função pausar_cronometro chamada")
        if self.esta_rodando:
            self.esta_rodando = False
            self.timer.stop()
            self.botao_iniciar.setEnabled(True)
            self.botao_pausar.setEnabled(False)
            self.salvar_tempo()

    def atualizar_tempo(self):
        self.tempo_segundos += 1
        horas = self.tempo_segundos // 3600
        minutos = (self.tempo_segundos % 3600) // 60
        segundos = self.tempo_segundos % 60
        self.label_tempo.setText(f"{horas:02d}:{minutos:02d}:{segundos:02d}")

    def salvar_tempo(self):
        print("Função salvar tempo rolando ai")
        horas = self.tempo_segundos // 3600
        minutos = (self.tempo_segundos % 3600) // 60
        segundos = self.tempo_segundos % 60
        data_atual = datetime.now()

        try:
            print("Try rola")
            conexao = mysql.connector.connect(**self.db_config)
            print('Passou de conexao')
            cursor = conexao.cursor()
            query = "INSERT INTO contador (horas, minutos, segundos, data) VALUES (%s, %s, %s, %s)"
            valores = (horas, minutos, segundos, data_atual)
            cursor.execute(query, valores)
            conexao.commit()
            print("Tempo salvo com sucesso!")
        except mysql.connector.Error as err:
            print(f"Erro ao salvar no banco: {err}")
        finally:
            if conexao.is_connected():
                cursor.close()
                conexao.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    janela = Cronometro()
    janela.show()
    sys.exit(app.exec_())
