from PyQt5 import QtWidgets,uic
from PyQt5.QtWidgets import QDialog
import sys
import mysql.connector as sql

class Updateform(QDialog):# with respect bookid cuz we take bookid from library
    def __init__(self,bid):# bid exists in order to  carry data from library code
        super(Updateform,self).__init__()
        self.bookdb=None#not to miss used db make none default

        uic.loadUi("updateFormui.ui",self)
        print("The Book id is :"+str(bid))
        self.LoadData(bid)# load data  that fetch from library code default show when pop up
        self.updatebut.clicked.connect(self.update)
        self.insertbut.clicked.connect(self.insert)
        self.deletebut.clicked.connect(self.delete)
        self.clearbut.clicked.connect(self.clear)


    def update(self):#take  cuz update 
        id=self.bookid.toPlainText()
        title=self.title.toPlainText()
        author=self.author.toPlainText()
        publisher=self.publisher.toPlainText()
        copy=self.nocp.toPlainText()
        leftcopy=self.lcp.toPlainText()
        self.dbconnect1()
        cursor=self.bookdb.cursor()
        sql_update="update book_tb set title=%s,author=%s,publisher=%s,no_of_copies=%s,left_copies=%s where bookid="+str(id)#sql column name used for update and str(id)no need to in quotes cuz str make
        value=(title,author,publisher,copy,leftcopy)#in sql we use direct value here but there use variable to catch data update
        cursor.execute(sql_update,value)
        self.bookdb.commit()
        self.showmesg("updated sucessfully","ok")

    def showmesg(self,title ,body):   
        from PyQt5.QtWidgets import QMessageBox
        msg=QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(body)
        msg.setWindowTitle(title)
        msg.exec_()
    

    def insert(self):
        id=self.bookid.toPlainText()
        title=self.title.toPlainText()
        author=self.author.toPlainText()
        publisher=self.publisher.toPlainText()
        copy=self.nocp.toPlainText()
        leftcopy=self.lcp.toPlainText()
        self.dbconnect1()
        cursor=self.bookdb.cursor()
        sql_insert="insert into book_tb (bookid,title,author,publisher,no_of_copies,left_copies) values(%s,%s,%s,%s,%s,%s)"
        value=(id,title,author,publisher,copy,leftcopy)
        cursor.execute(sql_insert,value)
        self.bookdb.commit()
        self.clear()
        self.showmesg("inserted sucessfully","ok")

        
    

   
    def delete(self):
        id=self.bookid.toPlainText()
        if len(id)==0:
            self.showmesg("deleted sucessfully","ok")
        else:
            self.dbconnect1()
            cursor=self.bookdb.cursor()
            delete_str="delete from book_tb where bookid="+str(id)
            cursor.execute(delete_str)
            self.bookdb.commit()
            self.clear()
            self.showmesg("deleted sucessfully","ok")





        
    

    
    def clear(self):
        self.bookid.setPlainText("")# ""it means no data here
        self.title.setPlainText("")
        self.author.setPlainText("")
        self.publisher.setPlainText("")
        self.nocp.setPlainText("")
        self.lcp.setPlainText("")

        
    








    def LoadData(self,bid):# bid belong cuz it need to load by this
        self.dbconnect1()#load data take bookid as bid and use it to search and show
        sql="select * from book_tb where bookid="+str(bid)# in python str + num  is srror
        self.cursor=self.bookdb.cursor()
        self.cursor.execute(sql)
        values=self.cursor.fetchone()# value get int for num
        self.bookid.setPlainText(str(values[1]))# in num we need to make str cuz set text accept str
        self.title.setPlainText(values[2])
        self.author.setPlainText(values[3])
        self.publisher.setPlainText(values[4])
        self.nocp.setPlainText(str(values[5]))
        self.lcp.setPlainText(str(values[7]))


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


if __name__=="__main__":
    app=QtWidgets.QApplication([])
    win=Updateform(1234)# 1234 is manually fill data from mysql in order to run  alone this file
    win.show()
    sys.exit(win.exec_())
