-- 1. Failure rate by product quality type
SELECT type,
       COUNT(*) AS records,
       ROUND(AVG(machine_failure)::numeric * 100, 1) AS failure_rate_pct
FROM sensor_readings
GROUP BY type
ORDER BY failure_rate_pct DESC;

-- 2. Failure type distribution
SELECT SUM(twf) AS twf_failure_sum,
       SUM(hdf) AS hdf_failure_sum,
       SUM(pwf) AS pwf_failure_sum,
       SUM(osf) AS osf_failure_sum,
       SUM(rnf) AS rnf_failure_sum  
FROM sensor_readings;  

-- 3. OSF rate by product quality type
SELECT type,
       ROUND(AVG(osf)::numeric * 100, 2) AS osf_rate_pct
FROM sensor_readings
GROUP BY type
ORDER BY osf_rate_pct DESC;

-- 4. Quarantine summary
SELECT quarantine_reason,
       COUNT(*) AS row_count
FROM quarantine 
GROUP BY quarantine_reason
ORDER BY row_count DESC;
 