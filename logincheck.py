from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QIcon,QPixmap
from PyQt5 import QtWidgets,uic
import sys

class logincheck(QDialog):
    def __init__(self):
        super(logincheck,self).__init__()
        uic.loadUi("login.ui",self)
        self.iconlabel.setPixmap(QPixmap("login.jpg"))
        self.iconlabel.setScaledContents(True)
        self.butlogin.clicked.connect(self.loginfun)
        self.butclose.clicked.connect(self.closefun)     
 
    def loginfun(self):
        username=self.usernametxt.toPlainText().strip()
        password=self.passwordtxt.text().strip()
        self.dbconnect()
        self.cursor=self.db.cursor()
        self.cursor.execute("select * from login_tb")
        rows=self.cursor.fetchall()
        found=0
        for x in rows:
            usr=x[1]
            pwd=x[2]
            if username==usr and password==pwd:
                print("sucessful")
                found=1
                self.setVisible(False)# it hides login form after sucess log in 
                from Library import library  #it is needed to connect with library code
                lib=library()
                lib.show()
                lib.exec_()
        if found==0:
            from PyQt5.QtWidgets import QMessageBox
            msg=QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("login unsucessful.Try Again ")
            msg.setWindowTitle("Error Login")
            msg.exec_()


        #db connect and query
    def dbconnect(self):
        import mysql.connector as sq
        try:
            self.db=sq.connect (
                                host="localhost",
                                username="root",
                                password="root",
                                database="librarydb"
                                )
        except:
               print("db connection error ")  
    
    
    
    
    
    def closefun(self):
        sys.exit(win.exec_())             
        





if __name__=="__main__":
   app=QtWidgets.QApplication([])
   win=logincheck()
   win.show()
   sys.exit(win.exec_())