SELECT *
FROM tasks_queue
WHERE status IN ('in_queue','processing', 'failed')
ORDER BY status,retries;

