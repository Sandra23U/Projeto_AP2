import cherrypy
import os

from pageTipo import PaginaTipo #classe PaginaTipo
#from pageAnuncio import PaginaAnuncio
from pageEquipe import PaginaEquipe #classe PaginaEquipe

local_dir = os.path.dirname(__file__)

class Principal():
    topo = open("html/cabecalho.html").read()
    rodape = open("html/rodape.html").read()
    @cherrypy.expose()
    def index(self):
        html = self.topo
        html = html + '''<br/>
        <p>Aqui vai o conteúdo central da página inicial do projeto...</p>
        <p class="cor1">Home da Cris</p><br/>
        '''
        html = html + self.rodape

        return html

#Para que o cherrypy possa encontrar os arquivos dentro do diretório da aplicação
local_config = {
    "/":{"tools.staticdir.on":True,
         "tools.staticdir.dir":local_dir},
}

#objetos utilizados para rota de navegação
root = Principal() #rota principal
root.pgTipo = PaginaTipo() #rota principal/pgTipo
#root.pgAnuncio = PaginaAnuncio() #rota principal/pgAnuncio
root.pgEquipe = PaginaEquipe() #rota princial/pgEquipe

cherrypy.quickstart(root,config=local_config)
