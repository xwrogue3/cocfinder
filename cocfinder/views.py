from cocfinder import app

@app.route('/')
def main():
    return 'This is the main view'

@app.route('/bases/')
def bases():
    return 'This is the main view for bases'

# Need CRUD views for the bases

