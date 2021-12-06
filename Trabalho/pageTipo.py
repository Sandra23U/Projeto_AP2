import cherrypy
from classes.tipo import *

class PaginaTipo():
    topo = open("html/cabecalho.html").read()
    rodape = open("html/rodape.html").read()
    @cherrypy.expose()
    def index(self):
        return self.montaFormulario()

    def montaFormulario(self, pId=0, pNome=""):
        html = self.topo

        html += '''<br/>
                <h2>Tipos de Anúncios</h2><br/>
                <form name="formCadastro" action="gravarTipo" method="post">
                    <p>
                        <input type="hidden" id="txtId" name="txtId" value="%s" />
                        <label><b>Informe o nome do tipo:</b></label><br />
                        <input type="text" id="txtNome" name="txtNome" value="%s" size="50" maxlength="50" required />
                    </p>
                    <p><br/>
                        <input type="submit" id="btnGravar" name="btnGravar" value="Gravar" />
                    </p><br/>
                </form>
                
                ''' % (pId, pNome)

        html += self.montaTabela()
        html += self.rodape

        return html
#=========================================================
    def montaTabela(self):
        html = '''<table class="alinha">
                    <tr>
                        <th>ID</th>
                        <th>Nome do Tipo</th>
                        <th>Ação</th>
                    </tr>
        '''
        objTipo = Tipo()
        dados = objTipo.obterTipos()
        for tp in dados:
            html += "<tr>" \
                        "<td>%s</td>" \
                        "<td>%s</td>" \
                        "<td style='text-align:center'>[<a href='alterarTipo?idTipo=%s'>Alterar</a>] " \
                            "[<a href='excluirTipo?idTipo=%s'>Excluir</a>]" \
                    "</tr> \n" % (tp["id"], tp["nome"], tp["id"], tp["id"])

        html += "</table><br/>"
        return html
#===============================================================
#o que ação tem que expor (interação get ou post)
    @cherrypy.expose()
    def gravarTipo(self,txtId,txtNome,btnGravar):
        if len(txtNome) > 0:
            objTipo = Tipo()
            objTipo.set_nome(txtNome)
            retorno = 0 #variável de controle...

            if int(txtId) == 0: #Novo registro
                retorno = objTipo.gravar()
            else: #Alterando um registro existente
                objTipo.set_id(int(txtId)) #definindo para o objeto o id a ser alterado
                retorno = objTipo.alterar()

            if retorno > 0:
                return '''
                    <script>
                        alert("O tipo %s foi armazenado no banco de dados.");
                        window.location.href = "/pgTipo";
                    </script>
                ''' % (txtNome)
            else:
                return '''
                    Erro ao armazenar o tipo <b>%s</b>.<br />
                    <a href="/">Voltar</a>
                ''' % (txtNome)
        else:
            return '''
                O nome do tipo precisa ser informado.<br />
                <a href="/">Voltar</a>
            '''

    @cherrypy.expose()
    def excluirTipo(self,idTipo):
        objTipo = Tipo()
        objTipo.set_id(int(idTipo))
        if objTipo.excluir() > 0:
            raise cherrypy.HTTPRedirect("/pgTipo")#redireciona para a rota indicada no HTTPRedirect
        else:
            return '''
                <p>Não foi possível excluir o Tipo de Anúncio...<p>
                <p>[<a href="/">Voltar</a>]
            '''

    @cherrypy.expose()
    def alterarTipo(self,idTipo): #recupera no banco o dado a ser alterado e o prepara no formulário
        objTipo = Tipo()
        #objTipo.set_id(int(idTipo))
        dados = objTipo.obterTipo(idTipo)
        return self.montaFormulario(dados[0]["id"], dados[0]["nome"])
