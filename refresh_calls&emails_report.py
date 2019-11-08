import requests
import os
import re
import time
import auth
import httplib2
import pandas as pd
import excel_updater as xl_upd
from apiclient import discovery
from bs4 import BeautifulSoup as bs
from datetime import datetime, timedelta, date
from gdrive_files_manage import uploadFile_gdrive, listFiles_gdrive_folder, deleteFile_gdrive, listFiles

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'gdrive_file_manager'
authInst = auth.Auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.get_credentials()
http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

bittrix_session = requests.Session()
bittrix_session.auth = ('nikolay@idsiberian.ru', 'dancer123')
date = datetime.now().date() - timedelta(1)
#date = datetime.strptime('05.07.2019', '%d.%m.%Y')
params = (('set_filter', 'Y'),
  ('sort_id', '3'),
  ('sort_type', 'ASC'),
  ('F_DATE_TYPE', 'interval'),
  ('F_DATE_FROM', '{0}.{1}.{2}'.format(date.day, date.month, date.year)),
  ('F_DATE_TO', '{0}.{1}.{2}'.format(date.day, date.month, date.year)),
  ('F_DATE_DAYS',''),
  ('filter','%5B0%5D%5B1%5D'),
  ('save','Y'),
  ('SHOWALL_1','1'))

r = bittrix_session.get('https://sibcedar.bitrix24.ru/crm/reports/report/view/1523/', params=params)

soup = bs(r.text, features='lxml')
table = soup.findAll('table', {'class':'reports-list-table'})
report_table = str(table[0].prettify())
report_df = pd.read_html(report_table, header=None, index_col=None)[0]


# паттерн для удаления строк (фильтрации), в которых содержатся общие итоги
pattern = re.compile('Ответственный|Страницы|—')
result_df = report_df[report_df['Ответственный'].apply(lambda x: not re.match(pattern, x))][0:]
result_df['date'] = date  #date.strftime('%d.%m.%Y')

filenames = ['Рябов. Отчет Звонки + Письма.xlsx', 'Шпинев. Отчет Звонки + Письма.xlsx']
filepath = r'W:\Gutorov\02 - Отчеты\Отчеты Звонки Письма'
gdrive_folder_id = '12IyRgYoENfCBeprH_JT49DB3jkL2_ole'
query = '"'+ gdrive_folder_id + '" in parents'

for file_id in listFiles_gdrive_folder(drive_service, query):
    deleteFile_gdrive(drive_service, file_id)
    print('File %s has been deleted' % file_id)


for file in filenames:
    xl_upd.update_reports(file, filepath, result_df)
    uploadFile_gdrive(drive_service, file, os.path.join(filepath, file), 'application/vnd.ms-excel', gdrive_folder_id)
