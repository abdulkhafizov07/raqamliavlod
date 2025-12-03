import sys
import socket
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QMessageBox

class AdminApp(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 12345))
        self.server_socket.listen(5)
        self.client_sockets = []
        
        threading.Thread(target=self.accept_clients, daemon=True).start()

    def initUI(self):
        self.setWindowTitle("Admin Panel")
        
        self.layout = QVBoxLayout()

        self.lock_button = QPushButton("Lock", self)
        self.lock_button.clicked.connect(self.lock_clients)
        self.layout.addWidget(self.lock_button)

        self.unlock_button = QPushButton("Unlock", self)
        self.unlock_button.clicked.connect(self.unlock_clients)
        self.layout.addWidget(self.unlock_button)

        self.setLayout(self.layout)
        self.show()

    def accept_clients(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            self.client_sockets.append(client_socket)
            print(f"Client {addr} connected.")

    def lock_clients(self):
        self.send_command("LOCK")

    def unlock_clients(self):
        self.send_command("UNLOCK")

    def send_command(self, command):
        for client_socket in self.client_sockets:
            try:
                client_socket.send(command.encode())
            except:
                self.client_sockets.remove(client_socket)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = AdminApp()
    sys.exit(app.exec_())
