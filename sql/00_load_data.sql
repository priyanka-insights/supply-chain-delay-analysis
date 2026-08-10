-- Prerequisite: MySQL client must allow local file loading.
-- Run this once per session if you get a "local_infile" error:
--   SET GLOBAL local_infile = 1;
--
-- Run this script from the project root directory so the relative path resolves correctly.

LOAD DATA LOCAL INFILE 'data/processed/master_table_features.csv'
INTO TABLE orders_master
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- Verify row count matches Python output (should be 96470)
SELECT COUNT(*) FROM orders_master;
