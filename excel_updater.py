import xlwings as xw
import os


def update_reports(filename, filepath, data):
    path = os.path.join(filepath, filename)
    wb = xw.Book(path)
    ws = wb.sheets['Data']
    last_row = ws.range('A' + str(ws.cells.last_cell.row)).end('up').row
    ws.range('A' + str(last_row + 1)).options(index=False).value = data
    ws.range('{0}:{1}'.format(last_row + 1, last_row + 1)).api.Delete(xw.constants.DeleteShiftDirection.xlShiftUp)
    wb.api.RefreshAll()
    wb.save()
    wb.close()
