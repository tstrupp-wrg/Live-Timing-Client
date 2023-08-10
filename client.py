import sys
import socket
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QTextEdit
from PyQt5.QtCore import QThread, pyqtSignal

# 192.168.1.127
# 5005

class ClientWorker(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, server_ip, server_port):
        super().__init__()
        self.server_ip = server_ip
        self.server_port = server_port

    def run(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((self.server_ip, self.server_port))
            self.data_received.emit('Connected to server\n')
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                self.data_received.emit(data.decode())
        except ConnectionRefusedError:
            self.data_received.emit('Connection refused\n')
        except Exception as e:
            self.data_received.emit(f'Error: {str(e)}')
        finally:
            client_socket.close()

class ClientGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('TCP Client')
        self.setGeometry(100, 100, 300, 400)

        # IP address input
        self.ip_input = QLineEdit(self)
        self.ip_input.setPlaceholderText('Server IP')
        self.ip_input.setGeometry(20, 20, 150, 30)

        # Port number input
        self.port_input = QLineEdit(self)
        self.port_input.setPlaceholderText('Port Number')
        self.port_input.setGeometry(180, 20, 100, 30)

        # Connect button
        self.connect_btn = QPushButton('Connect', self)
        self.connect_btn.setGeometry(20, 70, 260, 30)
        self.connect_btn.clicked.connect(self.connect_to_server)

        # Data display
        self.data_display = QTextEdit(self)
        self.data_display.setGeometry(20, 120, 260, 240)
        self.data_display.setReadOnly(True)

    def connect_to_server(self):
        server_ip = self.ip_input.text()
        server_port = int(self.port_input.text())

        self.worker = ClientWorker(server_ip, server_port)
        self.worker.data_received.connect(self.update_data_display)
        self.worker.start()

    def update_data_display(self, data):
        self.data_display.append(data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ClientGUI()
    window.show()
    sys.exit(app.exec_())
