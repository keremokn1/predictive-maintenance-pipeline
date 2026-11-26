-- 5. Hypothesis: OSF happens above type-specific strain thresholds
SELECT type,
       COUNT(*) AS osf_count,
       MIN(strain_minnm) AS min_strain
FROM sensor_readings
WHERE osf = 1   
GROUP BY type
ORDER BY min_strain; 

-- 6. Hypothesis (reverse): is every reading above the threshold an OSF?
WITH readings_with_threshold AS (
    SELECT type,
           strain_minnm,
           osf,
           CASE type
               WHEN 'L' THEN 11000
               WHEN 'M' THEN 12000
               WHEN 'H' THEN 13000
           END AS threshold
    FROM sensor_readings
)
SELECT type,
       COUNT(*) AS above_threshold,
       SUM(osf) AS osf_count 
FROM readings_with_threshold
WHERE strain_minnm > threshold
GROUP BY type
ORDER BY type;

-- 7. Risk levels: early warning before overstrain failure
WITH readings_with_threshold AS (
    SELECT type,
           strain_minnm,
           osf,
           CASE type
               WHEN 'L' THEN 11000
               WHEN 'M' THEN 12000
               WHEN 'H' THEN 13000
           END AS threshold
    FROM sensor_readings
),
risk_levels AS (
    SELECT osf,
           CASE
               WHEN strain_minnm > threshold THEN 'critical'
               WHEN strain_minnm >= threshold * 0.9 THEN 'warning'
               ELSE 'normal'
           END AS risk_level
    FROM readings_with_threshold
)
SELECT risk_level,
       COUNT(*) AS readings,
       SUM(osf) AS osf_count
FROM risk_levels
GROUP BY risk_level
ORDER BY readings;

-- 8.Identify quality types with failure rates above the overall average.
WITH type_failure_rate AS(
    SELECT type,
           ROUND(AVG(machine_failure)::numeric * 100,1) AS failure_rate_pct
    FROM sensor_readings  
    GROUP BY type      
)
SELECT type,
       failure_rate_pct 
FROM type_failure_rate
WHERE failure_rate_pct > (SELECT AVG(machine_failure) * 100 FROM sensor_readings);