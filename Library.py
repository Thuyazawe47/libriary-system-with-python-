from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5 import QtWidgets,uic
import sys 
import mysql.connector as sql

class library(QDialog):
    def __init__(self):
        super(library,self).__init__()
        self.bookdb=None #  deafault to db 
        uic.loadUi("library.ui",self)
        self.searchbut.clicked.connect(self.search)
        self.tableView.clicked.connect(self.Tableselect)
        self.butupdate.clicked.connect(self.update)


    def update(self):# we need to catch index and value because it was table 
        index=self.tableView.selectionModel().currentIndex()
        value=index.sibling(index.row(),index.column()).data()
        self.setVisible(False)
        from updateform import Updateform
        ui=Updateform(value)
        ui.show()
        ui.exec_()


    def Tableselect(self):
        self.butupdate.setEnabled(True)# activate but when clicked on table value


    


    def search(self):
        choosetype=None#it become two data type catch cause radio but
        inputtype=None
        if self.authorradio.isChecked():
            choosetype="author"
        elif self.titleradio.isChecked():
            choosetype="title"
        else:
            choosetype="publisher"
        inputtype=self.inputtxt.toPlainText().strip()
        print(choosetype)
        print(inputtype)
        sql_str="select * from book_tb where "+choosetype+" = '"+inputtype+"'" # we write with +___+ cuz it was variable and note second  inputtype need single quote after  double
        print(sql_str)

        self.dbconnect1()
        self.cursor1=self.bookdb.cursor()
        self.cursor1.execute(sql_str)
        rows=self.cursor1.fetchall()
        

        if len(rows)==0:
            from PyQt5.QtWidgets import QMessageBox
            mesg=QMessageBox()
            mesg.setIcon(QMessageBox.Critical)
            mesg.setText("Your information is not found,Try searching another")
            mesg.setWindowTitle("No Data")
            mesg.exec_()
        
        else:
           import pandas as pd # pandas use data frame type and mysql check below
           
           sql_pd=pd.read_sql(sql_str,self.bookdb)# change format sql to panda
           df=pd.DataFrame(sql_pd,columns=["id","bookid","title","author","publisher","published_year","no_of_copies","left_copies"])
           from TableModel import pandasModel
           model=pandasModel(df)
           self.tableView.setModel(model)

           """ #Plain Text if used  my sql use list represnt as role ,tuple represent column in mysql 
            for x in rows:#when we take data query from sql it get list close tuple
                for y in range (len(x)):# len(x) represent for column in data structure of list close tuple coulmn same as index or Room 
                self.obj name of plaintext.appendPlainText(str(x[y]))# check here y is x of index     
"""

               


             

 

    
    def dbconnect1(self):

        try:#try to know error
            self.bookdb=sql.connect(


                host="localhost",
                username="root",
                password="root",
                database="librarydb"
        )
            
        except:
            print("db error connection")





"""
if __name__=="__main__":#it need only one for whole project it connect sub into main system.but it needs  while  coding subsys and need to test spcific sub sys 
   app=QtWidgets.QApplication([])
   win=library()
   win.show()
   sys.exit(win.exec_())
"""