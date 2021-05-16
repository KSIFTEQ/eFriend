import pdb
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton
from PyQt5.QAxContainer import QAxWidget
from collections import defaultdict
import pandas as pd

class Login(QMainWindow):
    def __init__(self):
        self.acct_no  = None
        self.acct_pwd = None

        self.app =  QApplication(sys.argv)   
        super().__init__()  
        self.setWindowTitle("계좌정보입력")
        self.setGeometry(300, 300, 320, 120)

        self.acct_no = None
        label = QLabel("계좌번호( - 제외) ", self)
        label.move(10,20)

        self.enter_acct = QLineEdit(self)
        self.enter_acct.move(100, 20)

        self.acct_pwd = None
        label = QLabel("계좌비밀번호 ", self)
        label.move(10,60)

        self.enter_pwd = QLineEdit(self)
        self.enter_pwd.setEchoMode(QLineEdit.Password)
        self.enter_pwd.move(100, 60)

        button = QPushButton("입력", self)
        button.move(210,60)
        self.show()
        button.clicked.connect(self.__get_acct_info)     
        button.clicked.connect(self.close)
        self.app.exec_()   
          
    def __get_acct_info(self):
        self.acct_no  = self.enter_acct.text()
        self.acct_pwd = self.enter_pwd.text() 

class Portfolio:
    def __init__(self, Login):
        self.df = None
        self.acct_no  = Login.acct_no
        self.acct_pwd = Login.acct_pwd        
        self.__request_SATPS()

    def __request_SATPS(self):
        self.conn = QAxWidget("ITGExpertCtl.ITGExpertCtlCtrl.1")
        self.conn.SetSingleData(0, self.acct_no[:-2])
        self.conn.SetSingleData(1, self.acct_no[-2:])       
        self.conn.SetSingleData(2, self.conn.GetEncryptPassword(self.acct_pwd))
        self.conn.SetSingleData(3, "N")
        self.conn.SetSingleData(4, "N")
        self.conn.SetSingleData(5, "02")
        self.conn.SetSingleData(6, "01")
        self.conn.SetSingleData(7, "N")
        self.conn.SetSingleData(8, "N")
        self.conn.SetSingleData(9, "01")
        self.conn.RequestData("SATPS")
        self.conn.ReceiveData.connect(self.__conn_receivedata)  
        input("Enter!")

    def __conn_receivedata(self):
        dict_SATPS = {
            0  : "종목코드",
            1  : "종목명",
            7  : "보유수량",
            9  : "매입평균가격",
            10 : "매입금액",
            11 : "현재가",
            12 : "평가금액",
            13 : "평가손익금액",
            14 : "평가손익율",
        }
        dict_acct = defaultdict(list)
        for i in range(0, self.conn.GetMultiRecordCount(0)):
            for j in dict_SATPS:
                data = self.conn.GetMultiData(0, i, j, 0)
                dict_acct[dict_SATPS[j]].append(data)

        self.df = pd.DataFrame(dict_acct)

class Transactions:
    def __init__(self, Login):
        self.df = None
        self.acct_no  = Login.acct_no
        self.acct_pwd = Login.acct_pwd
        self.__request_SDOC()

    def __request_SDOC(self):
        self.conn = QAxWidget("ITGExpertCtl.ITGExpertCtlCtrl.1")
        self.conn.SetSingleData(0, self.acct_no[:-2])
        self.conn.SetSingleData(1, self.acct_no[-2:])        
        self.conn.SetSingleData(2,self.conn.GetEncryptPassword(self.acct_pwd))
        self.conn.SetSingleData(3, "20200101")
        self.conn.SetSingleData(4, "20210331")
        self.conn.SetSingleData(5, "00")
        self.conn.SetSingleData(6, "00")
        self.conn.SetSingleData(8, "01")
        self.conn.SetSingleData(11, "00")
        self.conn.RequestData("SDOC")
        self.conn.ReceiveData.connect(self.__conn_receivedata)  
        input("Enter!")
        
    def __conn_receivedata(self):
        dict_SDOC = {
            0  : "주문일자",
            4  : "주문구분명",
            6  : "매도매수구분코드명",
            7  : "상품번호",
            8  : "상품명",
            9  : "주문수량",
            10 : "주문단가",
            11 : "주문시각",
            12 : "총체결수량",
            13 : "평균가",
            15 : "총체결금액",
        }
        dict_acct = defaultdict(list)
        for i in range(0, self.conn.GetMultiRecordCount(0)):
            for j in dict_SDOC:
                data = self.conn.GetMultiData(0, i, j, 0)
                dict_acct[dict_SDOC[j]].append(data)

        self.df = pd.DataFrame(dict_acct)