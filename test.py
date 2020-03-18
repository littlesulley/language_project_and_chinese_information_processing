from lxml import etree


parsed = etree.parse(
    './04_Corpus/Chinese/2013_001_TUFS_CH_027.xml', etree.HTMLParser())


paragraphs = parsed.xpath('//paragraph')
# 找到所有error结点
errors = parsed.xpath('//error')
errorNum = len(errors)
texts = []

# 把每个段落里的error结点都打上标记
for paragraph in paragraphs:
    if paragraph.text:
        texts.append(paragraph.text)

    # 遍历子节点
    for sub in paragraph.iterchildren():
        texts.append('#%s#' % sub.get('id', ''))
         # tail是当前结点到下个邻居结点之间的文本内容，如果没有文本则返回None
        if sub.tail:
            texts.append(sub.tail)
    texts.append('\n')

texts = ''.join(texts).strip()

# 把每个error标记替换
for i in range(1, errorNum+1):
    errorTag = '#'+str(i)+'#'
    _type = errors[i-1].attrib['type']
    if _type == 'delete':
        revised = '[DELETED]'
    else:
        revised = errors[i-1].attrib['revised']
    texts = texts.replace(errorTag, '<font color="red">'+revised+'</font>')

print(texts)