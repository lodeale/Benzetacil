# -*- coding: utf-8 -*-
#!/usr/bin/env python
# ejemplo entry.py
import pygtk
pygtk.require('2.0')
import gtk
import hack

###################### ventana ####################
class Main:
    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_border_width(5)
        self.window.set_size_request(500, 500)
        self.window.set_title("Benzetacil GTK v01")
        self.window.connect("delete_event", lambda w,e: gtk.main_quit())

        #Creo la tabla
        self.table = gtk.Table(10, 10, True)

        #Creo el lable URL
        self.label1 = gtk.Label("URL:")

        #Creo la caja de texto para la URL
        self.url = gtk.Entry()
        self.url.set_max_length(100)
        self.url.connect("activate", self.enter_callback, self.url)
        self.url.set_text("http://127.0.0.1/blindSQL/index.php?id_n=2")
        self.url.select_region(0, len(self.url.get_text()))

        #Creo la caja de texto para el output
        self.salida = gtk.TextView()
        self.salida.set_property('editable', False)
        self.buffer = self.salida.get_buffer()

        #Creo el boton conectar
        self.buttonRun = gtk.Button("Run")
        self.buttonRun.connect("clicked", self.conectar)

        #Creo el boton de sacar Tabla
        self.buttonST = gtk.Button("Tablas")
        self.buttonST.connect("clicked",self.conectarTablas)

        #Creo el boton de sacar Registros
        self.buttonSR = gtk.Button("Registros")
        self.buttonSR.connect("clicked",self.conectarRegistro)

        #creo un separador
        self.separator = gtk.HSeparator()

        #Creo un boton de exit
        self.buttonQuit = gtk.Button(stock=gtk.STOCK_CLOSE)
        self.buttonQuit.connect("clicked", lambda w: gtk.main_quit())

        #agrego el combo para econtrar errores
        self.combo = gtk.Combo()
        slist = ["Compara fuentes","Busca Patron"]
        self.combo.set_popdown_strings(slist)

        #agrego el combo para el methodo
        self.comboM = gtk.Combo()
        mlist = ["GET","POST"]
        self.comboM.set_popdown_strings(mlist)

        #creo un scroll window en un pack verticl
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.vbox=gtk.VBox(False,1)
        self.vbox.pack_start(scrolled_window, gtk.TRUE, gtk.TRUE, 0)
        scrolled_window.add_with_viewport(self.salida)

        #agrego los widgets
        self.window.add(self.table)

        self.table.attach(self.label1,0,1,0,1)
        self.table.attach(self.url,1,9,0,1)
        self.table.attach(self.buttonRun,9,10,0,1)
        self.table.attach(self.combo,0,3,1,2)
        self.table.attach(self.comboM,3,5,1,2)
        self.table.attach(self.buttonST,6,7,1,2)
        self.table.attach(self.buttonSR,7,8,1,2)
        self.table.attach(self.separator,0,10,2,3)
        self.table.attach(self.vbox,0,10,3,9)
        self.table.attach(self.buttonQuit,0,2,9,10)


        #muestrando
        self.window.show_all()


    def enter_callback(self, widget, url):
        entry_text = self.url.get_text()
        print "Entry contents: %s\n" % entry_text

    def conectarRegistro(self,widget):
        self.buffer.insert(self.buffer.get_end_iter(),"\n\n[------ [Registros!]------]\n")
        methodError = self.combo.entry.get_text()
        method = self.comboM.entry.get_text()
        #for db in range(0,len(self.bbddE)):
        obj3 = hack.atack(self.url.get_text(),self.bbddE,self.tablaE)


    def conectarTablas(self,widget):
        self.buffer.insert(self.buffer.get_end_iter(),"\n\n[------ [tablas!]------]\n")
        methodError = self.combo.entry.get_text()
        method = self.comboM.entry.get_text()
        #for db in range(0,len(self.bbddE)):
        obj2 = hack.atack(self.url.get_text(),self.bbddE,"")
        obj2.injBlind()
        tablaE = obj2.runBlind(methodError)
        for x in range(0,len(tablaE)):
            self.buffer.insert(self.buffer.get_end_iter(),"\n[+]"+tablaE[x])

    def conectar(self, widget):
        self.bbddE = ""
        #Se crea una instancia del modulo hack
        #la clase injection que es herencia de
        #la clase sitex.
        methodError = self.combo.entry.get_text()
        method = self.comboM.entry.get_text()
        obj = hack.atack(self.url.get_text(),"","")
        self.buffer.insert(self.buffer.get_end_iter(),obj.method(method))
        self.buffer.insert(self.buffer.get_end_iter(),obj.vulnerable())
        self.buffer.insert(self.buffer.get_end_iter(),"\n\n[------ [base de datos!]------]\n")
        obj.injBlindBBDD()
        self.bbddE = obj.runBlindBBDD(methodError)
        self.buffer.insert(self.buffer.get_end_iter(),"\n[+]"+self.bbddE)


if __name__ == "__main__":
    app = Main()
    gtk.main()

