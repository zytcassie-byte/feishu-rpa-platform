CREATE TABLE rpa_task (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task_no VARCHAR(50) UNIQUE,
    task_type VARCHAR(20),
    business_key VARCHAR(50),
    params TEXT,
    status VARCHAR(20) DEFAULT 'PENDING',
    retry_count INT DEFAULT 0,
    max_retry INT DEFAULT 3,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);