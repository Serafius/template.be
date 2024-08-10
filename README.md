# template.be

## Setup

To run this project, follow these steps:

```bash
# Clone the repository
git clone https://github.com/Serafius/template.be
cd template.be

# Create and activate virtual environment
python -m venv venv
# On Unix or MacOS
source venv/bin/activate
# On Windows
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the application
uvicorn app.main:app --reload --port 5723
```
