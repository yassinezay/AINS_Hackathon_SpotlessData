from flask import Flask, request, render_template, redirect, url_for, send_file
import pandas as pd
from AutoClean import AutoClean
import os
import sweetviz as sv

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        file_path = os.path.join( file.filename)
        file.save(file_path)

        dataset = pd.read_csv(file_path)
        pipeline = AutoClean(dataset, mode='auto', duplicates=True, missing_num=True, missing_categ=True, 
                             encode_categ=['onehot', [0, 1]], extract_datetime=True, outliers=True, 
                             outlier_param=1.5, logfile=True, verbose=False)

        output_path = os.path.join('cleaned_' + file.filename)
        logfile_path = os.path.join('autoclean.log')

        pipeline.output.to_csv(output_path, index=False)

        return render_template('download.html', cleaned_file=output_path, logfile=logfile_path, original_file=file_path)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(filename)
    return send_file(file_path, as_attachment=True)

@app.route('/report/<filename>')
def report(filename):
    file_path = os.path.join(filename)
    dataset = pd.read_csv(file_path)
    
    # Generate the sweetviz report
    report = sv.analyze(dataset)
    report_path = os.path.join('report.html')
    report.show_html(filepath=report_path, open_browser=False)
    
    return render_template('viz.html', report_path="viz.html")

if __name__ == "__main__":
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    app.run(debug=True)
