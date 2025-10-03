# Path Of Exile Market Parser
Automates Path of Exile trade queries and logs results to Google Sheets

---

##  Overview
- Cycles through list of queries directly to official API
- Allows for consolidation of data & item components/products for easier profit visualization
- Backend: Python (pygsheets, requests), JSON
- Frontend: Google Sheets

## ⚙️ Setup
- Requires Python 3.10+
- Install dependencies: `pip install -r requirements.txt`
- Set environment variable: `GOOGLE_SERVICE_FILE=/path/to/service.json`
- Run a single cycle: `python main.py`

## Examples

### Datastream in Sheets
<img width="505" height="623" alt="image" src="https://github.com/user-attachments/assets/3a6ad7b6-6b8b-4617-a8fb-4ecfafa77a71" />

### More Organized Data 
<img width="652" height="503" alt="image" src="https://github.com/user-attachments/assets/d6f509d5-58e4-4035-aaeb-62d565c7f244" />

### Resulting User-Facing Application
<img width="658" height="572" alt="image" src="https://github.com/user-attachments/assets/f08a0798-8690-4033-b430-ee7880e3cc4e" />

## Future Improvements
- Migrate database to something like Postgres (stability, ease)
- Setup user-facing section as a webapp for ease/professionalism
- Better error handling and alerting
- Cleanup code formatting and style (pretty messy)
