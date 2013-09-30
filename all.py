# -*- coding: utf-8 -*-
__author__ = 'Bondarenko Yura'
from PyQt4 import QtCore, QtGui
import hashlib
from datetime import date

# -*- coding: utf-8 -*-
__author__ = 'Bondarenko Yura'
import sqlite3
import datetime
import shutil, os
import SQL

class base:
    def __init__(self):
        self.err=""
        self.db={
            "db":(SQL.db, "db.db"),
            "system":(SQL.system, "systemDb.db")
        }
        self.install()
    def connect(self,db):
    # Подкдключение к базе данных с вкл. внешними ключами
    # db_con -- имя подключаемой базы данных(файла)
        try:
            self.con=sqlite3.connect(db[1], isolation_level=None, detect_types=sqlite3.PARSE_DECLTYPES)
        except sqlite3.DatabaseError as err:
            self.err="Ошибка: {0}".format(err)
            return False
        else:
            self.cur=self.con.cursor()
            sql="PRAGMA foreign_keys=1;"
            try:
                self.cur.execute(sql)
            except sqlite3.DatabaseError as err:
                self.err="Ошибка: {0}".format(err)
                self.disconnect()
                return False
            else:
                self.err=""
                self.con.commit()
                return True
    def disconnect(self):
    #Закрытие подключения к базе данных
        self.con.commit()
        self.cur.close()
        self.con.close()
    def install(self):
    #Инсталяция таблиц базы данных
        for base in self.db:
            self.connect(self.db[base])
            for table in self.db[base][0]:
                if type(table)==str and not(table[0]=="_"):
                    try:
                        self.cur.execute(self.db[base][0][table])
                    except sqlite3.DatabaseError as err :
                        self.err="При создании таблици '{0}':\n произошла ошибка\n{1}".format(table, err)
                        self.disconnect()
                        return False
                    else:
                        self.con.commit()
            self.disconnect()
        self.err=""
        return True
    def remove(self,db):
        try:
            os.remove(db[1])
        except IOError as err:
            self.err="При удалении файла {0}:\n произошла ошибка\n{1}".format(db[1], err)
            return False
        else:
            self.err=""
            return True
    def backup(self):
    ##### нужно проакрить наличие баз данных!!!! и бекапа так как ошибки
        if not os.path.exists(self.db["db"][1]):
            self.err="База данных не инициализированна.\nФаил {0} не найден".format(self.db["db"][1])
            return False
        else:
            insert="""
            INSERT INTO backup (nameDb, nameBackup, date)
            VALUES (:nameDb, :nameBackup, :date);"""
            nameBackup=self.db["db"][1][:-4]+'-'+str(datetime.datetime.now())+".bcp"
            date=datetime.date.today()
            key={"nameDb":self.db["db"][1],
                "nameBackup":nameBackup,
                "date":date}
            self.connect(self.db["system"])
            try:
                shutil.copy(self.db["db"][1], nameBackup)
            except IOError as err:
                self.err="При создании резервной копии возникала ошибка:\n{0}".format(err)
                self.disconnect()
                return False
            else:
                self.err=""
                self.disconnect()
                return True
    def recovery(self, idBackup):
    # Востановление сохраненых бекапов
        select="""\
            SELECT nameBackup, nameDb FROM backup
            WHERE "idBackup"={0}""".format(idBackup)
        self.connect(self.db["system"])
        try:
            self.cur.execute(select)
        except sqlite3.DatabaseError as err:
            self.err="Востановление не удалось. Ошибка:{0}".format(err)
            self.disconnect()
            return False
        else:
            temp=self.cur.fetchone()
            self.disconnect()
            try:
                shutil.copy(temp[0],temp[1])
            except IOError as err:
                self.err="Востановление не удалось, ошибка:{0}".format(err)
                return False
            else:
                return True
    def sql(self, sql=None, key=None, write=False):
    #Выборка данных
        if sql==None:
            self.err="Не возможно выполнить операцию так как не заданны все параметры"
            return False
        else:
            self.connect(self.db["db"])
            if type(key)==dict:
                try:
                    self.cur.execute(sql, key)
                except sqlite3.DatabaseError as err:
                    self.err="Произошла ошибка: {0}".format(err)
                    self.disconnect()
                    return False
            elif key==None:
                try:
                    self.cur.execute(sql)
                except sqlite3.DatabaseError as err:
                    self.err="Произошла ошибка: {0}".format(err)
                    self.disconnect()
                    return False
            else:
                self.err="Произошла ошибка: задан не ключь в неверном формате"
                self.disconnect()
                return False
        if write==True:
            self.disconnect()
        self.err=""
        return True
    def select(self, sql, key=None):
        try:
            sql=SQL.select[sql]
        except KeyError as err:
            self.err="Внутреняя ошибка {0}".format(err)
            return False
        else:
            return self.sql(sql, key)
    def update(self, sql, key=None):
        try:
            sql=SQL.update[sql]
        except KeyError as err:
            self.err="Внутреняя ошибка {0}".format(err)
            return False
        else:
            return self.sql(sql, key, True)
    def insert(self, sql, key=None):
        try:
            sql=SQL.insert[sql]
        except KeyError as err:
            self.err="Внутреняя ошибка {0}".format(err)
        else:
            return self.sql(sql, key, True)
    def delete(self, sql, key=None):
        try:
            sql=SQL.delete[sql]
        except KeyError as err:
            self.err="Внутреняя ошибка {0}".format(err)
        else:
            return self.sql(sql, key, True)

class report:
#Создание отчета
    def __init__(self, title, info):
    # title -- название отчета
    # info -- кортеж или список (название столбцов, строки)
        self.settings={}
        self.css()
        self.copyright()
        self.table(info)
        self.title(title)
        self.name_file()
        self.gen()
        self.save()
    def copyright(self):
        self.settings['copyright']='Отчет создан с помощью програмы учета "Taxi". <a href="mailto:yura.bondarenko.job?">Бодаренко Юрий 2013</a>'
    def table(self, info):
    #составление с информации таблици
    #title - шапка таблици
    #info - информация для отчета
        def gen_td(td_inf, th=False):
        #генерация ячеек стрки
        #td_inf - информация для строки
        #th - включайт тег <th>, по умолчанию отключен и генерируется <td>
            if th:
                dh='h'
            else:
                dh='d'
            td=""
            for td_temp in td_inf:
                td='{0}\t\t<t{2}>{1}</t{2}>\n'.format(td, td_temp,dh)
            return (td)
        def gen_tr(tr_inf, title=False):
        #генерируется строка таблици
        #title - включает возможность генерации шапки таблици
            if title:
                tr='\t<tr>\n{0}\t</tr>\n'.format(gen_td(tr_inf, True))
            else:
                tr=''
                for tr_temp in tr_inf:
                    tr='{0}\t<tr>\n{1}\t</tr>\n'.format(tr,gen_td(tr_temp))
            return (tr)
        self.settings['table']='<p><table id="hor-minimalist-b">\n{0}{1}</table>'.format(gen_tr(info[0],True), gen_tr(info[1]))
    def css(self, file=r'style.css'):
    #загрузка  css из файла и сохранение в строку
    #file - имя файла в котором хранятся шаблоны
        css_file=open(file)
        css_gen=""
        for line in css_file:
            css_gen=css_gen+line
        self.settings['css']=css_gen
    def title(self,title):
        self.settings['title']=title
    def name_file(self):
        self.settings['name_file']='report_{0}_{1}.html'.format(self.settings['title'], str(datetime.datetime.now()))
    def gen(self):
    #сборка отчета в html
        self.settings['report']="""\
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>{0[title]}</title>
<style type="text/css">
<!--
{0[css]}
-->
</style>
<body>
{0[table]}
{0[copyright]}
</body>
            """.format(self.settings)
    def save(self):
    #сохранения отчета в фаил
        report_file=open(self.settings["name_file"], "w", encoding='utf-8')
        report_file.write(self.settings["report"])
        report_file.closed

class tableView(QtGui.QTableView):
    def __init__(self, sql, keys=None, check=False):
        QtGui.QTableView.__init__(self)
        self.check=check
        self.err=""
        self.sql=sql
        if keys==None:
            self.keys={}
        else:
            self.keys=keys
        self.base=base()
        self.load()
        self.setSortingEnabled(True)
        self.setCornerButtonEnabled(False)
        self.sortByColumn(0,QtCore.Qt.AscendingOrder)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.size()
        self.doubleClicked.connect(self.activ)
    def activ(self,const):
        self.index=self.model().item(const.row()).text()
    def size(self):
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
    def load(self):
        model=QtGui.QStandardItemModel()
        if self.base.select(self.sql, self.keys):
            for info in self.base.cur:
                strInfo=[]
                check=self.check
                for i in info:
                    temp=QtGui.QStandardItem(str(i))
                    if check:
                        temp.setCheckable(True)
                        check=False
                    strInfo.append(temp)
                model.appendRow(strInfo)
            self.base.disconnect()
            self.setModel(model)
            self.size()
            self.err=""
            return True
        else:
            self.err=self.base.err
            return False
    def selectId(self):
        index=self.selectedIndexes()
        if index:
            return self.model().item(index[0].row()).text()
        else:
            self.err="Выделите строку."
            return False
    def addRow(self, key):
        if self.base.select(self.sql):
            for info in self.base.cur:
                for item in key.items():
                    if info[1]==item[1]:
                        self.err="Такая запись уже существует."
                        self.base.disconnect()
                        return False
            self.base.insert(self.sql, key)
            self.load()
            self.err=""
            return True
        else:
            self.err=self.base.err
            return False
    def delRow(self):
        if self.base.delete(self.sql,{"id":self.selectId()}):
            self.load()
            self.err=""
            return True
        else:
            self.err=self.base.err
            return False
    def selectRow(self):
        self.len=self.model().rowCount()
        self.index=[]
        for i in range(0, self.len):
            if self.model().item(i).checkState():
                self.index.append(self.model().item(i).text())
        return True

class comboBox(QtGui.QComboBox):
    def __init__(self, sql=None, keys=None):
        QtGui.QComboBox.__init__(self)
        self.err=None
        self.activated["int"].connect(self.activ)
        self.base=base()
        self.sql=sql
        if keys==None:
            self.keys={}
        else:
            self.keys=keys
        #self.load()
    def activ(self, const):
        self.index=self.itemData(const)
    def load(self):
        if self.sql==None:
            return False
        self.clear()
        if self.base.select(self.sql, self.keys):
            for row in self.base.cur:
                len=row.__len__()
                text=""
                for i in range(1, len):
                    text="{0} {1}".format(text, row[i])
                data=row[0]
                self.addItem(text, data)
                try:
                    info=self.keys[self.sql]
                except KeyError:
                    self.setCurrentIndex(0)
                    self.emit(QtCore.SIGNAL("activated(int)"),0)
                else:
                    if row[0]==info:
                        index=self.count()
                        self.setCurrentIndex(index-1)
                        self.emit(QtCore.SIGNAL("activated(int)"),index-1)
            self.base.disconnect()
            return True
        else:
            self.err=self.base.err
            return False
    def setSql(self, sql, keys=None):
        if keys==None:
            self.keys={}
        else:
            self.keys=keys
        self.sql=sql
        self.load()

class dateEdit(QtGui.QDateEdit):
    def __init__(self, datePy=None):
        QtGui.QDateEdit.__init__(self)
        if datePy==None:
            self.now()
        else:
            self.setDatePy(datePy)
    def now(self):
        now=date.today()
        now=QtCore.QDate(now.year, now.month, now.day)
        self.setDate(now)
    def setDatePy (self, datePy):
        if type(datePy)==date:
            self.setDate(QtCore.QDate(datePy.year, datePy.month, datePy.day))
            return True
        else:
            return False


class modelInfo():
    def __init__(self):
        self.err=None
        self.base=base()
        self.keys={}
    def loadUserCombo(self):
        self.userCombo=comboBox("login")
        self.userCombo.activated.connect(lambda: self.keys.update({"idUser":self.userCombo.index}))
        self.userCombo.load()
        if self.userCombo.count()==0:
            self.base.insert("accessAdmin")
            self.base.insert("installPost")
            self.base.insert("installUser")
            self.base.insert("installTimeWork")
            self.base.insert("installStatus")
            self.base.insert("installPayment")
            self.userCombo.load()
        return self.userCombo
    def check(self, password=""):
        self.base.select("password", self.keys)
        info=self.base.cur.fetchone()
        self.base.disconnect()
        checkPass=hashlib.md5()
        checkPass.update(password.encode("UTF-8"))
        password=checkPass.hexdigest()
        if password==info[0]:
            self.err=None
            return True
        else:
            self.err="Введен не верный пароль"
            return False
    def loadCarTable(self):
        self.carTable=tableView("car")
        self.carTable.doubleClicked.connect(self.loadCarInfo)
        return self.carTable
    def loadCarCombo(self):
        self.carCombo=comboBox("carCombo")
        self.carCombo.activated.connect(lambda: self.keys.update({"idCar":self.carCombo.index}))
        self.carCombo.load()
        return self.carCombo
    def loadCarInfo(self):
        self.keys["idCar"]=self.carTable.index
        self.base.select("carInfo", self.keys)
        info=self.base.cur.fetchone()
        self.keys.update({"carName":info[0],
                   "model":info[1],
                   "color":info[2],
                   "number":info[3],
                   "radio":info[4],
                   "info":info[5]})
        self.base.disconnect()
        return True
    def saveCar(self, newKeys):
        self.keys.update(newKeys)
        if self.base.update("carInfo", self.keys):
            self.carTable.load()
            return True
        else:
            return False
    def setCarInfo(self, name="", number="", radio="", info=""):
        self.keys["name"]=name
        self.keys["number"]=number
        self.keys["radio"]=radio
        self.keys["info"]=info
    def loadCarDriverTable(self):
        self.carDriverTable=tableView("driverCar", self.keys)
        self.carDriverTable.doubleClicked.connect(self.loadPeriodInfo)
        return self.carDriverTable
    def loadCarRepairTable(self):
        self.carRepairTable=tableView("carRepair", self.keys)
        self.carRepairTable.doubleClicked.connect(lambda: self.keys.update({"idRepair":self.carRepairTable.index}))
        self.carRepairTable.doubleClicked.connect(self.loadRepairInfo)
        return self.carRepairTable
    def loadDetailRepairTable(self):
        self.detailRepairTable=tableView("detailRepair", self.keys)
        self.detailRepairTable.doubleClicked.connect(lambda: self.keys.update({"idDetail":self.carRepairTable.index}))
        self.detailRepairTable.doubleClicked.connect(self.loadDetailInfo)
        return self.detailRepairTable
    def loadDetailNewTable(self):
        self.detailNewTable=tableView("detailNew")
        return self.detailNewTable
    def addCarDriver(self, keys=None):
        if type(keys)==dict:
            self.keys.update(keys)
            if self.base.insert("carDriver", self.keys):
                self.carDriverTable.load()
                self.err=None
                return True
            else:
                self.err=self.base.err
                return False
        else:
            self.err="Введенны некоректные данные."
            return False
    def deleteCar(self):
        self.base.delete("car", self.keys)
        self.carTable.load()
        return True
    def loadPeriodInfo(self):
        self.keys["idDriverCar"]=self.carDriverTable.index
        self.base.select("driverCarInfo", self.keys)
        info=self.base.cur.fetchone()
        self.keys.update({"driverName":"{0[1]} {0[0]} {0[2]}".format(info),
                          "dateIn":info[3],
                          "dateOut":info[4]})
        self.base.disconnect()
    def updatePeriodInfo(self, keys):
        self.keys.update(keys)
        if self.base.update("driverCarInfo", self.keys):
            self.carDriverTable.load()
            return True
        else:
            self.err=self.base.err
            return False
    def deletePeriodInfo(self):
        if self.base.delete("driverCarInfo", self.keys):
            self.carDriverTable.load()
            return True
        else:
            self.err=self.base.err
            return False
    def loadDriverInfoTable(self):
        self.driver=tableView("carDriver", self.keys)
        return self.driver
    def loadMechanicCombo(self):
        self.mechanicCombo=comboBox("mechanic")
        self.mechanicCombo.activated.connect(lambda: self.keys.update({"idWorker":self.mechanicCombo.index}))
        self.mechanicCombo.load()
        return self.mechanicCombo
    def addCar(self, newKeys):
        self.keys.update(newKeys)
        if self.base.insert("car", self.keys):
            self.carTable.load()
            return True
        else:
            return False
    def endDriver(self, dateOut):
        self.keys["idWorker"]=self.carDriverTable.selectId()
        if type(dateOut)==date:
            self.keys["dateOut"]=dateOut
            if self.base.update("driverCar", self.keys):
                self.carDriverTable.load()
                return True
            else:
                return False
        else:
            return False
    def loadCarColorTable(self):
        self.carColorTable=tableView("carColor")
        return self.carColorTable
    def loadCarColorCombo(self):
        self.carColorCombo=comboBox("carColor")
        self.carColorCombo.activated.connect(lambda: self.keys.update({"idColor":self.carColorCombo.index}))
        self.carColorCombo.load()
        return self.carColorCombo
    def loadCarModelTable(self):
        self.carModelTable=tableView("carModel")
        return self.carModelTable
    def loadCarModelCombo(self):
        self.carModelCombo=comboBox("carModel")
        self.carModelCombo.activated.connect(lambda: self.keys.update({"idModel":self.carModelCombo.index}))
        self.carModelCombo.load()
        return self.carModelCombo
    def loadDetailTypeTable(self):
        self.detailTypeTable=tableView("detailType")
        return self.detailTypeTable
    def loadDetailMadeTable(self):
        self.detailMadeTable=tableView("detailMade")
        return  self.detailMadeTable
    def loadCatalogCombo(self):
        self.catalogCombo=comboBox("catalog")
        self.catalogCombo.activated.connect(lambda: self.keys.update({"code":self.catalogCombo.index}))
        self.catalogCombo.load()
        return self.catalogCombo
    def loadCatalogTable(self):
        self.catalogTable=tableView("catalog")
        self.catalogTable.doubleClicked.connect(self.loadCatalogInfo)
        return self.catalogTable
    def loadCatalogInfo(self):
        pass
    def loadDetailTypeCombo(self):
        self.detailTypeCombo=comboBox("detailType")
        self.detailTypeCombo.activated.connect(lambda: self.keys.update({"idType":self.detailTypeCombo.index}))
        self.detailTypeCombo.load()
        return self.detailTypeCombo
    def loadWorkerCombo(self):
        self.workerCombo=comboBox("worker", self.keys)
        self.workerCombo.activated.connect(lambda: self.keys.update({"idWorker":self.workerCombo.index}))
        self.workerCombo.load()
        return self.workerCombo
    def loadDetailMadeCombo(self):
        self.detailMadeCombo=comboBox("detailMade")
        self.detailMadeCombo.activated.connect(lambda: self.keys.update({"idMade":self.detailMadeCombo.index}))
        self.detailMadeCombo.load()
        return self.detailMadeCombo
    def addToCatalog(self, name="", about=""):
        if name=="":
            return False
        else:
            self.keys["name"]=name
            self.keys["about"]=about
            newRow="{0[name]}{0[idType]}{0[idMade]}".format(self.keys)
            self.base.select("catalogCheck")
            for info in self.base.cur:
                row=""
                for i in info:
                    row="{0}{1}".format(row, i)
                if row==newRow:
                    self.base.disconnect()
                    return False
            self.base.disconnect()
            self.base.insert("catalog", self.keys)
            self.catalogTable.load()
            return True
    def loadRepairClassTable(self):
        self.repairClassTable=tableView("classRepair")
        return self.repairClassTable
    def loadRepairClassCombo(self):
        self.repairClassCombo=comboBox("classRepair")
        self.repairClassCombo.activated.connect(lambda: self.keys.update({"idClass":self.repairClassCombo.index}))
        self.repairClassCombo.activated.connect(self.loadRepairTypeCombo)
        self.repairClassCombo.load()
        return self.repairClassCombo
    def loadRepairTypeTable(self):
        self.repairTypeTable=tableView("typeRepair")
        return self.repairTypeTable
    def loadRepairTypeCombo(self):
        try:
            self.keys["idClass"]
        except KeyError:
            try:
                self.__dict__["repairTypeCombo"]
            except KeyError:
                self.repairTypeCombo=comboBox("typeRepair", self.keys)
        else:
            try:
                self.keys["repairTypeCombo"]
            except KeyError:
                self.repairTypeCombo=comboBox("typeRepair", self.keys)
        self.repairTypeCombo.activated.connect(lambda: self.keys.update({"idType":self.repairTypeCombo.index}))
        self.repairTypeCombo.load()
        return self.repairTypeCombo
    def loadRepairTable(self):
        self.repairTable=tableView("repair")
        self.repairTable.doubleClicked.connect(self.loadRepairInfo)
        return self.repairTable
    def loadRepairInfo(self):
        self.base.select("repairInfo", self.keys)
        info=self.base.cur.fetchall()[0]
        self.base.disconnect()
        self.keys.update({"idClass":info[0],
                          "idType":info[1],
                          "idCar":info[2],
                          "idWorker":info[3],
                          "date":info[4],
                          "kmage":info[5],
                          "price":info[6]})
    def addRepair(self, keys=None):
        if type(keys)==dict:
            self.keys.update(keys)
            if self.base.insert("repair", self.keys) and self.base.select("lastRepair"):
                self.repairTable.load()
                self.keys["idRepair"]=self.base.cur.fetchone()[0]
                self.base.disconnect()
                if self.addDetailToRepair():
                    return True
                else:
                    return False
            else:
                self.err="Внутреняя ошибка.\n{0}\nОбратитесь к разработчику.".format(self.base.err)
                return False
        else:
            self.err="Внутреняя ошибка.\nОбратитесь к разработчику."
            return False
    def addRepairCar(self,keys):
        if self.addRepair(keys):
            self.carRepairTable.load()
            return True
        else:
            return False
    def addDetailToRepairCar(self):
        if self.addDetailToRepair():
            self.detailRepairTable.load()
            return True
        else:
            return False
    def updateRepair(self,keys=None):
        if type(keys)==dict:
            self.keys.update(keys)
            if self.base.update("repair", self.keys):
                self.detailRepairTable.load()
                return True
        self.err=self.base.err
        return False
    def repealRepair(self):
        self.base.select("")
    def addDetailToRepair(self):
        self.newDetailInstallTable.selectRow()
        index=self.newDetailInstallTable.index
        if len(index)>0:
            for i in self.newDetailInstallTable.index:
                self.keys["idDetail"]=i
                if self.base.insert("detailHis", self.keys)==False or self.base.update("detailInstall", self.keys)==False:
                    self.err="Деталь с номером {0} не списалась.\n{1}\nОбратитесь к разработчику.".format(i, self.base.err)
                    return False
                else:
                    if self.base.update("numberMinus",self.keys):
                        self.newDetailTable.load()
                        self.unfitDetailTable.load()
                        self.useDetailTable.load()
        return True

    def loadWorkerTable(self):
        self.workerTable=tableView("worker")
        self.workerTable.doubleClicked.connect(lambda: self.keys.update({"idWorker":self.workerTable.index}))
        self.workerTable.doubleClicked.connect(self.loadWorkerInfo)
        return self.workerTable
    def loadFormerWorkerTable(self):
        self.formerWorkerTable=tableView("formerWorker")
        self.formerWorkerTable.doubleClicked.connect(lambda: self.keys.update({"idWorker":self.formerWorkerTable.index}))
        self.formerWorkerTable.doubleClicked.connect(self.loadWorkerInfo)
        return self.formerWorkerTable
    def loadWorkerCarTable(self):
        self.workerCarTable=tableView("workerCar", self.keys)
        self.workerCarTable.doubleClicked.connect(lambda: self.keys.update({"idDriverCar":self.workerCarTable.index}))
        return self.workerCarTable
    def loadWorkerRepairTable(self):
        self.workerRepairTable=tableView("workerRepair", self.keys)
        self.workerRepairTable.doubleClicked.connect(lambda: self.keys.update({"idDriverCar":self.workerRepairTable.index}))
        return self.workerRepairTable
    def loadWorkerInfo(self):
        self.base.select("workerInfo", self.keys)
        info=self.base.cur.fetchone()
        self.base.disconnect()
        keys={"name1":info[0],
              "name2":info[1],
              "name3":info[2],
              "passport":info[3],
              "addressReg":info[4],
              "addressRes":info[5],
              "phoneMob":info[6],
              "phoneHome":info[7],
              "eMail":info[8],
              "info":info[9]}
        self.keys.update(keys)
    def deleteWorker(self):
        pass
    def saveWorker(self, newKeys):
        self.keys.update(newKeys)
        if self.base.update("workerInfo", self.keys):
            self.workerTable.load()
            self.formerWorkerTable.load()
            return True
        else:
            return False
    def addWorker(self, newKeys):
        self.keys.update(newKeys)
        if self.base.insert("worker", self.keys):
            self.workerTable.load()
            self.formerWorkerTable.load()
            return True
        else:
            return False
    def loadDetailBaseTable(self):
        self.detailBaseTable=tableView("detailBase")
        self.detailBaseTable.doubleClicked.connect(self.loadDetailInfo)
        return self.detailBaseTable
    def loadDetailInfo(self):
        self.base.select("detailInfo", self.keys)
        info=self.base.cur.fetchone()
        self.keys.update({"name":info[0],
                          "type":info[1],
                          "made":info[2],
                          "price":info[3],
                          "payment":info[4],
                          "date":info[5],
                          "status":info[6],
                          "about":info[7]})
    def loadPostTable(self):
        self.postTable=tableView("post")
        return self.postTable
    def loadPostCombo(self):
        self.postCombo=comboBox("post")
        self.postCombo.activated.connect(lambda: self.keys.update({"idPost":self.postCombo.index}))
        self.postCombo.load()
        return self.postCombo
    def loadTimeWorkTable(self):
        self.timeWorkTable=tableView("timeWork")
        self.timeWorkTable.doubleClicked.connect(self.loadTimeWorkInfo)
        return self.timeWorkTable
    def loadAccessCombo(self):
        self.accessCombo=comboBox("access")
        self.accessCombo.activated.connect(lambda: self.keys.update({"idAccess":self.accessCombo.index}))
        self.accessCombo.load()
        return self.accessCombo
    def loadAccessTable(self):
        self.accessTable=tableView("access")
        self.accessTable.doubleClicked.connect(self.loadAccessInfo)
        return self.accessTable
    def loadAccessInfo(self):
        self.keys["idAccess"]=self.accessTable.index
        self.base.select("accessInfo", self.keys)
        info=self.base.cur.fetchone()
        self.base.disconnect()
        for i in range (0, 11):
            self.keys["access{0}".format(i)]=info[i]
    def setAccess(self):
        self.base.update("access", self.keys)
        for i in range (0, 11):
            self.keys["access{0}".format(i)]=0
    def loadLastAccess(self):
        self.base.select("lastAccess", self.keys)
        self.keys["idAccess"]=self.base.cur.fetchone()[0]
    def loadAllWorkerCombo(self):
        self.allWorkerCombo=comboBox("workerAll")
        self.allWorkerCombo.activated.connect(lambda: self.keys.update({"idWorker":self.allWorkerCombo.index}))
        self.allWorkerCombo.load()
        return self.allWorkerCombo
    def setTimeWork(self, dateIn=None, dateOut=None):
        self.keys.update({"dateIn":dateIn,
                          "dateOut":dateOut})
        if dateOut==None:
            self.base.insert("timeWork", self.keys)
        else:
            self.base.update("timeWork", self.keys)
        self.timeWorkTable.load()
    def loadTimeWorkInfo(self):
        self.keys["idTimeWork"]=self.timeWorkTable.index
        self.base.select("timeWorkInfo",self.keys)
        info=self.base.cur.fetchone()
        self.base.disconnect()
        self.keys.update({"idWorker":info[0],
                          "idPost":info[1],
                          "dateIn":info[2]})
    def setPassword(self, password):
        checkPass=hashlib.md5()
        checkPass.update(password.encode("UTF-8"))
        password=checkPass.hexdigest()
        self.keys["pass"]=password
        self.base.update("password", self.keys)
        self.clearKey()
    def clearKey(self):
        self.keys={}
    def backup(self):
        pass
    def recovery(self):
        pass
    def loadNewDetailTable(self):
        self.newDetailTable=tableView("newDetail")
        self.newDetailTable.doubleClicked.connect(lambda:self.keys.update({"code":self.newDetailTable.index}))
        return self.newDetailTable
    def loadNewDetailSubTable(self):
        self.newDetailSubTable=tableView("newDetailSub", self.keys)
        self.newDetailSubTable.doubleClicked.connect(lambda:self.keys.update({"idDetail":self.newDetailSubTable.index}))
        return self.newDetailSubTable
    def loadNewDetailInstallTable(self):
        self.newDetailInstallTable=tableView("newDetailInstall", self.keys, True)
        return self.newDetailInstallTable
    def loadUseDetailTable(self):
        self.useDetailTable=tableView("useDetail")
        self.useDetailTable.doubleClicked.connect(self.loadDetailInfo)
        return self.useDetailTable
    def loadUnfitDetailTable(self):
        self.unfitDetailTable=tableView("unfitDetail")
        self.unfitDetailTable.doubleClicked.connect(self.loadDetailInfo)
        return self.unfitDetailTable
    def loadPaymentCombo(self):
        self.paymentCombo=comboBox("payment")
        self.paymentCombo.activated.connect(lambda: self.keys.update({"idPayment":self.paymentCombo.index}))
        self.paymentCombo.load()
        return self.paymentCombo
    def addDetail(self, number, dateBay, price):
        self.keys.update({"date":dateBay,
                          "price":price})
        self.keys["number"]=number
        self.base.update("number", self.keys)
        for i in range(0, number):
            self.base.insert("detail", self.keys)
        self.newDetailTable.load()
