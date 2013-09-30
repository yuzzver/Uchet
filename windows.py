# -*- coding: utf-8 -*-
__author__ = 'Bondarenko Yura'
import sys
from all import modelInfo, dateEdit
from PyQt4 import QtCore, QtGui
from datetime import date

class models():
    def __init__(self, parent=None):
        if parent!=None:
            try:
                self.model=parent.model
            except Exception:
                self.show()
                dialogError(self, "Не заданна модель")
                return False
            else:
                return True
        else:
            self.show()
            dialogError(self, "Нет родителя")
            return False

class addDetail(QtGui.QDialog, models):
    def __init__(self, parent=None, table=None, title=None, subCombo=None):
        QtGui.QDialog.__init__(self,parent)
        self.setModal(True)
        if models.__init__(self,parent):
            self.setWindowTitle('"АвтоПарк" Добавление детали на склад')
            self.detailLabel=QtGui.QLabel("Найменование")
            self.detail=self.model.loadCatalogCombo()
            self.priceLabel=QtGui.QLabel("Цена")
            self.price=QtGui.QLineEdit()
            dateIn=date.today()
            self.dateLabel=QtGui.QLabel("Дата покупки")
            self.dateBay=QtGui.QDateEdit(QtCore.QDate(dateIn.year, dateIn.month, dateIn.day))
            self.paymentLabel=QtGui.QLabel("Способ оплаты")
            self.payment=self.model.loadPaymentCombo()
            self.numberLabel=QtGui.QLabel("Количество")
            self.number=QtGui.QLineEdit()
            self.btnAdd=QtGui.QPushButton("Добавить")
            self.btnAdd.clicked.connect(self.save)
            self.btnCancel=QtGui.QPushButton("Отмена")
            self.btnCancel.clicked.connect(self.close)
            self.btnLayout=QtGui.QHBoxLayout()
            self.btnLayout.addWidget(self.btnCancel)
            self.btnLayout.addWidget(self.btnAdd)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.detailLabel,0,0)
            self.layout.addWidget(self.detail,0,1)
            self.layout.addWidget(self.priceLabel,1,0)
            self.layout.addWidget(self.price,1,1)
            self.layout.addWidget(self.paymentLabel,2,0)
            self.layout.addWidget(self.payment,2,1)
            self.layout.addWidget(self.numberLabel,3,0)
            self.layout.addWidget(self.number,3,1)
            self.layout.addWidget(self.dateLabel,4,0)
            self.layout.addWidget(self.dateBay,4,1)
            self.layout.addLayout(self.btnLayout,5,0,1,2)
            self.setLayout(self.layout)
            self.show()
    def save(self):
        number=int(self.number.text())
        dateBay=self.dateBay.date().toPyDate()
        price=self.price.text()
        self.model.addDetail(number, dateBay, price)
        self.close()

class subDetail(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setModal(True)
        if models.__init__(self,parent):
            self.setWindowTitle('"АвтоПарк" Перечень деталей')
            self.table=self.model.loadNewDetailSubTable()
            self.btnOk=QtGui.QPushButton("Ок")
            self.btnOk.clicked.connect(self.close)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.table)
            self.layout.addWidget(self.btnOk)
            self.setLayout(self.layout)
            self.show()

class addWidget(QtGui.QDialog, models):
    def __init__(self, parent=None, table=None, title=None, subCombo=None):
        QtGui.QDialog.__init__(self,parent)
        self.setModal(True)
        if table==None or models.__init__(self,parent)==False:
            self.setWindowTitle('"АвтоПарк" Ошибка')
            self.label=QtGui.QLabel("Не задана таблица")
            self.btnClose=QtGui.QPushButton("Ок")
            self.btnClose.clicked.connect(self.close)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.btnClose)
        else:
            self.setWindowTitle('"АвтоПарк" {0}'.format(title))
            self.layout=QtGui.QVBoxLayout()
            self.btnLayout=QtGui.QHBoxLayout()
            self.table=table
            self.text=QtGui.QLineEdit()
            self.btnAdd=QtGui.QPushButton("Добавить")
            self.btnAdd.clicked.connect(self.save)
            self.btnDel=QtGui.QPushButton("Удалить")
            self.btnDel.clicked.connect(self.table.delRow)
            self.btnLayout.addWidget(self.btnAdd)
            self.btnLayout.addWidget(self.btnDel)
            self.layout.addWidget(self.table)
            if subCombo!=None:
                self.subCombo=subCombo
                self.layout.addWidget(self.subCombo)
            self.layout.addWidget(self.text)
            self.layout.addLayout(self.btnLayout)
        self.setLayout(self.layout)
        self.show()
    def save(self):
        self.model.keys["info"]=self.text.text()
        self.table.addRow(self.model.keys)
        self.text.setText("")

class addAccess(addWidget):
    def __init__(self, parent):
        addWidget.__init__(self, parent, parent.model.loadAccessTable(), "Права доступа", None)
        self.btnAdd.clicked.connect(self.newAccess)
        self.table.doubleClicked.connect(lambda: setAccess(self))
    def newAccess(self):
        self.model.loadLastAccess()
        setAccess(self)

class setAccess(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Набора прав доступа')
            self.label=QtGui.QLabel("Создание набора правил {0}".format("parent.text.text()"))
            self.label1=QtGui.QLabel("Машины")
            self.label2=QtGui.QLabel("Ремонты")
            self.label3=QtGui.QLabel("Работники")
            self.label4=QtGui.QLabel("Детали")
            self.label5=QtGui.QLabel("Системные")
            self.label6=QtGui.QLabel("Удаление")
            self.label7=QtGui.QLabel("Просмотр")
            self.label8=QtGui.QLabel("Изменения")
            self.check1=QtGui.QCheckBox()
            self.check2=QtGui.QCheckBox()
            self.check3=QtGui.QCheckBox()
            self.check4=QtGui.QCheckBox()
            self.check5=QtGui.QCheckBox()
            self.check6=QtGui.QCheckBox()
            self.check7=QtGui.QCheckBox()
            self.check8=QtGui.QCheckBox()
            self.check9=QtGui.QCheckBox()
            self.check10=QtGui.QCheckBox()
            self.check11=QtGui.QCheckBox()
            self.btnSave=QtGui.QPushButton("Сохранить")
            self.btnSave.clicked.connect(self.save)
            self.btnCancel=QtGui.QPushButton("Отмена")
            self.btnCancel.clicked.connect(self.close)
            self.layoutBtn=QtGui.QHBoxLayout()
            self.layoutBtn.addWidget(self.btnCancel)
            self.layoutBtn.addWidget(self.btnSave)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label, 0,0,1,6)
            self.layout.addWidget(self.label1, 1,1)
            self.layout.addWidget(self.label2, 1,2)
            self.layout.addWidget(self.label3, 1,3)
            self.layout.addWidget(self.label4, 1,4)
            self.layout.addWidget(self.label5, 1,5)
            self.layout.addWidget(self.label6, 1,6)
            self.layout.addWidget(self.label7, 2,0)
            self.layout.addWidget(self.label8, 3,0)
            self.layout.addWidget(self.check1, 2,1)
            self.layout.addWidget(self.check2, 3,1)
            self.layout.addWidget(self.check3, 2,2)
            self.layout.addWidget(self.check4, 3,2)
            self.layout.addWidget(self.check5, 2,3)
            self.layout.addWidget(self.check6, 3,3)
            self.layout.addWidget(self.check7, 2,4)
            self.layout.addWidget(self.check8, 3,4)
            self.layout.addWidget(self.check9, 2,5)
            self.layout.addWidget(self.check10, 3,5)
            self.layout.addWidget(self.check11, 2,6,2,1)
            self.layout.addLayout(self.layoutBtn, 4,4,1,3)
            self.setLayout(self.layout)
            self.setCheckState()
            self.show()
    def setCheckState(self):
        for i in range(1,12):
            try:
                state=self.model.keys["access{0}".format(i-1)]
            except KeyError:
                getattr(self, "check{0}".format(i)).setCheckState(0)
            else:
                getattr(self, "check{0}".format(i)).setCheckState(state)
    def save(self):
        for i in range(1, 12):
            self.model.keys["access{0}".format(i)]=getattr(self, "check{0}".format(i)).checkState()
        self.model.setAccess()
        self.close()

class addTimeWork(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        self.setModal(True)
        if models.__init__(self,parent):
            self.setWindowTitle('"АвтоПарк" Должности работников')
            self.layout=QtGui.QVBoxLayout()
            self.btnLayout=QtGui.QHBoxLayout()
            self.table=self.model.loadTimeWorkTable()
            self.table.doubleClicked.connect(lambda: setTimeWork(self,True))
            self.btnAdd=QtGui.QPushButton("Добавить")
            self.btnAdd.clicked.connect(lambda: setTimeWork(self))
            self.btnDel=QtGui.QPushButton("Удалить")
            self.btnDel.clicked.connect(self.table.delRow)
            self.btnLayout.addWidget(self.btnAdd)
            self.btnLayout.addWidget(self.btnDel)
            self.layout.addWidget(self.table)
            self.layout.addLayout(self.btnLayout)
            self.setLayout(self.layout)
        self.show()

class setTimeWork(QtGui.QDialog, models):
    def __init__(self, parent=None, update=False):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.update=update
            self.labelWorker=QtGui.QLabel("Работник")
            self.workerCombo=self.model.loadAllWorkerCombo()
            self.labelPost=QtGui.QLabel("Долженость")
            self.postCombo=self.model.loadPostCombo()
            self.labelDateOut=QtGui.QLabel("Дата снятия")
            self.dateOut=QtGui.QDateEdit()
            if update:
                dateIn=self.model.keys["dateIn"]
            else:
                dateIn=date.today()
                self.dateOut.setReadOnly(True)
            self.labelDateIn=QtGui.QLabel("Дата принятия")
            self.dateIn=QtGui.QDateEdit(QtCore.QDate(dateIn.year, dateIn.month, dateIn.day))
            self.btnSave=QtGui.QPushButton("Сохранить")
            self.btnCancel=QtGui.QPushButton("Отмена")
            self.btnLayout=QtGui.QHBoxLayout()
            self.btnLayout.addWidget(self.btnCancel)
            self.btnCancel.clicked.connect(self.close)
            self.btnLayout.addWidget(self.btnSave)
            self.btnSave.clicked.connect(self.save)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.labelWorker,0,0)
            self.layout.addWidget(self.workerCombo,0,1)
            self.layout.addWidget(self.labelPost,1,0)
            self.layout.addWidget(self.postCombo,1,1)
            self.layout.addWidget(self.labelDateIn,2,0)
            self.layout.addWidget(self.dateIn,2,1)
            self.layout.addWidget(self.labelDateOut,3,0)
            self.layout.addWidget(self.dateOut,3,1)
            self.layout.addLayout(self.btnLayout,4,0,1,2)
            self.setLayout(self.layout)
            self.show()
    def save(self):
        dateIn=self.dateIn.date().toPyDate()
        if self.update:
            dateOut=self.dateOut.date().toPyDate()
            if dateOut<dateIn:
                dialogError(self,"Указана не коректная дата\nснятия с должности.")
            else:
                self.model.setTimeWork(dateIn, dateOut)
                self.close()
        else:
            self.model.setTimeWork(dateIn)
            self.close()

class setPassword(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        if models.__init__(self, parent):
            self.userLabel=QtGui.QLabel("Работники")
            self.user=self.model.loadAllWorkerCombo()
            self.passLabel1=QtGui.QLabel("Новый пароль")
            self.password1=QtGui.QLineEdit()
            self.password1.setEchoMode(QtGui.QLineEdit.Password)
            self.password2=QtGui.QLineEdit()
            self.passLabel2=QtGui.QLabel("Подтверждение пароля")
            self.password2.setEchoMode(QtGui.QLineEdit.Password)
            self.btnSave=QtGui.QPushButton("Ок")
            self.btnSave.clicked.connect(self.save)
            self.btnCancel=QtGui.QPushButton("Отменить")
            self.btnCancel.clicked.connect(self.close)
            self.btnLayout=QtGui.QHBoxLayout()
            self.btnLayout.addWidget(self.btnCancel)
            self.btnLayout.addWidget(self.btnSave)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.userLabel,0,0)
            self.layout.addWidget(self.user,0,1)
            self.layout.addWidget(self.passLabel1,1,0)
            self.layout.addWidget(self.password1,1,1)
            self.layout.addWidget(self.passLabel2,2,0)
            self.layout.addWidget(self.password2,2,1)
            self.layout.addLayout(self.btnLayout,3,0,1,2)
            self.setLayout(self.layout)
            self.show()
    def save(self):
        pass1=self.password1.text()
        pass2=self.password2.text()
        if pass1==pass2:
            self.model.setPassword(pass1)
            self.close()
        else:
            dialogError(self, "Пароли не совпадают")

class dialogWindows(QtGui.QDialog):
#Родитель диалоговых окон. Реализует 2 кнопки(ok, cancel)
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        self.label=QtGui.QLabel("")
        self.btnYes=QtGui.QPushButton("Да")
        self.btnNo=QtGui.QPushButton("Отмена")
        self.btnYes.clicked.connect(self.accept)
        self.btnNo.clicked.connect(self.reject)
        self.layout=QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layoutBtn=QtGui.QHBoxLayout()
        self.layoutBtn.addWidget(self.btnNo)
        self.layoutBtn.addWidget(self.btnYes)
        self.layout.addLayout(self.layoutBtn)
        self.setLayout(self.layout)

class carDeleteWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            label=QtGui.QLabel("""
            Удаление машины повлечет за собой каскадное удаление
            информации:
                -произведеных ремонтов;
                -устаноавленых деталях;
                -водителях и периодах вождения.
            После удаления эту информацию невозможно будет
            восстановить.""")
            self.btnDel=QtGui.QPushButton("Удалить")
            self.btnDel.clicked.connect(self.delete)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(label)
            self.layout.addWidget(self.btnDel)
            self.setLayout(self.layout)
    def delete(self):
        dialog=dialogWindows(self)
        dialog.label.setText("Вы уверены что хотите удалить\nэту машину с базы данных??")
        dialog.btnYes.setText("Да")
        dialog.show()
        result=dialog.exec_()
        if result==QtGui.QDialog.Accepted:
            self.model.deleteCar()
            self.parentWidget().parentWidget().parentWidget().close()

class detailsWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Перечень всех деталей")
            self.btnAdd=QtGui.QPushButton("Добавить детали на склад")
            self.btnAdd.clicked.connect(lambda: addDetail(self))
            self.tab=QtGui.QTabWidget()
            self.newDetail=self.model.loadNewDetailTable()
            self.newDetail.doubleClicked.connect(lambda: subDetail(self))
            self.useDetail=self.model.loadUseDetailTable()
            self.unfitDetail=self.model.loadUnfitDetailTable()
            self.tab.addTab(self.newDetail, "Детали на складе")
            self.tab.addTab(self.useDetail, "Установленные детали")
            self.tab.addTab(self.unfitDetail, "Списанные детали")
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,14)
            self.layout.addWidget(self.btnAdd,0,14,1,1)
            self.layout.addWidget(self.tab,1,0,15,15)
            self.setLayout(self.layout)

class repairCar(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Ремонт машины')
            self.label=QtGui.QLabel("Произвести ремонт/обслуживание машины")
            self.carLabel=QtGui.QLabel("Машина")
            self.carCombo=self.model.loadCarCombo()
            self.mechanicLabel=QtGui.QLabel("Механик")
            self.mechanicCombo=self.model.loadMechanicCombo()
            self.classLabel=QtGui.QLabel("Класс ремонта")
            self.classCombo=self.model.loadRepairClassCombo()
            self.typeLabel=QtGui.QLabel("Тип ремонта")
            self.typeCombo=self.model.loadRepairTypeCombo()
            self.dateLabel=QtGui.QLabel("Дата ремонта")
            self.dateLine=QtGui.QDateEdit()
            self.priceLabel=QtGui.QLabel("Цена ремонта")
            self.priceLine=QtGui.QLineEdit()
            self.detailsLabel=QtGui.QLabel("Детали необхотимые для ремонта или обслуживания:")
            self.detailsTable=self.model.loadNewDetailInstallTable()
            self.saveBtn=QtGui.QPushButton("Сохранить")
            self.clrBtn=QtGui.QPushButton("Отменить")
            self.layoutBtn=QtGui.QHBoxLayout()
            self.layoutBtn.addWidget(self.saveBtn)
            self.saveBtn.clicked.connect(self.addRepair)
            self.layoutBtn.addWidget(self.clrBtn)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,5)
            self.layout.addWidget(self.carLabel,1,0,1,1)
            self.layout.addWidget(self.carCombo,1,1,1,5)
            self.layout.addWidget(self.mechanicLabel,1,6,1,1)
            self.layout.addWidget(self.mechanicCombo,1,7,1,5)
            self.layout.addWidget(self.classLabel,2,0,1,1)
            self.layout.addWidget(self.classCombo,2,1,1,5)
            self.layout.addWidget(self.typeLabel,2,6,1,1)
            self.layout.addWidget(self.typeCombo,2,7,1,5)
            self.layout.addWidget(self.dateLabel,3,0,1,1)
            self.layout.addWidget(self.dateLine,3,1,1,5)
            self.layout.addWidget(self.priceLabel,3,6,1,1)
            self.layout.addWidget(self.priceLine,3,7,1,5)
            self.layout.addWidget(self.detailsLabel,4,0,1,12)
            self.layout.addWidget(self.detailsTable,5,0,12,12)
            self.layout.addLayout(self.layoutBtn,17,0,1,12)
            self.setLayout(self.layout)
            self.open()
    def addRepair(self):
        keys={"date":self.dateLine.date().toPyDate(),
              "price":self.priceLine.text()}
        self.model.addRepair(keys)
        self.close()

class repairsWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Произведенные ремонты и обслуживания машин")
            self.repairTable=self.model.loadRepairTable()
            self.reportBtn=QtGui.QPushButton("Отчеты")
            self.repairBtn=QtGui.QPushButton("Произвести ремонт")
            self.repairBtn.clicked.connect(lambda: repairCar(self))
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,7)
            self.layout.addWidget(self.reportBtn,0,13)
            self.layout.addWidget(self.repairBtn,0,14)
            self.layout.addWidget(self.repairTable,1,0,15,15)
            self.setLayout(self.layout)

class workersWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Сотрудники предприятия")
            self.addWorkerBtn=QtGui.QPushButton("Добавить сотрудника")
            self.addWorkerBtn.clicked.connect(lambda: addWorkerWidget(self))
            self.tab=QtGui.QTabWidget()
            self.workerTable=self.model.loadWorkerTable()
            self.workerTable.doubleClicked.connect(lambda: workerWidget(self))
            self.formerWorkersTab=self.model.loadFormerWorkerTable()
            self.formerWorkersTab.doubleClicked.connect(lambda: workerWidget(self))
            self.tab.addTab(self.workerTable, "Сотрудники")
            self.tab.addTab(self.formerWorkersTab, "Бывшие сотрутники")
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,7)
            self.layout.addWidget(self.addWorkerBtn,0,14,1,1)
            self.layout.addWidget(self.tab,1,0,15,15)
            self.setLayout(self.layout)

class workerWidget(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.tab=QtGui.QTabWidget()
            self.workInfo=workerInfoWidget(self)
            self.workerCar=workerCarWidget(self)
            self.workerRepair=workerRepairWidget(self)
            self.workerDelete=workerDeleteWidget(self)
            self.tab.addTab(self.workInfo, "Общая информация")
            self.tab.addTab(self.workerCar, "Машины")
            self.tab.addTab(self.workerRepair, "Ремонты и обслуживания")
            self.tab.addTab(self.workerDelete, "Удаление")
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.tab)
            self.setLayout(self.layout)
            self.show()

class workerInfo(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.name1Label=QtGui.QLabel("Имя")
            self.name1=QtGui.QLineEdit()
            self.name2Label=QtGui.QLabel("Фамилия")
            self.name2=QtGui.QLineEdit()
            self.name3Label=QtGui.QLabel("Отчество")
            self.name3=QtGui.QLineEdit()
            self.passportLabel=QtGui.QLabel("Паспорт")
            self.passport=QtGui.QTextEdit()
            self.addressRegLabel=QtGui.QLabel("Адрес прописки")
            self.addressReg=QtGui.QLineEdit()
            self.addressResLabel=QtGui.QLabel("Адрес проживания")
            self.addressRes=QtGui.QLineEdit()
            self.phoneMobLabel=QtGui.QLabel("Моб. тел.")
            self.phoneMob=QtGui.QLineEdit()
            self.phoneHomeLabel=QtGui.QLabel("Дом. тел.")
            self.phoneHome=QtGui.QLineEdit()
            self.eMailLabel=QtGui.QLabel("e-mail")
            self.eMail=QtGui.QLineEdit()
            self.infoLabel=QtGui.QLabel("Дополнительная\nинформация")
            self.info=QtGui.QTextEdit()
            self.label=QtGui.QLabel()
            self.btn1=QtGui.QPushButton("Btn1")
            self.btn2=QtGui.QPushButton("Btn2")
            self.btnLayout=QtGui.QVBoxLayout()
            self.btnLayout.addWidget(self.btn1)
            self.btnLayout.addWidget(self.btn2)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.name1Label,0,0)
            self.layout.addWidget(self.name1,0,1,1,5)
            self.layout.addWidget(self.name2Label,1,0)
            self.layout.addWidget(self.name2,1,1,1,5)
            self.layout.addWidget(self.name3Label,2,0)
            self.layout.addWidget(self.name3,2,1,1,5)
            self.layout.addWidget(self.passportLabel,3,0)
            self.layout.addWidget(self.passport,3,1,2,5)
            self.layout.addWidget(self.addressRegLabel,5,0)
            self.layout.addWidget(self.addressReg,5,1,1,5)
            self.layout.addWidget(self.addressResLabel,6,0)
            self.layout.addWidget(self.addressRes,6,1,1,5)
            self.layout.addWidget(self.phoneMobLabel,7,0)
            self.layout.addWidget(self.phoneMob,7,1,1,5)
            self.layout.addWidget(self.phoneHomeLabel,8,0)
            self.layout.addWidget(self.phoneHome,8,1,1,5)
            self.layout.addWidget(self.eMailLabel,9,0)
            self.layout.addWidget(self.eMail,9,1,1,5)
            self.layout.addWidget(self.infoLabel,10,0,2,1)
            self.layout.addWidget(self.info,10,1,7,5)
            self.layout.addWidget(self.label,17,0,2,1)
            self.layout.addLayout(self.btnLayout,17,1,2,5)
            self.setLayout(self.layout)
    def getInfo(self):
        newInfo={}
        newInfo["name1"]=self.name1.text()
        newInfo["name2"]=self.name2.text()
        newInfo["name3"]=self.name3.text()
        newInfo["passport"]=self.passport.toPlainText()
        newInfo["addressReg"]=self.addressReg.text()
        newInfo["addressRes"]=self.addressRes.text()
        newInfo["phoneMob"]=self.phoneMob.text()
        newInfo["phoneHome"]=self.phoneHome.text()
        newInfo["eMail"]=self.eMail.text()
        newInfo["info"]=self.info.toPlainText()
        return newInfo

class workerInfoWidget(workerInfo):
    def __init__(self, parent=None):
        workerInfo.__init__(self, parent)
        self.name1.setText(parent.model.keys["name1"])
        self.name2.setText(parent.model.keys["name2"])
        self.name3.setText(parent.model.keys["name3"])
        self.passport.setText(parent.model.keys["passport"])
        self.addressRes.setText(parent.model.keys["addressRes"])
        self.addressReg.setText(parent.model.keys["addressReg"])
        self.phoneMob.setText(parent.model.keys["phoneMob"])
        self.phoneHome.setText(parent.model.keys["phoneHome"])
        self.eMail.setText(parent.model.keys["eMail"])
        self.info.setText(parent.model.keys["info"])
        self.label.setText("Режим\nредактирования\nданных")
        self.btn1.clicked.connect(self.setMode)
        self.btn2.setText("Сохранить изменения")
        self.btn2.clicked.connect(self.save)
        self.mode=True
        self.setMode()
    def setMode(self):
        if self.mode:
            self.name1.setReadOnly(True)
            self.name2.setReadOnly(True)
            self.name3.setReadOnly(True)
            self.passport.setReadOnly(True)
            self.addressRes.setReadOnly(True)
            self.addressReg.setReadOnly(True)
            self.phoneMob.setReadOnly(True)
            self.phoneHome.setReadOnly(True)
            self.eMail.setReadOnly(True)
            self.info.setReadOnly(True)
            self.btn1.setText("Включить")
            self.btn2.setDisabled(True)
            self.mode=False
        else:
            self.name1.setReadOnly(False)
            self.name2.setReadOnly(False)
            self.name3.setReadOnly(False)
            self.passport.setReadOnly(False)
            self.addressRes.setReadOnly(False)
            self.addressReg.setReadOnly(False)
            self.phoneMob.setReadOnly(False)
            self.phoneHome.setReadOnly(False)
            self.eMail.setReadOnly(False)
            self.info.setReadOnly(False)
            self.btn1.setText("Выключить")
            self.btn2.setDisabled(False)
            self.mode=True
    def save(self):
        newKeys=self.getInfo()
        self.model.saveWorker(newKeys)
        self.setMode()

class workerCarWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Перечень машин которыми управлял или управляет сотрудник.")
            self.workerCar=self.model.loadWorkerCarTable()
            self.addCar=QtGui.QPushButton("Добавить машину")
            self.closeCar=QtGui.QPushButton("Закрыть период")
            self.layoutBtn=QtGui.QHBoxLayout()
            self.layoutBtn.addWidget(self.closeCar)
            self.layoutBtn.addWidget(self.addCar)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.workerCar)
            self.layout.addLayout(self.layoutBtn)
            self.setLayout(self.layout)

class workerRepairWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Ремонты выплненные этим сотрудником")
            self.workerRepair=self.model.loadWorkerRepairTable()
            self.editRepair=QtGui.QPushButton("Отредактировать")
            self.addRepair=QtGui.QPushButton("Произвести ремонт")
            self.layoutBtn=QtGui.QHBoxLayout()
            self.layoutBtn.addWidget(self.editRepair)
            self.layoutBtn.addWidget(self.addRepair)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.workerRepair)
            self.layout.addLayout(self.layoutBtn)
            self.setLayout(self.layout)

class workerDeleteWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            label=QtGui.QLabel("""
            Удаление работника повлечет за собой каскадное удаление
            информации:
                -произведеных ремонтов;
                -устаноавленых деталях;
                -водителях и периодах вождения.
            После удаления эту информацию невозможно будет
            восстановить.""")
            self.btnDel=QtGui.QPushButton("Удалить")
            self.btnDel.clicked.connect(self.delete)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(label)
            self.layout.addWidget(self.btnDel)
            self.setLayout(self.layout)
    def delete(self):
        dialog=dialogWindows(self)
        dialog.label.setText("Вы уверены что хотите удалить\nэтого сотрудника с базы данных??")
        dialog.btnYes.setText("Да")
        dialog.show()
        result=dialog.exec_()
        if result==QtGui.QDialog.Accepted:
            self.model.deleteWorker()
            self.parentWidget().parentWidget().parentWidget().close()

class addWorkerWidget(workerInfo):
    def __init__(self, parent=None):
        workerInfo.__init__(self, parent)
        self.btn1.setText("Сохранить")
        self.btn1.clicked.connect(self.save)
        self.btn2.setText("Отмена")
        self.btn2.clicked.connect(self.close)
        self.show()
    def save(self):
        newKeys=self.getInfo()
        self.model.addWorker(newKeys)
        self.close()

class settingWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.group1=QtGui.QGroupBox("Добавление/удаление вспомогательной информации в базу данных")
            self.labelCar=QtGui.QLabel("Информация для машин")
            self.btnCarColor=QtGui.QPushButton("Цвет машин")
            self.btnCarColor.clicked.connect(lambda: addWidget(self,self.model.loadCarColorTable(), "Цвет машин"))
            self.btnCarModel=QtGui.QPushButton("Модель машин")
            self.btnCarModel.clicked.connect(lambda: addWidget(self,self.model.loadCarModelTable(), "Модели машин"))
            self.labelDetail=QtGui.QLabel("Информация для делей")
            self.btnTypeD=QtGui.QPushButton("Тип детали")
            self.btnTypeD.clicked.connect(lambda: addWidget(self,self.model.loadDetailTypeTable(), "Типы деталей"))
            self.btnMade=QtGui.QPushButton("Производитель деталей")
            self.btnMade.clicked.connect(lambda: addWidget(self,self.model.loadDetailMadeTable(), "Производители деталей"))
            self.btnDetail=QtGui.QPushButton("Каталог деталей")
            self.btnDetail.clicked.connect(lambda: catalog(self))
            self.labelRepair=QtGui.QLabel("Информация для ремонтов")
            self.btnClassR=QtGui.QPushButton("Класс ремонта")
            self.btnClassR.clicked.connect(lambda: addWidget(self, self.model.loadRepairClassTable(), "Класс ремонта"))
            self.btnTypeR=QtGui.QPushButton("Тип ремонта")
            self.btnTypeR.clicked.connect(lambda: addWidget(self, self.model.loadRepairTypeTable(), "Тип ремонта", self.model.loadRepairClassCombo()))
            self.labelWorker=QtGui.QLabel("Информация для работников")
            self.btnAccess=QtGui.QPushButton("Права доступа")
            self.btnAccess.clicked.connect(lambda: addAccess(self))
            self.btnPost=QtGui.QPushButton("Должность")
            self.btnPost.clicked.connect(lambda: addWidget(self, self.model.loadPostTable(),"Добавление должностей", self.model.loadAccessCombo()))
            self.layout1=QtGui.QGridLayout()
            self.layout1.addWidget(self.labelCar,0,0)
            self.layout1.addWidget(self.btnCarColor,1,0,1,1)
            self.layout1.addWidget(self.btnCarModel,1,1,1,1)
            self.layout1.addWidget(self.labelDetail,2,0)
            self.layout1.addWidget(self.btnTypeD,3,0,1,1)
            self.layout1.addWidget(self.btnMade,3,1,1,1)
            self.layout1.addWidget(self.btnDetail,3,2,1,1)
            self.layout1.addWidget(self.labelRepair,4,0)
            self.layout1.addWidget(self.btnClassR,5,0,1,1)
            self.layout1.addWidget(self.btnTypeR,5,1,1,1)
            self.layout1.addWidget(self.labelWorker,6,0)
            self.layout1.addWidget(self.btnAccess,7,0)
            self.layout1.addWidget(self.btnPost,7,1)
            self.group1.setLayout(self.layout1)
            self.group2=QtGui.QGroupBox("Управление пользователями")
            self.label2=QtGui.QLabel("""\"Права доступа" устанавливает какие работни-
            ки могут входить в програму. А так же указывает
            пароль для входа в программу.
            "Изменить пароль позволяет изменить пароль
            работника для входа в программу.""")
            self.worker=QtGui.QPushButton("Назначить на должность")
            self.worker.clicked.connect(lambda: addTimeWork(self))
            self.password=QtGui.QPushButton("Изменить пароль")
            self.password.clicked.connect(lambda: setPassword(self))
            self.layout2=QtGui.QGridLayout()
            self.layout2.addWidget(self.label2, 0,1,5,10)
            self.layout2.addWidget(self.worker,1,0,1,1)
            self.layout2.addWidget(self.password,2,0,1,1)
            self.group2.setLayout(self.layout2)
            self.group3=QtGui.QGroupBox("Резервное копирование")
            self.label3=QtGui.QLabel("""\"Резервное копирование" позволяет создавать и
            востанавливать резервные копии базы данных. """)
            self.btnBackup=QtGui.QPushButton("Резервное копирование")
            self.btnBackup.clicked.connect(lambda: addWidget(self,self.model.loadDetailMadeTable(), "Производители деталей"))
            self.layout3=QtGui.QGridLayout()
            self.layout3.addWidget(self.label3, 0,1,3,10)
            self.layout3.addWidget(self.btnBackup,1,0,1,1)
            self.group3.setLayout(self.layout3)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.group1)
            self.layout.addWidget(self.group2)
            self.layout.addWidget(self.group3)
            self.setLayout(self.layout)

class catalog(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self,parent)
        if models.__init__(self, parent):
            self.setModal(True)
            self.setWindowTitle('"АвтоПарк" Каталог деталей')
            self.labelCatalog=QtGui.QLabel("Каталог деталей")
            self.tableCatalog=self.model.loadCatalogTable()
            self.tableCatalog.doubleClicked.connect(lambda: detailWidget(self))
            self.btnAdd=QtGui.QPushButton("Добавить деталь")
            self.btnAdd.clicked.connect(lambda: addCatalog(self))
            self.btnDel=QtGui.QPushButton("Удалить деталь")
            self.btnDel.clicked.connect(self.tableCatalog.delRow)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.labelCatalog,0,0,1,2)
            self.layout.addWidget(self.tableCatalog,1,0,5,2)
            self.layout.addWidget(self.btnDel,6,0,1,1)
            self.layout.addWidget(self.btnAdd,6,1,1,1)
            self.setLayout(self.layout)
            self.show()

class detailWidget(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Информация о детале')
            self.setModal(True)
            self.name
            self.type
            self.made
            self.about
            self.btnСhange
            self.btnSave

class addCatalog(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Добавление детали в каталог')
            self.setModal(True)
            self.setWindowTitle('"АвтоПарк" Добавление деталт в каталог')
            self.labelName=QtGui.QLabel("Название детали")
            self.textName=QtGui.QLineEdit()
            self.labelType=QtGui.QLabel("Тип детали")
            self.comboType=self.model.loadDetailTypeCombo()
            self.labelMade=QtGui.QLabel("Производитель")
            self.comboMade=self.model.loadDetailMadeCombo()
            self.labelAbout=QtGui.QLabel("Дополнительная\nинформация")
            self.textAbout=QtGui.QTextEdit()
            self.btnSave=QtGui.QPushButton("Сохранить")
            self.btnSave.clicked.connect(self.save)
            self.btnCanсel=QtGui.QPushButton("Отмена")
            self.btnCanсel.clicked.connect(self.close)
            self.layoutBtn=QtGui.QHBoxLayout()
            self.layoutBtn.addWidget(self.btnCanсel)
            self.layoutBtn.addWidget(self.btnSave)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.labelName,0,0,1,1)
            self.layout.addWidget(self.textName,0,1,1,5)
            self.layout.addWidget(self.labelType,1,0,1,1)
            self.layout.addWidget(self.comboType,1,1,1,5)
            self.layout.addWidget(self.labelMade,2,0,1,1)
            self.layout.addWidget(self.comboMade,2,1,1,5)
            self.layout.addWidget(self.labelAbout,3,0,2,1)
            self.layout.addWidget(self.textAbout,3,1,5,5)
            self.layout.addLayout(self.layoutBtn,8,0,1,6)
            self.setLayout(self.layout)
            self.show()
    def save(self):
        name=self.textName.text()
        about=self.textAbout.toPlainText()
        self.model.addToCatalog(name, about)
        self.textName.setText("")
        self.textAbout.setText("")







#Родитель диалоговых окон
class dialogWindows(QtGui.QDialog):
#Родитель диалоговых окон. Реализует 2 кнопки(ok, cancel)
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle('"АвтоПарк"')
        self.setModal(True)
        self.label=QtGui.QLabel("")
        self.btnYes=QtGui.QPushButton("Да")
        self.btnNo=QtGui.QPushButton("Отмена")
        self.btnYes.clicked.connect(self.accept)
        self.btnNo.clicked.connect(self.reject)
        self.layout=QtGui.QVBoxLayout()
        self.layout.addWidget(self.label)
        self.layoutBtn=QtGui.QHBoxLayout()
        self.layoutBtn.addWidget(self.btnNo)
        self.layoutBtn.addWidget(self.btnYes)
        self.layout.addLayout(self.layoutBtn)
        self.setLayout(self.layout)
#Диалоговое окно закрытия
class dialogClose(dialogWindows):
    def __init__(self, parent):
        dialogWindows.__init__(self, parent)
        self.label.setText("Вы уверены что хотите\nвыйти с приложения?")
#Диалоговое окно ошибки
class dialogError(dialogWindows):
    def __init__(self, parent=None, title=None):
        dialogWindows.__init__(self, parent)
        self.btnYes.setText("Ok")
        self.btnNo.setDisabled(True)
        if type(title)==str:
            self.setWindowTitle(title)
        else:
            self.setWindowTitle('"АвтоПарк" Ошибка')
        if parent:
            try:
                err=parent.__dict__["err"]
            except KeyError or err==None:
                try:
                    err=parent.__dict__["model"].err
                except KeyError:
                    err=None
        if type(err)==str:
            self.label.setText(err)
        else:
            self.label.setText("Неизвестная ошибка")
        self.show()
#Главное окно приложение
class mainWindow(QtGui.QTabWidget):
#Главное окно програмы
    def __init__(self, parent=None):
        QtGui.QTabWidget.__init__(self, parent)
        self.model=modelInfo()
        self.titleDict={"title":'"АвтоПарк" ',
                        0:"Машины",
                        1:"Ремонты",
                        2:"Сотрудники",
                        3:"Детали и расходнын материалы",
                        4:"Дополнительные функции"}
        self.setWindowTitle(self.titleDict["title"])
        self.hide()
        self.resize(700, 600)
        self.addTab(carsWidget(self), self.titleDict[0])
        self.addTab(repairsWidget(self), self.titleDict[1])
        self.addTab(workersWidget(self), self.titleDict[2])
        self.addTab(detailsWidget(self), self.titleDict[3])
        self.addTab(settingWidget(self), self.titleDict[4])
        self.login=loginWindow(self)
        self.login.destroyed.connect(self.close)
        self.login.accepted.connect(self.showMain)
        self.currentChanged.connect(self.titleSet)
    def titleSet(self, count):
        self.setWindowTitle("{0} {1}".format(self.titleDict["title"], self.titleDict[count]))
    def showMain(self):
        self.show()
        self.login.destroyed.disconnect()
#Окно ваторизации
class loginWindow(QtGui.QDialog, models):
#Окно входа в програму с выбором сотрудника и вводом пароля
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        if models.__init__(self, parent):
            self.setModal(True)
            self.setWindowTitle('"АвтоПарк" авторизация')
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self.userLabel=QtGui.QLabel("Работники")
            self.userCombo=self.model.loadUserCombo()
            self.passLabel=QtGui.QLabel("Пароль")
            self.passEdit=QtGui.QLineEdit()
            self.passEdit.setEchoMode(QtGui.QLineEdit.Password)
            self.btnIn=QtGui.QPushButton("Войти")
            self.btnIn.clicked.connect(self.login)
            self.btnIn.setDefault(True)
            self.btnClose=QtGui.QPushButton("Выйти")
            self.btnClose.clicked.connect(self.close)
            self.btnLayout=QtGui.QHBoxLayout()
            self.btnLayout.addWidget(self.btnClose)
            self.btnLayout.addWidget(self.btnIn)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.userLabel, 0,0)
            self.layout.addWidget(self.userCombo,0,1)
            self.layout.addWidget(self.passLabel,1,0)
            self.layout.addWidget(self.passEdit,1,1)
            self.layout.addLayout(self.btnLayout,2,1)
            self.setLayout(self.layout)
            self.show()
    def login(self):
        password=self.passEdit.text()
        if self.model.check(password):
            self.accept()
        else:
            self.err="Введен не верный пароль или выбран\nне тот сотрудник. Попробуйте еще раз."
            dialogError(self, '"АвтоПарк" Ошибка авторизации')
    def closeEvent(self, event):
        dialog=dialogClose(self)
        result=dialog.exec_()
        if result==QtGui.QDialog.Accepted:
            event.accept()
            self.close()
        else:
            event.ignore()
#Вкладка машин галавного окна
class carsWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Автомобили предприятия")
            self.addCarBtn=QtGui.QPushButton("Добавить машину")
            self.tableCars=self.model.loadCarTable()
            self.tableCars.doubleClicked.connect(lambda: carWidget(self))
            self.addCarBtn.clicked.connect(lambda: addCar(self))
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,2)
            self.layout.addWidget(self.addCarBtn,0,14,1,1)
            self.layout.addWidget(self.tableCars,1,0,15,15)
            self.setLayout(self.layout)
#Скелет информации о машине
class carInfo(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        if models.__init__(self, parent):
            self.model=parent.model
            self.setModal(True)
            self.name=QtGui.QLineEdit()
            self.carModel=self.model.loadCarModelCombo()
            self.color=self.model.loadCarColorCombo()
            self.number=QtGui.QLineEdit()
            self.radio=QtGui.QLineEdit()
            self.about=QtGui.QTextEdit()
            self.label=QtGui.QLabel()
            self.btn1=QtGui.QPushButton("Btn1")
            self.btn2=QtGui.QPushButton("Btn2")
            self.layoutBtn=QtGui.QHBoxLayout()
            self.layoutBtn.addWidget(self.btn2)
            self.layoutBtn.addWidget(self.btn1)
            self.form=QtGui.QFormLayout()
            self.form.addRow("Позывной", self.name)
            self.form.addRow("Модель", self.carModel)
            self.form.addRow("Цвет", self.color)
            self.form.addRow("Гос.номер", self.number)
            self.form.addRow("Радио", self.radio)
            self.form.addRow("Дополнительная\nинформация", self.about)
            self.form.addRow(self.layoutBtn)
            self.setLayout(self.form)
            self.show()
    def getInfo(self):
        newInfo={}
        newInfo["carName"]=self.name.text()
        newInfo["number"]=self.number.text()
        newInfo["radio"]=self.radio.text()
        newInfo["info"]=self.about.toPlainText()
        return newInfo
#Окно добавления машины
class addCar(carInfo):
    def __init__(self, parent=None):
        carInfo.__init__(self, parent)
        self.btn1.setText("Сохранить")
        self.btn1.clicked.connect(self.save)
        self.btn2.setText("Отменить")
        self.btn2.clicked.connect(self.close)
        self.show()
    def save(self):
        newKeys=self.getInfo()
        if newKeys["carName"]=="":
            self.err="Введите название машины."
            dialogError(self, '"АвтоПарк" Ошибка ввода')
        else:
            if self.model.addCar(newKeys):
                self.close()
            else:
                self.err=self.model.err
                dialogError(self, '"АвтоПарк" Ошибка записи')
#Окно карточки машины
class carWidget(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.tab=QtGui.QTabWidget()
            self.tab.addTab(carInfoWidget(self), "Общая информация")
            self.tab.addTab(carDriversWidget(self), "Водители")
            self.tab.addTab(carRepairWidget(self), "Ремонот")
            self.tab.addTab(carDeleteWidget(self), "Удаление")
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.tab)
            self.setLayout(self.layout)
            try:
                car=self.model.keys["carName"]
            except KeyError:
                self.err="Ошибка при загрузки информации."
                car="ОШИБКА"
                dialogError(self)
            self.setWindowTitle('"АвтоПарк" Машина {0}'.format(car))
            self.show()
#Вкладка с основной информацией о машине
class carInfoWidget(carInfo):
    def __init__(self, parent=None):
        carInfo.__init__(self, parent)
        self.label.setText("Режим\nредактирования\nданных")
        self.btn1.setText("Вкючить")
        self.btn1.clicked.connect(self.setMode)
        self.btn2.setText("Сохранить изменения")
        self.btn2.clicked.connect(self.save)
        self.mode=True
        self.setMode()
        try:
            self.name.setText(self.model.keys["carName"])
            self.number.setText(self.model.keys["number"])
            self.radio.setText(self.model.keys["radio"])
            self.about.setText(self.model.keys["info"])
        except KeyError:
            self.err="Ошибка при загрузки информации."
            dialogError(self)
    def setMode(self):
        if self.mode:
            self.carModel.setDisabled(True)
            self.color.setDisabled(True)
            self.about.setReadOnly(True)
            self.name.setReadOnly(True)
            self.radio.setReadOnly(True)
            self.number.setReadOnly(True)
            self.btn1.setText("Включить")
            self.btn2.setDisabled(True)
            self.mode=False
        else:
            self.carModel.setDisabled(False)
            self.color.setDisabled(False)
            self.about.setReadOnly(False)
            self.name.setReadOnly(False)
            self.radio.setReadOnly(False)
            self.number.setReadOnly(False)
            self.btn1.setText("Выключить")
            self.btn2.setDisabled(False)
            self.mode=True
    def save(self):
        newKeys=self.getInfo()
        self.model.saveCar(newKeys)
        self.setMode()
#Вкладка с информацией о водителях машины
class carDriversWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Водители управляющие автомобилем")
            self.infoDriver=self.model.loadCarDriverTable()
            self.infoDriver.doubleClicked.connect(self.periodDrive)
            self.driverAddBtn=QtGui.QPushButton("Добавить водителя")
            self.driverAddBtn.clicked.connect(lambda: addPeriodDriveWidget(self))
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,2)
            self.layout.addWidget(self.driverAddBtn,0,3,1,1)
            self.layout.addWidget(self.infoDriver,1,0,10,4)
            self.setLayout(self.layout)
    def periodDrive(self):
        periodDriveWidget(self)
#Родитель периода вождения
class periodDrive(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Период вождения')
            self.worker=self.model.loadWorkerCombo()
            self.dateIn=dateEdit()
            self.dateOut=dateEdit()
            self.btn1=QtGui.QPushButton("btn1")
            self.btn2=QtGui.QPushButton("btn2")
            self.form=QtGui.QFormLayout()
            self.form.addRow("Водитель:", self.worker)
            self.form.addRow("Начало периода вождения:", self.dateIn)
            self.form.addRow("Окончание периода вождения:", self.dateOut)
            self.form.addRow(self.btn1, self.btn2)
            self.setLayout(self.form)
            self.show()
#Окно добавления водителя на машину
class addPeriodDriveWidget(periodDrive):
    def __init__(self, parent=None):
        periodDrive.__init__(self, parent)
        self.btn1.setText("Отмена")
        self.btn1.clicked.connect(self.close)
        self.btn2.setText("Сохранить")
        self.btn2.clicked.connect(self.save)
    def save(self):
        keys={"dateIn":self.dateIn.date().toPyDate(),
              "dateOut":self.dateOut.date().toPyDate()}
        if self.model.addCarDriver(keys):
            self.close()
        else:
            dialogError(self)
#Окно c инфрмацией о периода вождения
class periodDriveWidget(periodDrive):
    def __init__(self, parent=None):
        periodDrive.__init__(self,parent)
        try:
            self.dateIn.setDatePy(self.model.keys["dateIn"])
            self.dateOut.setDatePy(self.model.keys["dateOut"])
        except KeyError:
            self.err="Ошибка загрузки информации."
            dialogError(self)
        self.btn1.setText("Удалить")
        self.btn1.clicked.connect(self.delete)
        self.btn2.setText("Сохранить")
        self.btn2.clicked.connect(self.save)
    def delete(self):
        if self.model.deletePeriodInfo():
            self.close()
        else:
            self.err=self.model.err
            dialogError(self)
    def save(self):
        keys={"dateIn":self.dateIn.date().toPyDate(),
              "dateOut":self.dateOut.date().toPyDate()}
        if self.model.updatePeriodInfo(keys):
            self.close()
        else:
            self.err=self.model.err
            dialogError(self)
#Вкладка с информацией о проведенных ремонтах машины
class carRepairWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("Произведеное обслуживание и ремонтные работы")
            self.infoRepair=self.model.loadCarRepairTable()
            self.infoRepair.doubleClicked.connect(lambda: repairInfoWidget(self))
            self.repairBtn=QtGui.QPushButton("Произвести ремонт/обслуживание")
            self.repairBtn.clicked.connect(lambda: addCarRepairWidget(self))
            self.reportBtn=QtGui.QPushButton("Формирование отчетов")
            self.reportBtn.clicked.connect(lambda: carReport(self))
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,2)
            self.layout.addWidget(self.repairBtn,1,1)
            self.layout.addWidget(self.reportBtn,1,0)
            self.layout.addWidget(self.infoRepair,2,0,10,4)
            self.setLayout(self.layout)
#Родитель окна ремонта
class addRepair(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Ремонт машины')
            self.label=QtGui.QLabel("Произвести ремонт/обслуживание машины")
            self.carCombo=self.model.loadCarCombo()
            self.kmage=QtGui.QLineEdit("0")
            self.mechanicCombo=self.model.loadMechanicCombo()
            self.classCombo=self.model.loadRepairClassCombo()
            self.typeCombo=self.model.loadRepairTypeCombo()
            self.date=dateEdit()
            self.priceLine=QtGui.QLineEdit("0")
            self.detailsLabel=QtGui.QLabel("Детали необхотимые для ремонта или обслуживания:")
            self.detailsTable=self.model.loadNewDetailInstallTable()
            self.saveBtn=QtGui.QPushButton("Сохранить")
            self.saveBtn.clicked.connect(self.addRepair)
            self.clrBtn=QtGui.QPushButton("Отменить")
            self.clrBtn.clicked.connect(self.close)
            self.form1=QtGui.QFormLayout()
            self.form1.addRow("Машина", self.carCombo)
            self.form1.addRow("Класс ремонта", self.classCombo)
            self.form1.addRow("Механик",self.mechanicCombo)
            self.form1.addRow("Дата ремонта", self.date)
            self.form2=QtGui.QFormLayout()
            self.form2.addRow("Пробег машины",self.kmage)
            self.form2.addRow("Тип ремонта", self.typeCombo)
            self.form2.addRow("Цена ремонта", self.priceLine)
            self.layoutBtn=QtGui.QHBoxLayout()
            self.layoutBtn.addWidget(self.clrBtn)
            self.layoutBtn.addWidget(self.saveBtn)
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,5)
            self.layout.addLayout(self.form1,1,0,1,6)
            self.layout.addLayout(self.form2,1,6,1,6)
            self.layout.addWidget(self.detailsLabel,2,0,1,12)
            self.layout.addWidget(self.detailsTable,3,0,12,12)
            self.layout.addLayout(self.layoutBtn,15,8,1,4)
            self.setLayout(self.layout)
            self.show()
    def loadKey(self):
        self.keys={"date":self.date.date().toPyDate(),
              "price":self.priceLine.text(),
              "kmage":self.kmage.text()}
#Окно проведения ремонта машины
class addCarRepairWidget(addRepair):
    def __init__(self, parent=None):
        addRepair.__init__(self, parent)
        self.setWindowTitle('"АвтоПарк" Ремонт машины:{0}'.format(self.model.keys["carName"]))
        self.carCombo.setDisabled(True)
    def addRepair(self):
        self.loadKey()
        if self.model.addRepairCar(self.keys):
            self.close()
        else:
            self.err=self.model.err
            dialogError(self)
#Окно общей информации о ремоте
class repairInfo(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Общая информация о ремонте')
            self.carCombo=self.model.loadCarCombo()
            self.mechanicCombo=self.model.loadMechanicCombo()
            self.classCombo=self.model.loadRepairClassCombo()
            self.typeCombo=self.model.loadRepairTypeCombo()
            try:
                self.kmage=QtGui.QLineEdit(str(self.model.keys["kmage"]))
                self.date=dateEdit(self.model.keys["date"])
                self.price=QtGui.QLineEdit(str(self.model.keys["price"]))
            except KeyError:
                self.err="Ошибка загрузки информации."
                dialogError(self)
            else:
                self.btnEdit=QtGui.QPushButton("Включить")
                self.btnEdit.clicked.connect(self.setMode)
                self.btnSave=QtGui.QPushButton("Сохранить")
                self.btnSave.clicked.connect(self.save)
                self.btnRepeal=QtGui.QPushButton("Отменить ремонт")
                self.btnRepeal.clicked.connect(self.repeal)
                self.btnLayout=QtGui.QHBoxLayout()
                self.btnLayout.addWidget(self.btnEdit)
                self.btnLayout.addWidget(self.btnSave)
                self.btnLayout.addWidget(self.btnRepeal)
                self.form=QtGui.QFormLayout()
                self.form.addRow("Машина", self.carCombo)
                self.form.addRow("Пробег машины",self.kmage)
                self.form.addRow("Класс ремонта", self.classCombo)
                self.form.addRow("Тип ремонта", self.typeCombo)
                self.form.addRow("Механик",self.mechanicCombo)
                self.form.addRow("Цена ремонта", self.price)
                self.form.addRow("Дата ремонта", self.date)
                self.form.addRow(self.btnLayout)
                self.setLayout(self.form)
                self.mode=True
                self.setMode()
    def setMode(self):
        if self.mode:
            self.mode=False
            self.carCombo.setDisabled(True)
            self.mechanicCombo.setDisabled(True)
            self.classCombo.setDisabled(True)
            self.typeCombo.setDisabled(True)
            self.kmage.setDisabled(True)
            self.date.setDisabled(True)
            self.price.setDisabled(True)
            self.btnEdit.setText("Включить")
            self.btnSave.setDisabled(True)
        else:
            self.mode=True
            self.carCombo.setDisabled(False)
            self.mechanicCombo.setDisabled(False)
            self.classCombo.setDisabled(False)
            self.typeCombo.setDisabled(False)
            self.kmage.setDisabled(False)
            self.date.setDisabled(False)
            self.price.setDisabled(False)
            self.btnEdit.setText("Выключить")
            self.btnSave.setDisabled(False)
    def save(self):
        keys={"kmage":self.kmage.text(),
              "price":self.price.text(),
              "date":self.date.date().toPyDate()}
        if self.model.updateRepair(keys)==False:
            self.err=self.mode.err
            dialogError(self)
    def repeal(self):
        dialog=dialogWindows(self)
        dialog.setWindowTitle('"АвтоПарк" Отмена ремонта')
        dialog.label.setText("Вы уверены что хотите отменить этот ремонт?")
        dialog.btnYes.setText("Да")
        dialog.show()
        result=dialog.exec_()
        if result==QtGui.QDialog.Accepted:
            if self.model.repealRepair():
                self.parentWidget().parentWidget().parentWidget().close()
            else:
                dialog.close()
                self.err=self.model.err
                dialogError(self)
#Окно с перечнем деталей затраченых на ремонт
class repairDetailInfo(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Информация затратах деталей на ремонт')
            self.label=QtGui.QLabel("Перечень деталей использованных во время ремонта\nили обслуживания.")
            self.addBtn=QtGui.QPushButton("Добавить делать")
            self.addBtn.clicked.connect(lambda: addRepairDetailWidget(self))
            self.detail=self.model.loadDetailRepairTable()
            self.detail.doubleClicked.connect(lambda: repairDetailInfoWidget(self))
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(self.label,0,0,1,4)
            self.layout.addWidget(self.addBtn,0,4,1,1)
            self.layout.addWidget(self.detail,1,0,5,5)
            self.setLayout(self.layout)
# Окно добовления деталей в ремонт
class addRepairDetailWidget(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Дополнительные детали')
            self.label=QtGui.QLabel("Перечень деталей которые можно добавить в ремонт:")
            self.detail=self.model.loadNewDetailInstallTable()
            self.addBtn=QtGui.QPushButton("Добавить детали")
            self.addBtn.clicked.connect(self.addDetail)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.detail)
            self.layout.addWidget(self.addBtn)
            self.setLayout(self.layout)
            self.show()
    def addDetail(self):
        if self.model.addDetailToRepairCar():
            self.close()
        else:
            self.err=self.model.err()
            dialogError(self)
#Окно информации о детале
class repairDetailInfoWidget(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.label=QtGui.QLabel("????")
            self.date=dateEdit()
            self.btn1=QtGui.QPushButton("Списать")
            self.btn2=QtGui.QPushButton("На склад")
            self.form=QtGui.QFormLayout()
            self.form.addRow(self.label)
            self.form.addRow("Дата снятие/списания", self.date)
            self.form.addRow(self.btn1, self.btn2)
            self.setLayout(self.form)
            self.show()


#Окно информации о ремонте
class repairInfoWidget(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setModal(True)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Информация о ремонте')
            self.tab=QtGui.QTabWidget()
            self.tab.addTab(repairInfo(self), "Общая информация")
            self.tab.addTab(repairDetailInfo(self), "Затраченые детали")
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(self.tab)
            self.setLayout(self.layout)
            self.show()





class carReport(QtGui.QDialog, models):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        if models.__init__(self, parent):
            self.setWindowTitle('"АвтоПарк" Формирование отчетa')
            label=QtGui.QLabel("Формирование отчетовпо затратам\nна машину за период")
            dateStartLabel=QtGui.QLabel("Начиная с")
            dateFinishLabel=QtGui.QLabel("по")
            self.dateStart=QtGui.QDateEdit()
            self.dateFinish=QtGui.QDateEdit()
            layoutDate=QtGui.QHBoxLayout()
            layoutDate.addWidget(dateStartLabel)
            layoutDate.addWidget(self.dateStart)
            layoutDate.addWidget(dateFinishLabel)
            layoutDate.addWidget(self.dateFinish)
            self.repairCheck=QtGui.QCheckBox("Затраты на роботы")
            self.detailCheck=QtGui.QCheckBox("Затраты на детали")
            self.reportBtn=QtGui.QPushButton("Сформировать отчет")
            self.clrBtn=QtGui.QPushButton("Отмена")
            self.layout=QtGui.QGridLayout()
            self.layout.addWidget(label,0,0,1,2)
            self.layout.addLayout(layoutDate,1,0,1,2)
            self.layout.addWidget(self.repairCheck,3,0)
            self.layout.addWidget(self.detailCheck,4,0)
            self.layout.addWidget(self.reportBtn,5,1)
            self.layout.addWidget(self.clrBtn,5,0)
            self.setLayout(self.layout)
            self.show()

class carDeleteWidget(QtGui.QWidget, models):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        if models.__init__(self, parent):
            label=QtGui.QLabel("""
            Удаление машины повлечет за собой каскадное удаление
            информации:
                -произведеных ремонтов;
                -устаноавленых деталях;
                -водителях и периодах вождения.
            После удаления эту информацию невозможно будет
            восстановить.""")
            self.btnDel=QtGui.QPushButton("Удалить")
            self.btnDel.clicked.connect(self.delete)
            self.layout=QtGui.QVBoxLayout()
            self.layout.addWidget(label)
            self.layout.addWidget(self.btnDel)
            self.setLayout(self.layout)
    def delete(self):
        dialog=dialogWindows(self)
        dialog.label.setText("Вы уверены что хотите удалить\nэту машину с базы данных??")
        dialog.btnYes.setText("Да")
        dialog.show()
        result=dialog.exec_()
        if result==QtGui.QDialog.Accepted:
            self.model.deleteCar()
            self.parentWidget().parentWidget().parentWidget().close()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    windows = mainWindow()
    sys.exit(app.exec_())