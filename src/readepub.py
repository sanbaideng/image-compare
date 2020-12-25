import zipfile
from lxml import etree
import ebooklib
from ebooklib import epub
from resultHandle import writeLine
import sys
import io
import chardet
book = epub.read_epub('OKR工作法.epub')
sys.stdout = io.TextIOWrapper(
    sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码

#


def readByEbooklib():
    for item in book.get_items():
        print("item.get_type():::", item.get_type())
        # print(item.get_content().decode())
        try:
            encoding = chardet.detect(item.get_content())['encoding']
            if(item.get_type() == 1):
                print(encoding)
                if(encoding == None):
                    print(encoding, 'aaaaaaaaa')
                    print(chardet.detect(item.get_content())['encoding'])
                else:
                    print(item.get_content().decode(encoding))
                # print(item.get_content())
                # print(item.get_content().decode())
                    writeLine("OKR工作法.txt",
                              item.get_content().decode(encoding))
            else:
                # print(chardet.detect(item.get_content()))
                # print(chardet.detect(item.get_content())['encoding'])
                # print(item.get_content().decode('utf-8'))
                writeLine("OKR工作法.txt", item.get_content().decode())
        except IOError:
            print("Error: 没有找到文件或读取文件失败", IOError)
        else:
            print("内容写入文件成功")


def get_epub_info(fname):
    ns = {
        'n': 'urn:oasis:names:tc:opendocument:xmlns:container',
        'pkg': 'http://www.idpf.org/2007/opf',
        'dc': 'http://purl.org/dc/elements/1.1/'
    }

    # prepare to read from the .epub file
    zip = zipfile.ZipFile(fname)

    # find the contents metafile
    txt = zip.read('META-INF/container.xml')
    tree = etree.fromstring(txt)
    cfname = tree.xpath('n:rootfiles/n:rootfile/@full-path', namespaces=ns)[0]

    # grab the metadata block from the contents metafile
    cf = zip.read(cfname)
    tree = etree.fromstring(cf)
    p = tree.xpath('/pkg:package/pkg:metadata', namespaces=ns)[0]

    # repackage the data
    res = {}
    for s in ['title', 'language', 'creator', 'date', 'identifier']:
        res[s] = p.xpath('dc:%s/text()' % (s), namespaces=ns)[0]

    return res

    # if item.get_type() == ebooklib.ITEM_DOCUMENT:
    #     print('==================================')
    #     print('NAME : ', item.get_name().encode('utf8'))
    #     # print('----------------------------------')
    #     print(item.get_content().decode())
    #     # print('==================================')
res = get_epub_info('OKR工作法.epub')
print(res)
