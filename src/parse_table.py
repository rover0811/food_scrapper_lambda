from bs4 import BeautifulSoup as bs


def find_rows(table):

    return table.find_all('tr')

def find_cells(row):

    cells = []

    ths = row.find_all('th', recursive=False)
    if ths:
        cells.extend(ths)
    tds = row.find_all('td', recursive=False)
    if tds:
        cells.extend(tds)

    return cells

def insert_colspans(twod):

    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            cell_colspan = cell.get('colspan')
            if cell_colspan and cell_colspan.isdigit() and not cell.get('col_done'):
                cell['col_done'] = True
                for x in range(1, int(cell_colspan)):
                    if rdx == 0:
                        twod[rdx].insert(cdx, cell)
                    else:
                        if len(twod[rdx]) < len(twod[rdx - 1]):
                            twod[rdx].insert(cdx, cell)

    # flip done attributes back because state is saved on following iterations
    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            if cell.get('col_done'):
                cell['col_done'] = False

    return twod

def insert_rowspans(twod):

    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            cell_rowspan = cell.get('rowspan')
            if cell_rowspan and cell_rowspan.isdigit() and not cell.get('row_done'):
                cell['row_done'] = True
                for x in range(1, int(cell_rowspan)):
                    if rdx + x < len(twod):
                        twod[rdx + x].insert(cdx, cell)

    # flip done attributes back because state is saved on following iterations
    for rdx, row in enumerate(twod):
        for cdx, cell in enumerate(row):
            if cell.get('row_done'):
                cell['row_done'] = False

    return twod

def textonly(twod):

    text2d = []

    for rdx, row in enumerate(twod):
        text2d.append([])
        for cell in row:
            text2d[rdx].append(cell.text.strip())

    return text2d


def make2d(table, text_only=True):

    twod = []

    for rdx, row in enumerate(find_rows(table)):
        twod.append([])
        for cell in find_cells(row):
            twod[rdx].append(cell)

    twod = insert_colspans(twod)
    twod = insert_rowspans(twod)

    if text_only:
        twod = textonly(twod)

    return twod
