import base64


def image_to_base64(str):
    f = open(str, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f.read())
    ls_f=ls_f.decode()
    ls_f='{"ImageBase64":"data:image/jpeg;base64,' +ls_f+'"}'
    return ls_f

