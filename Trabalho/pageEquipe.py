import cherrypy

class PaginaEquipe():
    topo = open("html/cabecalho.html").read()
    rodape = open("html/rodape.html").read()

    @cherrypy.expose()
    def index(self):
        html = self.topo
        html += '''<h2>Sandra de Oliveira Souza...</h2>'''
        html += self.rodape

        return html