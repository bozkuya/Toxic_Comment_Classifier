SELECT 
  CASE 
    WHEN label = 1 THEN 'toxic'
    WHEN label = 0 THEN 'not toxic'
    ELSE 'unknown'
  END AS result,
  *
FROM comments

