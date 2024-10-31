SELECT q.ID, q.task_type, q.payload, q.status, q.statuslog, q.retries, q.priority, q.created_at, q.updated_at, q.processed_at
FROM dbo.tasks_queue AS q LEFT OUTER JOIN
     dbo.task_type AS tt ON q.task_type = tt.task_type
WHERE status IN ('in_queue', 'failed') 
      AND DATEDIFF(MINUTE, updated_at, GETDATE()) > (tt.retryinterval*(2^q.retries))-1 And q.retries<tt.maxretries
ORDER BY q.priority, q.ID