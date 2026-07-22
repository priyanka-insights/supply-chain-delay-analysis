LOAD DATA LOCAL INFILE 'C:/Users/prianka/OneDrive/Desktop/supply-chain-delay-analysis/data/processed/master_table_features.csv'
INTO TABLE orders_master
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

-- verify row count matches Python output (should be 96470)
SELECT COUNT(*) FROM orders_master;
