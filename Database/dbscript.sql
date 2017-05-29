CREATE TABLE Point (
  idPoint INTEGER  NOT NULL   IDENTITY ,
  PointName VARCHAR(255)    ,
  latitude FLOAT    ,
  longitude FLOAT      ,
PRIMARY KEY(idPoint));
GO




-- ------------------------------------------------------------
-- number of times the user usuallycommutes on public transport in a  given week
-- ------------------------------------------------------------

CREATE TABLE portalUser (
  idportalUser INTEGER  NOT NULL   IDENTITY ,
  Name VARCHAR(255)  NOT NULL  ,
  Age INT  NOT NULL  ,
  Gender INT  NOT NULL  ,
  ResidentiaAddress VARCHAR(255)    ,
  WorkAddress VARCHAR(255)    ,
  emailID VARCHAR(255)  NOT NULL  ,
  PTusagePerWeek INTEGER    ,
  ownVehicle BIT      ,
PRIMARY KEY(idportalUser));
GO




CREATE TABLE Bus (
  idBus INT  NOT NULL   IDENTITY ,
  source VARCHAR(45)    ,
  destination VARCHAR(45)    ,
  bus_type VARCHAR(45)      ,
PRIMARY KEY(idBus));
GO




CREATE TABLE usersearch (
  idusersearch INTEGER  NOT NULL   IDENTITY ,
  portalUser_idportalUser INTEGER  NOT NULL  ,
  source VARCHAR(255)  NOT NULL  ,
  destination VARCHAR(255)  NOT NULL    ,
PRIMARY KEY(idusersearch)  ,
  FOREIGN KEY(portalUser_idportalUser)
    REFERENCES portalUser(idportalUser));
GO


CREATE INDEX usersearch_FKIndex1 ON usersearch (portalUser_idportalUser);
GO


CREATE INDEX IFK_canperform ON usersearch (portalUser_idportalUser);
GO


CREATE TABLE feedback (
  idfeedback INTEGER  NOT NULL   IDENTITY ,
  usersearch_idusersearch INTEGER  NOT NULL  ,
  timeStart DATETIME    ,
  timeEnd DATETIME    ,
  Rating INTEGER      ,
PRIMARY KEY(idfeedback, usersearch_idusersearch)  ,
  FOREIGN KEY(usersearch_idusersearch)
    REFERENCES usersearch(idusersearch));
GO


CREATE INDEX feedback_FKIndex1 ON feedback (usersearch_idusersearch);
GO


CREATE INDEX IFK_canprovide ON feedback (usersearch_idusersearch);
GO


CREATE TABLE usersearch_has_Bus (
  usersearch_idusersearch INTEGER  NOT NULL  ,
  Bus_idBus INT  NOT NULL    ,
PRIMARY KEY(usersearch_idusersearch, Bus_idBus)    ,
  FOREIGN KEY(usersearch_idusersearch)
    REFERENCES usersearch(idusersearch),
  FOREIGN KEY(Bus_idBus)
    REFERENCES Bus(idBus));
GO


CREATE INDEX usersearch_has_Bus_FKIndex1 ON usersearch_has_Bus (usersearch_idusersearch);
GO
CREATE INDEX usersearch_has_Bus_FKIndex2 ON usersearch_has_Bus (Bus_idBus);
GO


CREATE INDEX IFK_has ON usersearch_has_Bus (usersearch_idusersearch);
GO
CREATE INDEX IFK_has1 ON usersearch_has_Bus (Bus_idBus);
GO


CREATE TABLE Bus_has_Point (
  bhpID INTEGER  NOT NULL   IDENTITY ,
  Point_idPoint INTEGER  NOT NULL  ,
  Bus_idBus INT  NOT NULL  ,
  PointNumber INTEGER  NOT NULL    ,
PRIMARY KEY(bhpID)    ,
  FOREIGN KEY(Bus_idBus)
    REFERENCES Bus(idBus),
  FOREIGN KEY(Point_idPoint)
    REFERENCES Point(idPoint));
GO


CREATE INDEX Bus_has_Point_FKIndex1 ON Bus_has_Point (Bus_idBus);
GO
CREATE INDEX Bus_has_Point_FKIndex2 ON Bus_has_Point (Point_idPoint);
GO


CREATE INDEX IFK_Rel_07 ON Bus_has_Point (Bus_idBus);
GO
CREATE INDEX IFK_Rel_08 ON Bus_has_Point (Point_idPoint);
GO



