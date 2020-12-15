from flask import Flask, render_template,request,jsonify,session,redirect,url_for
import os
import pandas as pd
import numpy as np
from flask import send_from_directory,abort
import xlrd
import flask_excel

app=Flask(__name__)
flask_excel.init_excel(app)

app.config['file_path1']='C:/Users/Sushil Varande/Desktop/Elucidata_Assignment/static/upload_file/Task-1'
app.config['file_path2']='C:/Users/Sushil Varande/Desktop/Elucidata_Assignment/static/upload_file/Task-2'
app.config['file_path3']='C:/Users/Sushil Varande/Desktop/Elucidata_Assignment/static/upload_file/Task-3'

app.config['allowed_file']=['xlsx','csv']

def fileAllowed(filename):

    if not '.' in filename:
        return False

    ext=filename.split('.')[1]
    print(ext)

    if ext in app.config['allowed_file']:
        return True
    else:
        return False

@app.route('/' ,methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route('/upload',methods=['GET','POST'])
def uploadfile():
    if request.method=='POST':
        if request.files:
            file=request.files['file']
            if file.filename == "":
                return "please select file"

            if not fileAllowed(file.filename):
                return "please select .xlsx or .csv file"

            
            option=request.form.get('select-task')
            # pd.read_excel is not working here so I used this
            data=request.get_array(field_name='file')

            df=pd.DataFrame(data,index=None,columns=None)
            new_header = df.iloc[0] 
            df = df[1:] 
            df.columns = new_header 

            if option=="1":
                #task-1
                df1= df[df["Accepted Compound ID"].str.upper().str.endswith("PC", na = False)]
                df2= df[df["Accepted Compound ID"].str.upper().str.endswith("LPC", na = False)]
                df3= df[df["Accepted Compound ID"].str.lower().str.endswith("plasmalogen", na = False)]
                 
                df_concat = pd.concat([df1,df2,df3], axis=0)
                df_concat.to_excel(os.path.join(app.config['file_path1'],"upload-file-result1.xlsx"))
                print("file saved")
                return render_template('result.html',filename="upload-file-result1.xlsx")



            
            if option=="2":
                #task-2
                df1=df
                df1['Retention time Roundoff(min)']=df['Retention time (min)'].apply(round)
                df1.to_excel(os.path.join(app.config['file_path2'],"upload-file-result2.xlsx"))
                print("file saved")
                return render_template('result.html',filename="upload-file-result2.xlsx")

            
            if option=="3":
                  #task-3    
                  df1=df
                  df1['Retention time Roundoff(min)']=df['Retention time (min)'].apply(round)
                  df1= df.infer_objects()
                  new_df=df1.groupby("Retention time Roundoff(min)").mean()
                  new_df.drop(["Retention time (min)"], axis = 1, inplace = True) 
                  new_df["Retention time Roundoff(min)"]=df["Retention time Roundoff(min)"]
                  new_df.to_excel(os.path.join(app.config['file_path3'],"upload-file-result3.xlsx"))
                  print("file saved")
                  return render_template('result.html',filename="upload-file-result3.xlsx")

            

@app.route('/download/<filename>')
def download(filename):
    if filename=="upload-file-result1.xlsx":
        try: 
            return send_from_directory(app.config['file_path1'],filename=filename,as_attachment=True)
        except FileNotFoundError:
            return abort(404)
    if filename=="upload-file-result2.xlsx":
        try: 
            return send_from_directory(app.config['file_path2'],filename=filename,as_attachment=True)
        except FileNotFoundError:
            return abort(404)
    if filename=="upload-file-result3.xlsx":
        try: 
            return send_from_directory(app.config['file_path3'],filename=filename,as_attachment=True)
        except FileNotFoundError:
            return abort(404)


if __name__ == '__main__':
    app.run(debug=True)