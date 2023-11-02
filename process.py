import os
import re
import sys
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def extract_info(file_path):
    filename = os.path.basename(file_path)
    model = os.path.splitext(filename)[0]
    directory = os.path.dirname(file_path)
    subdirectories = directory.split(os.sep)
    fold = 1 if subdirectories[-1] == 'oneFold' else 5
    task = subdirectories[-3]
    return {"Task": task, "Fold": fold, "Model": model}

def log2json(task, data):
    logTDP = f'./logs/{task}/{data}'

    ## 提取所有模型的日志文件
    file_paths = []
    for dir in os.listdir(logTDP):
        dirPath = f"{logTDP}/{dir}/"
        for filename in os.listdir(dirPath):
            filePath = os.path.join(dirPath, filename)
            file_paths.append(filePath)

    ## 将日志信息转换为标准形式：dict存储
    tdResult_11 = {
        "success": True,
        "taskData": {
            "taskdataID": 11,
            "modeldata": {}
        }
    }
    for log_file in file_paths:
        with open(log_file, 'r', encoding='utf-8') as log:
            modelInfo = extract_info(log_file)
            for line in log:
                match = re.search(r'All Fold Mean auc = (.*)', line)
                if match: auc = float(match.group(1))
                match = re.search(r'All Fold Mean acc = (.*)', line)
                if match: acc = float(match.group(1))
                match = re.search(r'All Fold Mean rmse = (.*)', line)
                if match: rmse = float(match.group(1))
            if modelInfo['Model'] not in tdResult_11['taskData']['modeldata']:
                tdResult_11['taskData']['modeldata'][modelInfo['Model']] = []
            tmpInfo = {"TaskType": modelInfo['Task'], "foldID": modelInfo['Fold'], "auc": auc, "acc": acc, "rmse": rmse}
            tdResult_11['taskData']['modeldata'][modelInfo['Model']].append(tmpInfo)
    
    ## 将dict转换为json文件
    with open('./results/tdResult_11.json', 'w') as f:
        json.dump(tdResult_11, f)


if __name__  == "__main__":
    log2json("CognitiveDiagnosis", "FrcSub")


