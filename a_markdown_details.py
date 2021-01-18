# coding:utf-8
import markdown
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
import re
import xml.etree.ElementTree as etree

import unittest

RE_FENCE_START = r'^{{3}(?P<class>#*)(?P<title>.*)'
RE_FENCE_END = r'}{3}'

class MyExtension(Extension):
    def extendMarkdown(self, md ):

        #detail&summary
        md.parser.blockprocessors.register(DetailBlock(md.parser),'box',175)


class DetailBlock(BlockProcessor):
    def test(self,parent,block):
        return re.match(RE_FENCE_START,block)

    def run(self,parent,blocks):
        original_block = blocks[0]

        pattern = re.compile(RE_FENCE_START)
        match = pattern.search(blocks[0])
        title = match.group("title")
        cls = match.group("class")
        cls_str=''
        if cls != "" :
            count = len(cls)
            cls_str=cls_str + 'h'+str(count)

        blocks[0] = re.sub(RE_FENCE_START,'',blocks[0])

        for block_num,block in enumerate(blocks):
            if re.search(RE_FENCE_END,block):
                blocks[block_num] = re.sub(RE_FENCE_END,'',block)
                e = etree.SubElement(parent,'details')

                summary = markdown.util.etree.SubElement( e , "summary")
                summary.set("class", cls_str )
                summary.text = markdown.util.AtomicString(title)

                #e.set('open','')
                #e.set('style','display: inline-block; border: 1px solid red;')
                self.parser.parseBlocks(e,blocks[0:block_num + 1])
                for i in range(0,block_num + 1):
                    blocks.pop(0)
                return True
        blocks[0] = original_block
        return False

def makeExtension(*args, **kwargs):
    return MyExtension(*args, **kwargs)

class TextClass(unittest.TestCase):
    def test_extends(self):
        import markdown
        md = markdown.Markdown(extensions=['a_markdown_details'])

       #日本語を単独で使えるようにしたい 
       #デコードする必要があるようだ
        text = '''{{{##title
hoge
hoge1
}}}'''
        print(md.convert(text))

if __name__ == "__main__":
    unittest.main()
    
