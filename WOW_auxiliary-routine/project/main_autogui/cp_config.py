# 用于数据存储，对于文件config.ini

import configparser

def set_default_parser():
    config = configparser.ConfigParser()
    config['communication'] = {
        'VX_KEY' : 'NULL'
    }
    with open('cp_config.ini','w') as cf:
        config.write(cf)


def read_VX_KEY_parser():
    config = configparser.ConfigParser()
    config.read('cp_config.ini')
    # 获取所以片段，或过滤掉DEFAULT
    # config.sections()
    vx_key = config.get('communication','VX_KEY')
    print(vx_key)
    return vx_key


def write_VX_KEY_parser(key):
    config = configparser.ConfigParser()
    config['communication'] = {
        'VX_KEY' : key
    }   
    with open('cp_config.ini','w') as cf:
        config.write(cf)    


# set_default_parser()
# read_VX_KEY_parser()
# write_VX_KEY_parser("sadhfeawiniaff")
# read_VX_KEY_parser()
