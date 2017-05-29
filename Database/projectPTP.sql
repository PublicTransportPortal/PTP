insert into Point (PointName, latitude, longitude)
select  Point1.pt , Point1.lt , Point1.ln
from Point1;



insert into Bus (source, destination, bus_type)
select bus1.d , bus1.bus, bus1.s
from bus1;


select * from Bus

select * from point
select * from bhp

insert into Bus_has_Point (Bus_idBus, Point_idPoint, PointNumber)
select Bus.idBus, Point.idPoint, bhp.number 
from bhp, Point, Bus
where LTRIM(RTRIM(Point.PointName))= bhp.point and LTRIM(RTRIM(Bus.bus_type))= LTRIM(RTRIM(bhp.bus)) order by cast(Bus.idBus as int)


select * from Bus_has_Point

/* get mainlist and buslist using this */
select Bus.bus_type, Point.PointName, Point.latitude, Point.longitude, Bus_has_Point.PointNumber
from Bus_has_Point, Point, Bus
where LTRIM(RTRIM(Point.idPoint))= Bus_has_Point.Point_idPoint and LTRIM(RTRIM(Bus.idBus))= LTRIM(RTRIM(Bus_has_Point.Bus_idBus)) order by cast(Bus.idBus as int)



/* for each bus_type,  get rows with unique point number only
*/

/*
delete from  Bus_has_Point
where Bus_has_Point.Point_idPoint not in
(
  SELECT      min(bhp.Point_idPoint) 
  FROM        Bus_has_Point as bhp
  GROUP BY    bhp.Bus_idBus, bhp.PointNumber
)
*/