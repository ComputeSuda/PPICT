import xlwt


def writeExcel(row, sheet, *items):
    Ptm_mutation = xlwt.Workbook()
    sheet = Ptm_mutation.add_sheet(sheet)
    items = list(items[0])
    # print(type(items))
    print(items)
    for i in range(len(items)):
        sheet.write(row, i, str(items[i]))
    return Ptm_mutation