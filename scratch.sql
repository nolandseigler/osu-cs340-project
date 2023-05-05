CREATE PROCEDURE select_all_data(p1 INT)
BEGIN
  label1: LOOP
    SET p1 = p1 + 1;
    IF p1 < 21 THEN
      SELECT * FROM (SELECT table_name FROM information_schema.tables where table_schema = 'cs340_umj' limit 1 offset p1)
      ITERATE label1;
    END IF;
    LEAVE label1;
  END LOOP label1;
  SET @x = p1;
END;

DELIMITER //
FOR i IN 1..20
DO
  SELECT * FROM (SELECT table_name FROM `information_schema`.`tables` where table_schema = 'cs340_seiglern' and table_name != 'diagnostic' limit 1 offset i);
END FOR;
//
DELIMITER ;

DELIMITER //
FOR i IN 0..20
DO
  SELECT table_name INTO @t FROM `information_schema`.`tables` where table_schema = 'cs340_seiglern' and table_name != 'diagnostic' limit 1 offset i;
  set @qry1:= concat('select * from ',@t);
  prepare stmt from @qry1;
  execute stmt;
END FOR;
//
DELIMITER ;