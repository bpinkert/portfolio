import os
import codecs
import argparse
import xlsxwriter


def format_raw(filename, outfile):

    f = codecs.open(filename, encoding='ANSI')

    text = f.read()

    string = text.encode('utf-8')

    lines = string.split('\r\n\r\n\r\n\r\n')

    d = dict()

    for line in lines:
        line = line.split('\r\n\r\n\r\n')
        key = line[0]
        if len(line) == 2:
            value = str(line[1])
            value = value.lstrip('AccessToString : ')
            values = value.split('\r\n')
            val_list = list()
            for v in values:
                v = v.lstrip('                 ')
                val_list.append(v)
            d[key] = val_list

    workbook = xlsxwriter.Workbook(outfile)
    worksheet = workbook.add_worksheet()
    row = 0
    col = 0
    order = sorted(d.keys())
    cell_format = workbook.add_format({'bold': True})
    cell_format.set_bg_color('#366092')
    cell_format.set_font_color('white')
    worksheet.write(0, 0, 'Folder', cell_format)
    pwidth = len('Permissions')
    worksheet.set_column(0, 1, pwidth)
    worksheet.write(0, 1, '', cell_format)
    worksheet.write(0, 2, '', cell_format)
    worksheet.write(0, 3, '', cell_format)
    worksheet.write(0, 4, '', cell_format)
    worksheet.write(0, 5, '', cell_format)
    worksheet.write(0, 6, '', cell_format)
    worksheet.write(0, 7, '', cell_format)
    worksheet.write(0, 8, '', cell_format)
    worksheet.write(0, 9, '', cell_format)
    worksheet.write(0, 10, '', cell_format)
    worksheet.write(0, 11, '', cell_format)
    worksheet.write(0, 12, '', cell_format)
    worksheet.write(0, 13, '', cell_format)
    worksheet.write(0, 14, '', cell_format)
    worksheet.write(0, 15, '', cell_format)
    worksheet.write(0, 16, '', cell_format)
    worksheet.write(0, 17, '', cell_format)
    worksheet.write(0, 18, '', cell_format)
    worksheet.write(0, 19, '', cell_format)
    worksheet.write(0, 20, '', cell_format)
    worksheet.merge_range('B1:U1', 'Permissions', cell_format)

    width = 10
    item_width = 10

    for key in order:
        key_width = len(key)
        if key_width > width:
            width = key_width
        for item in d[key]:
            iwidth = len(item)
            if iwidth > item_width:
                item_width = iwidth

    for key in order:
        row += 1
        worksheet.set_column(row, col, width)
        worksheet.write(row, col,    key, cell_format)
        i = 1
        for item in d[key]:
            worksheet.set_column(row, col + i, item_width)
            worksheet.write(row, col + i, item)
            i += 1

    workbook.close()


def main():

    parser = argparse.ArgumentParser(add_help = True, prog='python script to format NT security raw text file',
                                     description = "python script to format NT security raw text file",
                                     usage='Use like so: python format_permissions_raw.py '
                                           '--file raw.txt --output report.xlsx')

    parser.add_argument('--file', action='store', dest='fname', help='raw.txt')
    parser.add_argument('--output', action='store', dest='output', help='output.xlsx')
    # parser.add_argument('-debug', action='store', dest='debug', help='Turn DEBUG output ON')

    options = parser.parse_args()

    filename = options.fname
    outfile = options.output

    if outfile is None:
        outfile = "data.xlsx"
    if os.path.exists(os.path.abspath(outfile)):
        print parser.print_usage()
        print "File already exists, choose a different file name"
    if filename is None:
        print parser.print_usage()
        print "File name is blank. use --file file.txt or absolute path"
    else:
        try:
            format_raw(filename, outfile)
        except Exception as e:
            print parser.print_usage()
            print "File does not exist, make sure you have the path correct"
            print "Exception: %s" % e

if __name__ == '__main__':
    main()
