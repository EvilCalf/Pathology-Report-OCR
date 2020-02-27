import json
import os

import pandas as pd
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import \
    TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import models, ocr_client

import image2base64

try:
    cred = credential.Credential("xxxxx",
                                 "xxxxx")
    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-shanghai", clientProfile)

    req = models.GeneralFastOCRRequest()
    for root, dicts, files in os.walk("sckxcout/"):
        for file in files:
            imageurl = root + file
            params = image2base64.image_to_base64(root + file)
            req.from_json_string(params)

            resp = client.GeneralFastOCR(req)
            data = json.loads(resp.to_json_string())
            cnt = ''
            for v in data['TextDetections']:
                cnt = cnt + v['DetectedText']
            if (cnt.find('表现') != -1):
                cntPerform = cnt[cnt.find('表现') + 3:cnt.find('结果') - 2].strip()
                cntResult = cnt[cnt.find('结果') + 3:cnt.find('报告')].strip()
                if cntPerform.find('送达部位')!=-1:
                    list_cntPerform=list(cntPerform)
                    list_cntPerform.insert(cntPerform.find('送达部位'),'。')
                    list_cntPerform.insert(cntPerform.find('食管')+1,'。')
                    cntPerform=''.join(list_cntPerform)
                data = pd.DataFrame({
                    "影像表现：": [cntPerform],
                    "诊断结果": [cntResult],
                    "检查所见": ['None'],
                    "镜检诊断": ['None'],
                    "病理诊断": ['None'],
                    "镜检所见": ['None'],
                    "检查提示": ['None'],
                    "目录": [root + "/" + file]
                })
            if (cnt.find('检查所见') != -1):
                cntCheck = cnt[cnt.find('检查所见') + 5:cnt.find('活检')].strip()
                cntDiagnose1 = cnt[cnt.find('镜检诊断') + 5:cnt.find('建议')].strip()
                if cntCheck.find('送达部位')!=-1:
                    list_cntCheck=list(cntCheck)
                    list_cntCheck.insert(cntCheck.find('送达部位'),'。')
                    list_cntCheck.insert(cntCheck.find('食管')+1,'。')
                    cntCheck=''.join(list_cntCheck)
                data = pd.DataFrame({
                    "影像表现：": ['None'],
                    "诊断结果": ['None'],
                    "检查所见": [cntCheck],
                    "镜检诊断": [cntDiagnose1],
                    "病理诊断": ['None'],
                    "镜检所见": ['None'],
                    "检查提示": ['None'],
                    "目录": [root + "/" + file]
                })
            if (cnt.find('病理诊断') != -1):
                cntDiagnose2 = cnt[cnt.find('病理诊断') + 5:cnt.find('报告')].strip()
                data = pd.DataFrame({
                    "影像表现：": ['None'],
                    "诊断结果": ['None'],
                    "检查所见": ['None'],
                    "镜检诊断": ['None'],
                    "病理诊断": [cntDiagnose2],
                    "镜检所见": ['None'],
                    "检查提示": ['None'],
                    "目录": [root + "/" + file]
                })
            if (cnt.find('镜检所见') != -1):
                cntCheck2 = cnt[cnt.find('镜检所见') + 5:cnt.find('检查提示')].strip()
                cntNote = cnt[cnt.find('检查提示') + 5:cnt.find('报告')].strip()
                data = pd.DataFrame({
                    "影像表现：": ['None'],
                    "诊断结果": ['None'],
                    "检查所见": ['None'],
                    "镜检诊断": ['None'],
                    "病理诊断": ['None'],
                    "镜检所见": [cntCheck2],
                    "检查提示": [cntNote],
                    "目录": [root + "/" + file]
                })
            data.to_csv("name2file.csv", mode="a", header=0, index=0)
except TencentCloudSDKException as err:
    print(err)
