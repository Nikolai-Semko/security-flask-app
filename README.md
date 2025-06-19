# CST8919 Lab 2: Web App with Threat Detection using Azure Monitor and KQL

## 🎯 Lab Objective

Create a web application with a security monitoring system capable of detecting suspicious activity (e.g., brute-force attacks) and automatically sending notifications.

## 📋 Project Description

This project demonstrates creating a threat detection system for a web application using:

- **Python Flask** - for creating the web application
- **Azure App Service** - for application deployment
- **Azure Monitor & Log Analytics** - for log collection and analysis
- **KQL (Kusto Query Language)** - for security log analysis
- **Azure Alerts** - for automatic notifications about suspicious activity

## 🏗️ Solution Architecture

```
Flask App (Azure App Service)
    ↓ (logs)
Log Analytics Workspace
    ↓ (KQL queries)
Azure Monitor Alerts
    ↓ (notifications)
Email/Action Groups
```

## 🚀 Quick Start

### 1. Local Deployment
```bash
# Clone the repository
git clone <your-repo-url>
cd <your-repo-name>

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

### 2. Testing
- Application will be available at: http://localhost:8000
- Use `test-app.http` file with REST Client in VS Code
- Replace `{{base_url}}` with `http://localhost:8000`

## 🔐 Security Endpoints

### GET /
Home page with API information

### GET /health
Application health check

### POST /login
User authentication with logging of all attempts

**Test users:**
- admin:password123
- user1:mypassword  
- testuser:testpass

**Request example:**
```json
{
    "username": "admin",
    "password": "password123"
}
```

## 📊 KQL Queries for Log Analysis

### Main query for brute-force attack detection:
```kql
AppServiceConsoleLogs
| where ResultDescription contains "LOGIN_FAILED"
| extend LogData = parse_json(ResultDescription)
| where isnotempty(LogData.username)
| extend Username = tostring(LogData.username),
         IPAddress = tostring(LogData.ip_address)
| summarize FailedAttempts = count() by Username, IPAddress, bin(TimeGenerated, 5m)
| where FailedAttempts > 5
| order by TimeGenerated desc, FailedAttempts desc
```

**Query explanation:**
1. `AppServiceConsoleLogs` - App Service console logs table
2. `where ResultDescription contains "LOGIN_FAILED"` - filter only failed login attempts
3. `extend LogData = parse_json(ResultDescription)` - parse JSON from log
4. `extend Username = tostring(LogData.username)` - extract username
5. `summarize FailedAttempts = count() by Username, IPAddress, bin(TimeGenerated, 5m)` - group by user, IP and 5-minute intervals
6. `where FailedAttempts > 5` - keep only cases with >5 attempts
7. `order by TimeGenerated desc` - sort by time

### Additional useful queries:

**All authentication events:**
```kql
AppServiceConsoleLogs
| where ResultDescription contains "LOGIN_"
| extend LogData = parse_json(ResultDescription)
| project TimeGenerated,
          Event = tostring(LogData.event),
          Result = tostring(LogData.result), 
          Username = tostring(LogData.username),
          IPAddress = tostring(LogData.ip_address)
| order by TimeGenerated desc
```

**Suspicious IP addresses:**
```kql
AppServiceConsoleLogs
| where ResultDescription contains "LOGIN_FAILED"
| extend LogData = parse_json(ResultDescription)
| extend IPAddress = tostring(LogData.ip_address)
| summarize FailedAttempts = count(),
            UniqueUsers = dcount(tostring(LogData.username))
          by IPAddress
| where FailedAttempts >= 3
| order by FailedAttempts desc
```

## 🚨 Setting up Alert Rules

1. **Go to Azure Monitor > Alerts > Create Alert Rule**
2. **Scope**: select your Log Analytics Workspace
3. **Condition**: 
   - Signal type: `Custom log search`
   - Search query: use KQL query for brute-force attacks
   - Alert logic:
     - Based on: `Number of results`
     - Operator: `Greater than`
     - Threshold value: `0`
     - Aggregation granularity: `5 minutes`
     - Frequency of evaluation: `1 minute`
4. **Action Group**: create group with email notifications
5. **Alert Details**:
   - Name: `Brute Force Detection`
   - Severity: `2 - Warning`

## 🎥 Demo Video

**YouTube link:** [To be added after recording]

Video demonstrates:
- Application deployed in Azure
- Log generation and viewing in Azure Monitor
- KQL query execution
- Alert configuration and triggering

## 📚 What I Learned During This Lab

### Technical Skills:
1. **Azure App Service**: Learned the process of deploying Python applications in the cloud
2. **Azure Monitor**: Understood principles of centralized log collection and analysis
3. **KQL**: Mastered powerful query language for analyzing large volumes of data
4. **Alert Systems**: Set up automatic security notifications

### Challenges and Solutions:
1. **Log Format**: Initially logs were unstructured - solved by using JSON format
2. **Log Delay**: Logs appear in Azure Monitor not instantly - accounted for this during testing
3. **Alert Configuration**: Required time to understand correct threshold values

### Real-world Improvements:
1. **Geolocation**: Add analysis of IP address geographical location
2. **Machine Learning**: Use Azure ML for anomaly detection
3. **SIEM Integration**: Connect to systems like Azure Sentinel
4. **Rate Limiting**: Add automatic blocking of suspicious IPs
5. **Contextual Analysis**: Analyze time of day, devices, behavior patterns

## 🔧 Project Files

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies
- `startup.py` - Startup file for Azure App Service
- `test-app.http` - HTTP tests for REST Client
- `.gitignore` - Git exclusions
- `README.md` - Project documentation

## 🚀 Azure Deployment

### Step-by-step deployment:

1. **Create Azure resources:**
```bash
az login
az group create --name rg-security-lab --location canadacentral
az appservice plan create --name asp-security-lab --resource-group rg-security-lab --sku B1 --is-linux
az webapp create --resource-group rg-security-lab --plan asp-security-lab --name your-unique-name --runtime "PYTHON|3.9"
```

2. **Configure application:**
```bash
az webapp config set --resource-group rg-security-lab --name your-unique-name --startup-file "startup.py"
```

3. **Deploy code:**
```bash
zip -r app.zip . -x "venv/*" ".git/*"
az webapp deployment source config-zip --resource-group rg-security-lab --name your-unique-name --src app.zip
```

4. **Create Log Analytics Workspace:**
```bash
az monitor log-analytics workspace create --resource-group rg-security-lab --workspace-name law-security-lab --location canadacentral
```

5. **Configure Diagnostic Settings:**
   - Go to Azure Portal → App Service → Monitoring → Diagnostic settings
   - Enable: `AppServiceConsoleLogs`, `AppServiceHTTPLogs`
   - Send to created Log Analytics workspace

## 🧪 Testing

1. Open application in browser: `https://your-app-name.azurewebsites.net`
2. Use `test-app.http` for API testing
3. Replace `{{base_url}}` with your application URL
4. Execute multiple failed requests to simulate brute-force attack
5. Check logs in Azure Monitor after 5-10 minutes

## 📞 Contact Information

**Author:** [Your Name]  
**Email:** [your email]  
**GitHub:** [profile link]

---

*Lab completed as part of CST8919 course*