import xlrd


def readExcel(filepath, sheet):
    Ptm_Mutations = xlrd.open_workbook(filepath）
    sheet = Ptm_Mutations.sheet_by_name(sheet)
    rows = sheet.nrows 
    cols = sheet.ncols 

    return sheet, rows, cols


