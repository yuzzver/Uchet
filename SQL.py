# -*- coding: utf-8 -*-
__author__ = 'Bondarenko Yura'

#Системная база данных
system={}
#Бекапы
system["backup"]="""\
    CREATE TABLE IF NOT EXISTS backup(
        idBackup INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        viewName VARCHAR(100) NOT NULL,
        nameDb VARCHAR (100) NOT NULL,
        nameBackup VARCHAR (150) NOT NULL,
        info VARCHAR(500) NOT NULL,
        date date NOT NULL
    );
    """

#Основная база данных
db={}
#Модели автомобилей
db["modelCar"]="""\
    CREATE TABLE IF NOT EXISTS modelCar (
        idModel INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        model VARCHAR(150) NOT NULL
    );
    """
#Цвет
db["color"]="""\
    CREATE TABLE IF NOT EXISTS color (
        idColor INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        color VARCHAR(150) NOT NULL
    );
"""
#Авто INFO
db["car"]="""\
    CREATE TABLE IF NOT EXISTS car (
        idCar INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        carName VARCHAR(50) NOT NULL,
        idModel INTEGER,
        idColor INTEGER,
        radio VARCHAR(20),
        number VARCHAR(15),
        info VARCHAR(300),
        FOREIGN KEY (idModel) REFERENCES modelCar(idModel) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idColor) REFERENCES color(idColor) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """
#Работники
db["worker"]="""\
    CREATE TABLE IF NOT EXISTS worker (
        idWorker INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        name1 VARCHAR(30)NOT NULL,
        name2 VARCHAR(20),
        name3 VARCHAR(20),
        passport VARCHAR(300),
        addressReg VARCHAR(150),
        addressRes VARCHAR(150),
        phoneMob VARCHAR(15),
        phoneHome VARCHAR(15),
        eMail VARCHAR(100),
        info VARCHAR(500),
        pass VARCHAR(100)
    );
    """
#Период работы
db["timeWork"]="""\
    CREATE TABLE IF NOT EXISTS timeWork (
        idTimeWork INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        idWorker INTEGER,
        idPost INTEGER,
        dateIn date NOT NULL,
        dateOut date DEFAULT NULL,
        FOREIGN KEY (idWorker) REFERENCES worker(idWorker) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idPost) REFERENCES post(idPost) ON DELETE CASCADE ON UPDATE CASCADE
    );
"""
#Права доступа
db["access"]="""\
    CREATE TABLE IF NOT EXISTS access(
        idAccess INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
        nameAccess VARCHAR(20),
        carRead INTEGER DEFAULT 0,
        carWrite INTEGER DEFAULT 0,
        repairRead INTEGER DEFAULT 0,
        repairWrite INTEGER DEFAULT 0,
        workerRead INTEGER DEFAULT 0,
        workerWrite INTEGER DEFAULT 0,
        detailRead INTEGER DEFAULT 0,
        detailWrite INTEGER DEFAULT 0,
        systemRead INTEGER DEFAULT 0,
        systemWrite INTEGER DEFAULT 0,
        allDelete INTEGER DEFAULT 0
    );
"""
#Каталог должностей
db["post"]="""\
    CREATE TABLE IF NOT EXISTS post(
        idPost INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,
        post VARCHAR(50) NOT NULL,
        idAccess INTEGER,
        FOREIGN KEY (idAccess) REFERENCES access(idAccess) ON DELETE CASCADE ON UPDATE CASCADE
    );
"""
#Типы деталей
db["typeDetail"]="""\
    CREATE TABLE IF NOT EXISTS typeDetail (
        idType INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        type VARCHAR(100)
    );
"""
#Производитель деталей
db["made"]="""\
    CREATE TABLE IF NOT EXISTS made (
        idMade INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
        made VARCHAR(150)
    );
"""
#Каталог деталей
db["catalog"]="""\
    CREATE TABLE IF NOT EXISTS catalog (
        code INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL,
        idType INTEGER,
        name VARCHAR(120) NOT NULL,
        idMade INTEGER,
        number INTEGER DEFAULT 0,
        about VARCHAR(250),
        FOREIGN KEY (idType) REFERENCES typeDetail(idType) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idMade) REFERENCES made(idMade) ON DELETE CASCADE ON UPDATE CASCADE
    );
"""

db["status"]="""\
    CREATE TABLE IF NOT EXISTS status(
        idStatus INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        status VARCHAR(20)
    );
"""
db["payment"]="""\
    CREATE TABLE IF NOT EXISTS payment(
        idPayment INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        payment VARCHAR(20) NOT NULL
    );
"""
#База деталей
db["detailBase"]="""\
    CREATE TABLE IF NOT EXISTS detailBase (
        idDetail INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        code INTEGER,
        price FLOAT NOT NULL,
        date date NOT NULL,
        idPayment INTEGER,
        idStatus VARCHAR(20),
        FOREIGN KEY (code) REFERENCES catalog(code) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idStatus) REFERENCES status(idStatus) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idPayment) REFERENCES payment(idPayment) ON DELETE CASCADE ON UPDATE CASCADE
    );
"""
#История деталей
db["detailHis"]="""\
    CREATE TABLE IF NOT EXISTS detailHis (
        idDetailHis INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        idDetail INTEGER,
        idRepair INTEGER,
        dateOut date DEFAULT (null),
        kmageOut INTEGER DEFAULT (null),
        FOREIGN KEY (idDetail) REFERENCES detailBase(idDetail) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idRepair) REFERENCES repairCar(idRepair) ON DELETE CASCADE ON UPDATE CASCADE
    );
"""
#Водители машин
db["driverCar"]="""\
    CREATE TABLE IF NOT EXISTS driverCar (
        idDriverCar INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        idCar INTEGER,
        idWorker INTEGER,
        dateIn date,
        dateOut date,
        FOREIGN KEY (idCar) REFERENCES car(idCar) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idWorker) REFERENCES worker(idWorker) ON DELETE CASCADE ON UPDATE CASCADE
    );
    """
#Класс ремонта
db["classRepair"]="""\
    CREATE TABLE IF NOT EXISTS classRepair (
        idClass INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,
        class VARCHAR(100) NOT NULL
    );
"""
#Тип ремонта
db["typeRepair"]="""\
    CREATE TABLE IF NOT EXISTS "typeRepair" (
        idType INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        type VARCHAR(150) NOT NULL,
        idClass INTEGER,
        FOREIGN KEY (idClass) REFERENCES classRepair(idClass) ON DELETE CASCADE ON UPDATE CASCADE
    );
"""
#Ремаонт автомобилей
db["repairCar"]="""\
    CREATE TABLE IF NOT EXISTS "repairCar" (
        idRepair INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        idCar INTEGER,
        idType INTEGER,
        idWorker INTEGER,
        date date,
        kmAge INTEGER,
        price FLOAT,
        FOREIGN KEY (idCar) REFERENCES car(idCar) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idType) REFERENCES typeRepair(idType) ON DELETE CASCADE ON UPDATE CASCADE,
        FOREIGN KEY (idWorker) REFERENCES worker(idWorker) ON DELETE CASCADE ON UPDATE CASCADE
    );
"""

select={}
#Обшая информация о машине
select["car"]="""\
    SELECT idCar, carName, model, color, number
    FROM car
    LEFT OUTER JOIN color ON car.idColor=color.idColor
    LEFT OUTER JOIN modelCar ON car.idModel=modelCar.idModel"""
select["carCombo"]="""\
    SELECT idCar, carName, model, number
    FROM car
    LEFT OUTER JOIN modelCar ON car.idModel=modelCar.idModel
"""
#Развернутая информация по машине
select["carInfo"]="""\
    SELECT carName, model, color, number, radio, info
    FROM car
    LEFT OUTER JOIN modelCar ON car.idModel=modelCar.idModel
    LEFT OUTER JOIN color ON car.idColor=color.idColor
    WHERE car.idCar=:idCar"""
#Водители автомобиля
select["driverCar"]="""\
    SELECT idDriverCar, name1, name2, dateIn, dateOut
    FROM driverCar
    LEFT OUTER JOIN worker ON driverCar.idWorker=worker.idWorker
    WHERE driverCar.idCar=:idCar"""
select["driverCarInfo"]="""\
    SELECT name1, name2, name3, dateIn, dateOut
    FROM driverCar
    LEFT OUTER JOIN worker ON driverCar.idWorker=worker.idWorker
    WHERE driverCar.idDriverCar=:idDriverCar"""
select["carDriver"]="""\
    SELECT carName, dateIn, dateOut
    FROM driverCar
    LEFT OUTER JOIN car ON driverCar.idCar=car.idCar
    WHERE driverCar.idWorker=:idWorker"""
#Ремонты машины
select["carRepair"]="""\
    SELECT idRepair, class, type, name1, name2, date, price
    FROM repairCar
    LEFT OUTER JOIN typeRepair ON repairCar.idType=typeRepair.idType
    LEFT OUTER JOIN classRepair ON typeRepair.idClass=classRepair.idClass
    LEFT OUTER JOIN worker ON repairCar.idWorker=worker.idWorker
    WHERE repairCar.idCar=:idCar"""
#Детали на ремонт
select["detailRepair"]="""\
    SELECT detailHis.idDetail, name, type, detailBase.price, repairCar.date, detailHis.dateOut
    FROM detailHis
    LEFT OUTER JOIN repairCar ON detailHis.idRepair=repairCar.idRepair
    LEFT OUTER JOIN detailBase ON detailHis.idDetail=detailBase.idDetail
    LEFT OUTER JOIN catalog ON detailBase.code=catalog.code
    LEFT OUTER JOIN typeDetail ON catalog.idType=typeDetail.idType
    WHERE detailHis.idRepair=:idRepair"""

#Работники
select["workerList"]="""\
    SELECT worker.idWorker, name1, name2
    FROM worker
    LEFT OUTER JOIN (SELECT idWorker,idCar FROM driverCar
                    WHERE idCar=:idCar AND dateOut is Null) as driver ON worker.idWorker=driver.idWorker
    WHERE driver.idCar is Null"""
select["worker"]="""\
    SELECT worker.idWorker, name1, name2, name3
    FROM worker
    INNER JOIN (SELECT idWorker FROM timeWork
                    WHERE dateOut is Null) as time ON worker.idWorker=time.idWorker"""
select["formerWorker"]="""\
    SELECT worker.idWorker, name1, name2, name3
    FROM worker
    LEFT OUTER JOIN (SELECT idWorker FROM timeWork
                    WHERE dateOut is Null) as time ON worker.idWorker=time.idWorker
    WHERE time.idWorker is Null"""
select["workerInfo"]="""\
    SELECT name1, name2, name3, passport, addressReg, addressRes, phoneMob, phoneHome, eMail, info
    FROM worker
    WHERE idWorker=:idWorker
"""
select["workerCar"]="""\
    SELECT idDriverCar, carName, dateIn, dateOut
    FROM driverCar
    LEFT OUTER JOIN car ON driverCar.idCar=car.idCar
    WHERE idWorker=:idWorker
"""
select["workerRepair"]="""\
    SELECT idRepair, carName, class, type, date
    FROM repairCar
    LEFT OUTER JOIN car ON repairCar.idCar=car.idCar
    LEFT OUTER JOIN typeRepair ON repairCar.idType=typeRepair.idType
    LEFT OUTER JOIN classRepair ON typeRepair.idClass=classRepair.idClass
    WHERE idWorker=:idWorker
"""
select["mechanic"]="""\
    SELECT worker.idWorker, name1, name2, name3
    FROM worker
    INNER JOIN timeWork ON worker.idWorker=timeWork.idWorker\
    WHERE idPost=3 AND dateOut is Null"""
#Авторизация
select["login"]="""\
    SELECT idWorker, name1, name2
    FROM worker"""
select["password"]="""\
    SELECT pass
    FROM worker
    WHERE idWorker=:idUser"""
#Какие детали на складе
select["newDetail"]="""\
    SELECT DISTINCT catalog.code, type, name, made, number
    FROM catalog
    LEFT OUTER JOIN detailBase ON catalog.code=detailBase.code
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade
    LEFT OUTER JOIN typeDetail ON catalog.idType=typeDetail.idType
    WHERE number>0 """
select["newDetailSub"]="""\
    SELECT idDetail, date, payment, price
    FROM detailBase
    LEFT OUTER JOIN catalog ON detailBase.code=catalog.code
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade
    LEFT OUTER JOIN payment ON payment.idPayment=detailBase.idPayment
    WHERE (detailBase.idStatus=0 OR detailBase.idStatus=1) AND detailBase.code=:code"""
select["newDetailInstall"]="""\
    SELECT idDetail, name, type, made, date, payment, price
    FROM detailBase
    LEFT OUTER JOIN catalog ON detailBase.code=catalog.code
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade
    LEFT OUTER JOIN payment ON payment.idPayment=detailBase.idPayment
    LEFT OUTER JOIN typeDetail ON catalog.idType=typeDetail.idType
    WHERE (detailBase.idStatus=0 OR detailBase.idStatus=1)"""
select["detailInfo"]="""\
    SELECT name, type, made, price, payment, date, status, about
    FROM detailBase
    LEFT OUTER JOIN catalog ON detailBase.code=catalog.code
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade
    LEFT OUTER JOIN status ON status.idStatus=detailBase.idStatus
    LEFT OUTER JOIN payment ON payment.idPayment=detailBase.idPayment
    LEFT OUTER JOIN typeDetail ON catalog.idType=typeDetail.idType
    WHERE idDetail=:idDetail"""
select["detailHis"]="""\
    SELECT idDetail, name, price
    FROM detailBase
    LEFT OUTER JOIN catalog ON detailBase.code=catalog.code
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade
    WHERE (detailBase.idStatus=0 OR detailBase.idStatus=1) AND detailBase.code=:code"""
select["useDetail"]="""\
    SELECT idDetail, name, made, price
    FROM detailBase
    LEFT OUTER JOIN catalog ON detailBase.code=catalog.code
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade
    WHERE detailBase.idStatus=2"""
select["unfitDetail"]="""\
    SELECT idDetail, name, made, price
    FROM detailBase
    LEFT OUTER JOIN catalog ON detailBase.code=catalog.code
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade
    WHERE detailBase.idStatus=3"""
#Все ремонты
select["repair"]="""\
    SELECT idRepair, class, type, carName, name1, name2, date
    FROM repairCar
    LEFT OUTER JOIN typeRepair ON repairCar.idType=typeRepair.idType
    LEFT OUTER JOIN classRepair ON typeRepair.idClass=classRepair.idClass
    LEFT OUTER JOIN car ON repairCar.idCar=car.idCar
    LEFT OUTER JOIN worker ON repairCar.idWorker=worker.idWorker """
select["lastRepair"]="""\
    SELECT idRepair
    FROM repairCar
    ORDER BY idRepair DESC
    LIMIT 1
"""
select["repairInfo"]="""\
SELECT idClass, repairCar.idType, idCar, idWorker, date, kmage, price
    FROM repairCar
    LEFT OUTER JOIN typeRepair ON repairCar.idType=typeRepair.idType
WHERE idRepair=:idRepair"""
select["lastRepair"]="""\
    SELECT idRepair
    FROM repairCar
    ORDER BY idRepair DESC
    LIMIT 1
"""
#Типы ремота
select["typeRepair"]="""\
    SELECT idType, type, class
    FROM typeRepair
    LEFT OUTER JOIN classRepair ON typeRepair.idClass=classRepair.idClass"""
#Класс ремонта
select["classRepair"]="""\
    SELECT idClass, class
    FROM classRepair
"""
#Долдности
select["post"]="""\
    SELECT idPost, post, nameAccess
    FROM post
    LEFT OUTER JOIN access ON post.idAccess=access.idAccess
"""
#Тип детали
select["detailType"]="""\
    SELECT idType, type
    FROM typeDetail
"""
#Модель машины
select["carModel"]="""\
    SELECT idModel, model
    FROM modelCar"""
#Цвет машины
select["carColor"]="""\
    SELECT idColor, color
    FROM color"""
select["detailMade"]="""\
    SELECT idMade, made
    FROM made"""
select["catalog"]="""\
    SELECT code, name, type, made
    FROM catalog
    LEFT OUTER JOIN typeDetail ON catalog.idType=typeDetail.idType
    LEFT OUTER JOIN made ON catalog.idMade=made.idMade"""
select["catalogCheck"]="""\
    SELECT name, idType, idMade
    FROM catalog"""
select["access"]="""\
    SELECT idAccess, nameAccess
    FROM access"""

select["timeWork"]="""\
    SELECT idTimeWork, name1, name2, post, dateIn, dateOut
    FROM timeWork
    LEFT OUTER JOIN post ON timeWork.idPost=post.idPost
    LEFT OUTER JOIN worker ON timeWork.idWorker=worker.idWorker
"""
select["timeWorkInfo"]="""\
    SELECT idWorker, idPost, dateIn
    FROM timeWork
    WHERE idTimeWork=:idTimeWork
"""
select["accessInfo"]="""\
    SELECT carRead, carWrite, repairRead, repairWrite, workerRead, workerWrite, detailRead, detailWrite, systemRead, systemWrite, allDelete
    FROM access
    WHERE idAccess=:idAccess
"""
select["lastAccess"]="""\
    SELECT idAccess
    FROM access
    WHERE nameAccess=:info
"""
select["number"]="""\
    SELECT catalog
    FROM number
    WHERE code=:code"""
select["workerAll"]="""\
SELECT idWorker, name1, name2, name3
FROM worker
"""
select["payment"]="""\
    SELECT idPayment, payment
    FROM payment
"""
select["code"]="""\
SELECT code
FROM catalog
LEFT OUTER JOIN detailBase ON catalog.code=detailBase.code
WHERE idDetail=:idDetail
"""
#Перечень машин
#Перечень механиков



insert={}

insert["carDriver"]="""\
    INSERT INTO driverCar(idCar, idWorker, dateIn, dateOut)
    VALUES (:idCar, :idWorker, :dateIn, :dateOut) """
insert["car"]="""\
    INSERT INTO car(carName, idModel, idColor, radio, number, info)
    VALUES (:carName, :idModel, :idColor, :radio, :number, :info) """
insert["accessAdmin"]="""\
    INSERT INTO access(idAccess ,nameAccess, carRead, carWrite, repairRead, repairWrite, workerRead, workerWrite, detailRead, detailWrite, systemRead, systemWrite, allDelete)
    VALUES (0, "root", 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2) """
insert["installPost"]="""\
    INSERT INTO post(idPost, post, idAccess)
    VALUES (0, "admin", 0) """
insert["installUser"]="""\
    INSERT INTO worker(idWorker, name1, name2, name3, eMail, pass)
    VALUES (0, "Юра", "Бондаренко", "Сергеевич", "yuzzver@i.ua", "72026ddabae84b46bfd9bbba1c8f9a5c") """
insert["installTimeWork"]="""\
    INSERT INTO timeWork(idTimeWork, idWorker, idPost, dateIn)
    VALUES (0, 0, 0, "2013-06-10")"""
insert["installStatus"]="""\
    INSERT INTO status (idStatus, status)
    VALUES (0, "Новая"), (1, "Б\у"), (2, "Установленная"), (3, "Списана")"""
insert["installPayment"]="""\
    INSERT INTO payment(idPayment, payment)
    VALUES (0, "Наличный"), (1,"Безналичный"), (2, "Сотрудники")"""
insert["carColor"]="""\
    INSERT INTO color(color)
    VALUES (:info) """
insert["carModel"]="""\
    INSERT INTO modelCar(model) VALUES (:info) """
insert["detailType"]="""\
    INSERT INTO typeDetail(type) VALUES (:info) """
insert["detailMade"]="""\
    INSERT INTO made(made) VALUES (:info) """
insert["classRepair"]="""\
    INSERT INTO classRepair(class) VALUES(:info) """
insert["typeRepair"]="""\
    INSERT INTO typeRepair(type, idClass) VALUES(:info, :idClass) """
insert["post"]="""\
    INSERT INTO post(post, idAccess) VALUES (:info, :idAccess) """
insert["catalog"]="""\
    INSERT INTO catalog(name, idType, idMade, about) VALUES (:name, :idType, :idMade, :about) """
insert["access"]="""\
    INSERT INTO access(nameAccess)
    VALUES (:info)"""
insert["timeWork"]="""\
    INSERT INTO timeWork(idWorker, idPost, dateIn)
    VALUES (:idWorker, :idPost, :dateIn)"""
insert["detail"]="""\
    INSERT INTO detailBase(code, price, date, idPayment, idStatus)
    VALUES (:code, :price, :date, :idPayment, 0)"""
insert["worker"]="""\
    INSERT INTO worker (name1, name2, name3, passport, addressRes, addressReg, phoneMob, phoneHome, eMail, info)
    VALUES (:name1, :name2, :name3, :passport, :addressRes, :addressReg, :phoneMob, :phoneHome, :eMail, :info)
"""
insert["detailHis"]="""\
    INSERT INTO detailHis (idDetail, idRepair)
    VALUES (:idDetail, :idRepair )
"""
insert["repair"]="""\
    INSERT INTO repairCar (idCar, idType, idWorker, date, price, kmage)
    VALUES (:idCar, :idType, :idWorker, :date, :price, :kmage)
"""

update={}
update["carInfo"]="""\
    UPDATE car
    SET carName=:carName, idModel=:idModel, idColor=:idColor, number=:number, radio=:radio, info=:info
    WHERE idCar=:idCar """
update["driverCar"]="""\
    UPDATE driverCar
    SET dateOut=:dateOut
    WHERE idCar=:idCar AND idWorker=:idWorker AND dateOut is Null """
update["access"]="""\
UPDATE access
SET carRead=:access1, carWrite=:access2,
    repairRead=:access3, repairWrite=:access4,
    workerRead=:access5, workerWrite=:access6,
    detailRead=:access7, detailWrite=:access8,
    systemRead=:access9, systemWrite=:access10,
    allDelete=:access11
WHERE idAccess=:idAccess"""
update["timeWork"]="""\
UPDATE timeWork
SET idWorker=:idWorker, idPost=:idPost, dateIn=:dateIn, dateOut=:dateOut
WHERE idTimeWork=:idTimeWork"""
update["password"]="""\
UPDATE worker
SET pass=:pass
WHERE idWorker=:idWorker"""
update["number"]="""\
UPDATE catalog
SET number=number+:number
WHERE code=:code"""
update["workerInfo"]="""\
UPDATE worker
SET name1=:name1, name2=:name2, name3=:name3, passport=:passport, addressRes=:addressRes,
    addressReg=:addressReg, phoneMob=:phoneMob, phoneHome=:phoneHome, eMail=:eMail, info=:info
WHERE idWorker=:idWorker
"""
update["detailInstall"]="""\
UPDATE detailBase
SET idStatus=2
WHERE idDetail=:idDetail
"""
update["driverCarInfo"]="""\
UPDATE driverCar
SET dateIn=:dateIn, dateOut=:dateOut
WHERE idDriverCar=:idDriverCar
"""
update["numberMinus"]="""\
UPDATE catalog
SET number=number-1
WHERE code=(SELECT code FROM detailBase WHERE idDetail=:idDetail)
"""
update["repair"]="""\
UPDATE repairCar
SET idCar=:idCar, idType=:idType, idWorker=idWorker, date=:date, price=:price, kmage=:kmage
WHERE idRepair=:idRepair
"""
update["detailReinstall"]="""\
UPDATE (SELECT idStatus, idRepair
        FROM detailBase
        LEFT OUTER JOIN detailHis ON detailBase.idDetail=detailHis.idDetail
        WHERE idDetail=:idDetail) as detail
SET detail.idStatus=CASE WHEN idRepair is NULL THEN 0 ELSE 1 END
"""

delete={}
delete["car"]="""\
DELETE FROM car WHERE car.idCar=:idCar """
delete["carColor"]="""\
DELETE FROM color WHERE idColor=:id """
delete["detailType"]="""\
DELETE FROM typeDetail WHERE idType=:id """
delete["carModel"]="""\
DELETE FROM modelCar WHERE idModel=:id """
delete["detailMade"]="""\
DELETE FROM made WHERE idMade=:id """
delete["catalog"]="""\
DELETE FROM catalog WHERE code=:id """
delete["classRepair"]="""\
DELETE FROM classRepair WHERE idClass=:id """
delete["typeRepair"]="""\
DELETE FROM typeRepair WHERE idType=:id"""
delete["post"]="""\
DELETE FROM post WHERE idPost=:id"""
delete["access"]="""\
DELETE FROM access WHERE idAccess=:id"""
delete["timeWork"]="""\
DELETE FROM timeWork WHERE idTimeWork=:id"""
delete["worker"]="""\
DELETE FROM worker WHERE idWorker=:id
"""
delete["driverCarInfo"]="""\
DELETE FROM driverCar WHERE idDriverCar=:idDriverCar
"""
delete["carRepair"]="""\
DELETE FROM repairCar WHERE idRepair=:idRepair
"""
delete["detailRepair"]="""\
DELETE FROM detailHis WHERE idDetail=:idDetail and idRepair=:idRepair
"""
