import os
import re
import sys
import json
from decimal import Decimal
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def log2json():
    log_dir = f'./logs'

    # 提取所有模型的日志文件
    logInfos_path, cfgInfos_path = [], []
    for dir in os.listdir(log_dir):
        if dir == "README.md": continue
        dir_path = f"{log_dir}/{dir}/"
        logInfos_path.append(os.path.join(dir_path, f"{dir}.log"))
        cfgInfos_path.append(os.path.join(dir_path, f"cfg.json"))

    # 对提取的日志文件进行降序操作
    sortedPath_ = sorted(zip(logInfos_path, cfgInfos_path),
                         key=lambda x: datetime.strptime(x[0].split('/')[-2], '%Y-%m-%d-%H%M%S'), reverse=True)
    logInfos_path, cfgInfos_path = zip(*sortedPath_)

    result = {}  # 存放不同的json文件, 其中key为分类名, value中是该分类对应的结果
    taskInfo = {
        'CDModels': ['NCDM', 'MIRT', 'NCDM', 'KSCD', 'KSCD', 'KaNCD', 'KaNCD', 'IRT', 'NCDM', 'MGCD', 'KSCD', 'IRT',
                     'KaNCD', 'DINA', 'DINA', 'CDGK_MULTI', 'CDGK_MULTI', 'CDMFKC', 'CDMFKC', 'DINA', 'CDMFKC',
                     'CDGK_MULTI', 'NCDM', 'MIRT', 'KSCD', 'KaNCD', 'DINA', 'CDMFKC', 'CDGK_MULTI'],
        'KTModels': ['SKVMN', 'SimpleKT', 'SAKT', 'SAINT_plus', 'SAINT', 'RKT', 'QIKT', 'LPKT_S', 'LPKT', 'KQN', 'IEKT',
                     'HawkesKT', 'DKTDSC', 'DKT_plus', 'DKT']
    }
    datasetInfo = {'FrcSub': 1, 'ASSIST_0910': 2}
    applicationInfo = {
        # 有待确认
        'GeneralModels': ['SKVMN', 'SimpleKT', 'SAKT', 'SAINT_plus', 'SAINT', 'RKT', 'QIKT', 'LPKT_S', 'LPKT', 'KQN',
                          'IEKT', 'HawkesKT', 'NCDM', 'MIRT', 'NCDM', 'KSCD', 'KSCD', 'KaNCD', 'KaNCD', 'IRT', 'NCDM',
                          'MGCD', 'KSCD', 'IRT', 'KaNCD', 'DINA', 'DINA', 'CDGK_MULTI', 'CDGK_MULTI', 'CDMFKC',
                          'CDMFKC', 'DKTDSC', 'DKT_plus', 'DKT', 'DINA', 'CDMFKC', 'CDGK_MULTI', 'NCDM', 'MIRT', 'KSCD',
                          'KaNCD', 'DINA', 'CDMFKC', 'CDGK_MULTI']
    }
    # 从日志和配置信息中获取"数据集和模型"信息:
    for logdir, cfgdir in zip(logInfos_path, cfgInfos_path):
        dataset, model, fold = None, None, None
        taskID, datasetID, applicationID = 0, 0, 0
        auc, rmse, acc = 0, 0, 0
        with open(logdir, 'r', encoding='utf-8') as log:
            for line in log:
                match = re.search(r'\[DATASET\]: (.*)', line)  # 提取数据集名称信息
                if match: dataset = match.group(1)
                match = re.search(r'All Fold Mean auc = (.*)', line)  # 获取auc信息
                if match: auc = float(
                    Decimal(float(match.group(1))).quantize(Decimal("0.0001"), rounding="ROUND_HALF_UP"))
                match = re.search(r'All Fold Mean rmse = (.*)', line)  # 获取rmse信息
                if match: rmse = float(
                    Decimal(float(match.group(1))).quantize(Decimal("0.0001"), rounding="ROUND_HALF_UP"))
                match = re.search(r'All Fold Mean acc = (.*)', line)  # 获取acc信息
                if match: acc = float(
                    Decimal(float(match.group(1))).quantize(Decimal("0.0001"), rounding="ROUND_HALF_UP"))
        with open(cfgdir, 'r', encoding='utf-8') as cfg:
            data = json.loads(cfg.read())
            model = data['modeltpl_cfg']['cls']  # 获取模型名称信息
            fold = data['datatpl_cfg']['n_folds']  # 获取多折信息
        # 获取日志信息对应的任务、数据集和场景分类
        taskID = 1 if model in taskInfo['CDModels'] else 2
        taskName = "CognitiveDiagnosis" if taskID == 1 else "KnowledgeTrace"
        datasetID = datasetInfo[dataset]
        applicationID = 1 if model in applicationInfo['GeneralModels'] else 2
        applicationName = "General" if applicationID == 1 else "KnowledgeMissing"
        # 提取该日志中的指标信息和日志信息
        logurl = f"https://github.com/Chuckie-XC1028/EduStudioData/blob/main/{logdir.lstrip('./')}"
        # 将数据存放对应的json文件
        resultStore = f"result_{taskID * 100 + datasetID * 10 + applicationID}"  # 获取结果存放信息
        ## 创建对应的存储json文件以及基础配置信息
        if resultStore in result:
            # curid = result[resultStore]["num"]
            modelExistCheck = False
            for data_dict in result[resultStore]['data']:
                if model in data_dict.values(): modelExistCheck = True
            if not modelExistCheck:  # 说明此时json文件中未增加该model
                curid = result[resultStore]["num"]
                result[resultStore]["num"] = curid + 1  # 模型数量+1
                tmp_dict = {"id": curid + 1, "model": model, "auc-1": 0, "rmse-1": 0, "acc-1": 0, "auc-5": 0,
                            "rmse-5": 0, "acc-5": 0, "logurl-1": "", "logurl-5": ""}
                result[resultStore]["data"].append(tmp_dict)
        else:
            result[resultStore] = {
                "success": True,
                "task": taskName,
                "dataset": dataset,
                "application": applicationName,
                "num": 1,
                "data": [
                    {
                        "id": 1,
                        "model": model,
                        "auc-1": 0,
                        "rmse-1": 0,
                        "acc-1": 0,
                        "auc-5": 0,
                        "rmse-5": 0,
                        "acc-5": 0,
                        "logurl-1": "",
                        "logurl-5": ""
                    }
                ]
            }
        ## 将模型的指标信息存放result中
        if fold == 1:
            for idx, data_dict in enumerate(result[resultStore]['data']):
                if model in data_dict.values():
                    result[resultStore]["data"][idx]['auc-1'] = auc
                    result[resultStore]["data"][idx]['rmse-1'] = rmse
                    result[resultStore]["data"][idx]['acc-1'] = acc
                    result[resultStore]["data"][idx]['logurl-1'] = logurl
        if fold == 5:
            for idx, data_dict in enumerate(result[resultStore]['data']):
                if model in data_dict.values():
                    result[resultStore]["data"][idx]['auc-5'] = auc
                    result[resultStore]["data"][idx]['rmse-5'] = rmse
                    result[resultStore]["data"][idx]['acc-5'] = acc
                    result[resultStore]["data"][idx]['logurl-5'] = logurl

    # 将result中不同的json进行存储
    for jskey, item in result.items():
        outdir = f"./results/{jskey}.json"
        with open(outdir, 'w') as f:
            json.dump(item, f)


if __name__ == "__main__":
    log2json()
