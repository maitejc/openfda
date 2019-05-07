import http.server
import http.client
import json
import socketserver

IP = "127.0.0.1"
PORT=8000

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    OPENFDA_API_URL="api.fda.gov"
    OPENFDA_API_SEARCH_DRUG = "/drug/label.json?search=active_ingredient:%s"
    OPENFDA_API_SEARCH_COMPANY = "/drug/label.json?search=openfda.manufacturer_name:%s"
    OPENFDA_API_LIST_DRUG = "/drug/label.json?limit=%s"
    OPENFDA_API_LIST_COMPANY = "/drug/label.json?limit=%s"
    OPENFDA_API_LIST_WARNING = "/drug/label.json?limit=%s"

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open ("buscar.html", 'r') as f:
                archivo = f.read()
            self.wfile.write(bytes(archivo, "utf8"))
        elif "searchDrug" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            peticion = self.path.split("=")
            try:
                if peticion[2] != "":
                    principio = peticion[1]
                    limite = peticion[2]
                    principio_activo = principio + "=" + limite
                else:
                    #si no se introduce el límite
                    principio = peticion[1]
                    limite = "10"
                    principio_activo = principio + "=" + limite
            except IndexError:
                principio_activo = peticion[1] + "&limit=10"
            
            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_SEARCH_DRUG % principio_activo,None, headers)
            dame_respuesta = conn.getresponse()
            print(dame_respuesta.status, dame_respuesta.reason)
            repuesta_descodificada = dame_respuesta.read().decode("utf-8")
            conn.close()
            respuesta = json.loads(repuesta_descodificada)["results"]
            texto = ["<h1>Lista de medicamentos con esa sustancia</h3><br>"]
            for elementos in respuesta:
                if ('generic_name' in elementos['openfda']):
                    texto.append("<li>" + elementos["openfda"]["generic_name"][0] + "</li>")
                else:
                    texto.append("<li>Desconocido</li>")

            string = "".join(texto)
            self.wfile.write(bytes(string, "utf8"))
        elif "searchCompany" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            peticion = self.path.split("=")
            try:
                if peticion[2] != "":
                    empresa = peticion[1] 
                    limite = peticion[2]
                    buscar_empresa = empresa + "=" + limite
                else:
                    empresa = peticion[1]
                    limite = "10"
                    buscar_empresa = empresa + "=" + limite
            except IndexError:
                buscar_empresa = peticion[1] + "&limit=10"

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET",self.OPENFDA_API_SEARCH_COMPANY % buscar_empresa, None, headers)
            dame_resultados = conn.getresponse()
            print(dame_resultados.status, dame_resultados.reason)
            respuesta_descodificada = dame_resultados.read().decode("utf-8")
            conn.close()
            resultados = json.loads(respuesta_descodificada)["results"]
            texto = ["<h1>Lista de medicamentos de esa empresa</h1><br>"]
            for elementos in resultados:
                if ('generic_name' in elementos['openfda']):
                    texto.append("<li>" + elementos["openfda"]["generic_name"][0] + "</li>")
                else:
                    texto.append("<li>Desconocido</li>")

            string = "".join(texto)
            self.wfile.write(bytes(string, "utf8"))
        elif "listDrugs" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            peticion = self.path.split("=")
            limite = peticion[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_LIST_DRUG % limite, None, headers)
            dame_respuesta = conn.getresponse()
            print(dame_respuesta.status, dame_respuesta.reason)
            respuesta_descodificada = dame_respuesta.read().decode("utf-8")
            conn.close()
            respuesta = json.loads(respuesta_descodificada)["results"]
            texto =["<h1>Lista de medicamentos</h1><br>"]
            for elementos in respuesta:
                if ('generic_name' in elementos['openfda']):
                    texto.append("<li>" + elementos["openfda"]["generic_name"][0] + "</li>")
                else:
                    texto.append("<li>Desconocido</li>")

            string = "".join(texto)
            self.wfile.write(bytes(string, "utf8"))
        elif "listCompanies" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            peticion = self.path.split("=")
            limite = peticion[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET",self.OPENFDA_API_LIST_COMPANY %limite, None, headers)
            dame_respuesta = conn.getresponse()
            print(dame_respuesta.status, dame_respuesta.reason)
            respuesta_descodificada = dame_respuesta.read().decode("utf-8")
            conn.close()
            respuesta = json.loads(respuesta_descodificada)["results"]
            texto = ["<h1>Lista de empresas</h1><br>"]
            for elementos in respuesta:
                if ('manufacturer_name' in elementos['openfda']):
                    texto.append("<li>" + elementos["openfda"]["manufacturer_name"][0] + "</li>")
                else:
                    texto.append("<li>Desconocido</li>")

            string = "".join(texto)
            self.wfile.write(bytes(string, "utf8"))
        elif "listWarnings" in self.path:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            peticion = self.path.split("=")
            avisos = peticion[1]

            headers = {'User-Agent': 'http-client'}

            conn = http.client.HTTPSConnection(self.OPENFDA_API_URL)
            conn.request("GET", self.OPENFDA_API_LIST_WARNING % avisos, None, headers)
            dame_respuesta = conn.getresponse()
            print(dame_respuesta.status, dame_respuesta.reason)
            respuesta_descodificada = dame_respuesta.read().decode("utf-8")
            conn.close()
            respuesta = json.loads(respuesta_descodificada)["results"]
            texto = ["<h1>Lista de advertencias</h1><br>"]
            for elementos in respuesta:
                if ('warnings' in elementos):
                    texto.append("<li>"+ elementos["warnings"][0]+ "</li>")
                else:
                    texto.append("<li>Desconocido</li>")

            string = "".join(texto)
            self.wfile.write(bytes(string, "utf8"))
    
        elif 'redirect' in self.path:
            self.send_response(301)
            self.send_header('Location', 'http://localhost:'+ str(PORT))
            self.end_headers()
        elif "secret" in self.path:
            self.send_response(401)
            self.send_header('WWW-Authenticate', "Basic realm = DENIED")
            self.end_headers()
        
        else:
            self.send_response(404)
            self.end_headers()
            texto = ["<h1>Ha ocurrido un error, revisa que los datos introducidos sean correctos</h1><br>"]
            string = "".join(texto)
            self.wfile.write(bytes(string, "utf8"))
            
            
Handler = testHTTPRequestHandler
httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at %s:%s" % (IP, PORT))
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass
httpd.server_close()
print("Server stopped!")


