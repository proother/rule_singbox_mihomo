import os
import shutil
import logging
import requests
import zipfile
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

current_dir = os.getcwd()

def init():
    # 删除已有文件夹
    dir_path = os.path.join(current_dir, 'rule')
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        logging.warning('{} exists, delete!', dir_path)
        shutil.rmtree(dir_path)
    os.makedirs(dir_path)
    
    logging.info('init completed, skipping ASN download')

source_repo_url = "https://github.com/blackmatrix7/ios_rule_script/archive/refs/heads/master.zip"
def download_source_repo():
    logging.info('downloading rule source file...')
    source_zip = os.path.join(current_dir, 'ios_rule_script.zip')
    response = requests.get(source_repo_url, headers=headers)
    if response.status_code == 200:
        with open(source_zip, 'wb') as file:
            file.write(response.content)
        logging.info('downloading rule source complete')
    else:
        logging.critical(f'downloading rule source error, error code {response.status_code}')
        exit(1)
    source_folder = os.path.join(current_dir, 'ios_rule_script')
    os.makedirs(source_folder, exist_ok=True)
    with zipfile.ZipFile(source_zip, 'r') as zip_ref:
        zip_ref.extractall(source_folder)
        logging.info(f"unzip asn files to {source_folder}")

class RuleSet(object):
    def __init__(self, domain, domain_keyword, domain_suffix, ip_cidr, process_name):
        self.version = 2
        self.rules = list()
        if len(domain) != 0 or len(domain_keyword) != 0 or len(domain_suffix) != 0 or len(ip_cidr) != 0:
            rule = dict()
            if len(domain) != 0:
                rule['domain'] = list(set(domain))
            if len(domain_keyword) != 0:
                rule['domain_keyword'] = list(set(domain_keyword))
            if len(domain_suffix) != 0:
                rule['domain_suffix'] = list(set(domain_suffix))
            if len(ip_cidr) != 0:
                rule['ip_cidr'] = list(set(ip_cidr))
            self.rules.append(rule)
        if len(process_name) != 0:
            rule = dict()
            rule['process_name'] = list(set(process_name))
            self.rules.append(rule)

subs = ["Assassin'sCreed", "Cloud"]
def translate_rule():
    source_folder = os.path.join(current_dir, 'ios_rule_script/ios_rule_script-master/rule/Clash')
    for entry in os.listdir(source_folder):
        if entry == 'CGB':
            continue
        source_dir = os.path.join(source_folder, entry)
        if not os.path.isdir(os.path.join(source_folder, entry)):
            continue
        if entry in subs:
            for subEntry in os.listdir(source_dir):
                sub_source_dir = os.path.join(source_dir, subEntry)
                translate_source_to_target(subEntry, sub_source_dir, None)
        else:
            translate_source_to_target(entry, source_dir, None)

    logging.info(f"finish translating clash rules")

def translate_source_to_target(entry, source_dir, target_dir):
    # 不再为每个规则创建子目录，直接使用 rule 目录
    target_dir = os.path.join(current_dir, 'rule')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    source_file = os.path.join(source_dir, f'{entry}.yaml')
    if os.path.exists(os.path.join(source_dir, f'{entry}_Classical.yaml')):
        source_file = os.path.join(source_dir, f'{entry}_Classical.yaml')
    target_file = os.path.join(target_dir, f'geosite-{entry}.json')

    domain = list()
    domain_keyword = list()
    domain_suffix = list()
    ip_cidr = list()
    process_name = list()

    found_payload = False
    with open(source_file, 'r', encoding='utf-8') as file:
        for line in file:
            if 'payload:' in line.strip():
                found_payload = True
                continue
            if not found_payload:
                continue
            splits = line.strip()[2:].split(',')
            rule_type = splits[0]
            rule_content = splits[1]
            if rule_type == 'DOMAIN':
                domain.append(rule_content)
            elif rule_type == 'DOMAIN-SUFFIX':
                domain_suffix.append(rule_content)
            elif rule_type == 'DOMAIN-KEYWORD':
                domain_keyword.append(rule_content)
            elif rule_type == 'IP-CIDR' or rule_type == 'IP-CIDR6':
                ip_cidr.append(rule_content)    
            elif rule_type == 'IP-ASN':
                # 跳过 IP-ASN 规则，因为我们没有下载 ASN 数据
                logging.debug(f'Skipping IP-ASN rule: AS{rule_content}')
                pass
            elif rule_type == 'PROCESS-NAME':
                process_name.append(rule_content)
            else:
                logging.warning(f'Unknown rule type { rule_type }')

    rule_content = RuleSet(domain, domain_keyword, domain_suffix, ip_cidr, process_name)
    with open(target_file, 'w') as json_file:
        json.dump(rule_content, json_file, default=lambda obj: obj.__dict__, sort_keys=True, indent=2)
    # 不再生成 README 文件，因为所有文件都在同一个目录

extra_surge_conf = {}
def translate_extra():
    logging.info('translating extra surge rule...')
    target_folder = os.path.join(current_dir, 'rule')
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    
    for k, v in extra_surge_conf.items():
        source_file = os.path.join(current_dir, f'{k}.conf')
        response = requests.get(v, headers=headers)
        if response.status_code == 200:
            with open(source_file, 'wb') as file:
                file.write(response.content)
            logging.info(f'downloading {k}.conf complete')
        else:
            logging.critical(f'downloading {k}.conf error, error code {response.status_code}')
            exit(1)

        domain = list()
        domain_keyword = list()
        domain_suffix = list()
        ip_cidr = list()
        process_name = list()

        with open(source_file, 'r', encoding='utf-8') as file:
            for line in file:
                if len(line.strip()) == 0:
                    continue
                if line.startswith('#'):
                    continue
                splits = line.strip().split(',')
                rule_type = splits[0]
                rule_content = splits[1]
                if rule_type == 'DOMAIN':
                    domain.append(rule_content)
                elif rule_type == 'DOMAIN-SUFFIX':
                    domain_suffix.append(rule_content)
                elif rule_type == 'DOMAIN-KEYWORD':
                    domain_keyword.append(rule_content)
                elif rule_type == 'IP-CIDR' or rule_type == 'IP-CIDR6':
                    ip_cidr.append(rule_content)    
                elif rule_type == 'IP-ASN':
                    # 跳过 IP-ASN 规则，因为我们没有下载 ASN 数据
                    logging.debug(f'Skipping IP-ASN rule: AS{rule_content}')
                    pass
                elif rule_type == 'PROCESS-NAME':
                    process_name.append(rule_content)
                elif rule_type == 'USER-AGENT':
                    pass
                else:
                    logging.warning(f'Unknown rule type { rule_type }')
        
        # 直接保存到 rule 目录
        target_file = os.path.join(target_folder, f'{k}.json')        
        rule_content = RuleSet(domain, domain_keyword, domain_suffix, ip_cidr, process_name)
        with open(target_file, 'w') as json_file:
            json.dump(rule_content, json_file, default=lambda obj: obj.__dict__, sort_keys=True, indent=2)

def post_clean():
    shutil.rmtree(os.path.join(current_dir, 'ios_rule_script'))
    os.remove(os.path.join(current_dir, 'ios_rule_script.zip'))
    for key in extra_surge_conf:
        os.remove(os.path.join(current_dir, f'{key}.conf'))

def main():
    init()
    download_source_repo()
    translate_rule()
    translate_extra()
    post_clean()

if __name__ == "__main__":
    main()
