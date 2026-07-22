-- Data cleaning step before running analysis queries
-- Empty review_score values from the CSV loaded as 0 instead of NULL
-- during LOAD DATA INFILE, since the column type is FLOAT.
-- This was caught by comparing SQL output against the Python output
-- (Q4 total_orders count did not drop after adding a NOT NULL filter).

SET SQL_SAFE_UPDATES = 0;

UPDATE orders_master
SET review_score = NULL
WHERE review_score = 0;

SET SQL_SAFE_UPDATES = 1;

-- verify: should return 646, matching the missing review count from Python
SELECT COUNT(*) FROM orders_master WHERE review_score IS NULL;
