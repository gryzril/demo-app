Jenkins - http://127.0.0.1:8080


Frontend
http://localhost:5173/

Backend
http://localhost:8000/swagger


How to run locally:
    Recommended tools and installs
    - pgAdmin
    - Python 12
    - Docker Desktop
    - Vue Dev tools
    - Visual Studio Code

    Frontend
    ```
    cd /frontend
    npm run dev
    ```
    OR
    docker compose up --build frontend


    Backend

How to run tests:
    Playwright

    Backend Tests

How CI/CD pipeline is configured:
    ```docker compose -f docker-compose.jenkins.yml up -d```

Deployment Instructions: