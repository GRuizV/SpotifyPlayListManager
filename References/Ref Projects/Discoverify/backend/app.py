from flask import Flask, request, send_file
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['playlist-generator']
collection = db['songs']

@app.route('/api/discover-daily')
def discover_daily():
    # Logic to generate daily playlist
    return 'Daily playlist generated'

@app.route('/api/stripe/process-event', methods=['POST'])
def process_event():
    # Logic to process Stripe events
    return 'Stripe event processed'

@app.route('/')
def index():
    return send_file('frontend/deployedBuild/index.html')

if __name__ == '__main__':
    app.run(port=8081)


