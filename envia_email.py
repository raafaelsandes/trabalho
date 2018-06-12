#!/usr/bin/python
#RAFA

import cgi
import smtplib
from os import curdir
from os.path import join as pjoin
from http.server import BaseHTTPRequestHandler, HTTPServer


def send_email(email, subject, body):
    gmail_user = "enviodeemailviaform@gmail.com"
    gmail_password = "teste313"

    email_text = """   
    From: %s  
    To: %s  
    Subject: %s
    
    %s
    """ % (gmail_user, ", ".join(email), subject, body)
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, email.split(','), email_text)
        server.close()

        result = 'Email enviado!'
    except:
        result = 'Problema no envio...'

    return result


# Essa classe manipulara qualquer solicitacao recebida do navegador
class RafaHandler(BaseHTTPRequestHandler):

    # Manipulador para as solicitacoes do GET
    def do_GET(self):

        if self.path == "/":
            self.path = pjoin(curdir, 'formulario.html')

        try:
            # Verifique a extensao de arquivo necessaria e defina o tipo certo de mime
            tenta_enviar = False
            if self.path.endswith(".html"):
                mimetype = 'text/html'
                tenta_enviar = True
            if self.path.endswith(".jpg"):
                self.path = pjoin(curdir, self.path.replace('/', ''))
                mimetype = 'image/jpg'
                tenta_enviar = True
            if self.path.endswith(".gif"):
                self.path = pjoin(curdir, self.path.replace('/', ''))
                mimetype = 'image/gif'
                tenta_enviar = True
            if self.path.endswith(".js"):
                self.path = pjoin(curdir, self.path.replace('/', ''))
                mimetype = 'application/javascript'
                tenta_enviar = True
            if self.path.endswith(".css"):
                self.path = pjoin(curdir, self.path.replace('/', ''))
                mimetype = 'text/css'
                tenta_enviar = True

            if tenta_enviar:
                # Abra o arquivo estático solicitado e envie
                with open(self.path) as out:
                    self.send_response(200)
                    self.send_header('Content-type', mimetype)
                    self.end_headers()
                    self.wfile.write(out.read().encode())

            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Manipulador para as solicitacoes do POST
    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST',
                     'CONTENT_TYPE': self.headers['Content-Type'],
                     })

        name = form["nome"].value
        fone = form["telefone"].value
        email = form["email"].value
        mensagem = form["mensagem"].value

        result = send_email(email, "Email do Cliente", mensagem)

        print(name, fone, email, mensagem)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(result.encode())
        return


def main():
    # Porta do serviço
    port_number = 8080
    try:
        # Crie um servidor da Web e defina o manipulador para gerenciar a solicitacao recebida
        server = HTTPServer(('', port_number), RafaHandler)
        print("Started httpserver on port http://0.0.0.0:{0}".format(port_number))
        # Aguarde para sempre os pedidos de HTTP recebidos
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')
        server.socket.close()


if __name__ == "__main__":
    # executar apenas se for executado como um script
    main()
