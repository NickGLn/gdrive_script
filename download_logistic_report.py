import os
import auth
import httplib2
from apiclient import discovery
from gdrive_files_manage import downloadFile

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_id.json'
APPLICATION_NAME = 'gdrive_file_manager'
authInst = auth.Auth(SCOPES, CLIENT_SECRET_FILE, APPLICATION_NAME)
credentials = authInst.get_credentials()
http = credentials.authorize(httplib2.Http())
drive_service = discovery.build('drive', 'v3', http=http)

windows_path = 'W:\Dannye_dlya_analitiki\DataComDep\Costs\Logistic'
windows_filename = '2019 Отчет логист + Аналитика.xlsx'
downloadFile(drive_service, '14ysPTG6o45qP3Gj-ciBWFIBF5JWTlrbR_myO1LEFml4', os.path.join(windows_path, windows_filename))