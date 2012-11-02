-- *******************************************************************
--  ospc: Script for creating Hosts table
--   Usage:
--       $ sqlite3 ospc < hosts.sql
--
-- *******************************************************************
-- *******************************************************************
DROP TABLE IF EXISTS hosts;
CREATE TABLE hosts (id              INTEGER PRIMARY KEY,
		   hostname        VARCHAR(20),
                   static_ip       VARCHAR(20),
                   dynamic_ip      VARCHAR(20),
		   disk_size       INTEGER,
                   role            VARCHAR(15),
                   timestamp       DATE);
