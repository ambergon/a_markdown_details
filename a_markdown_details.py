# coding:utf-8
"""
Markdown Custom class extension for Python-Markdown
=========================================

    >>> import markdown
    >>> md = markdown.Markdown(extensions=['a_markdown_details'])


    >>> md.convert('{{{##title')
    >>> md.convert('}}}')
    u'<p><summary class="h2 aaa">summary_title</summary></p>'

"""
from __future__ import absolute_import
from __future__ import unicode_literals
import markdown
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
import re
import xml.etree.ElementTree as etree

#--div--

#detail
# RE_FENCE_START = r'^[{]{3}$'
# RE_FENCE_END = r'^[}]{3}$'

RE_FENCE_START = r'^{{3}(?P<class>#*)(?P<title>.*)'
#RE_FENCE_START = r'^{{3}\n'
RE_FENCE_END = r'}{3}'



#SUMMARY = r'[{]{2}(?P<class>#*)(?P<title>.+?)[}]{2}(?P<class_option>.*)'
SUMMARY = r'[{]{2}(?P<class>#*)(?P<title>.+?)[}]{2}(?P<class_option>.*)$'

class MyExtension(Extension):
    def extendMarkdown(self, md, md_globals):

        #detail&summary
        md.parser.blockprocessors.register(DetailBlock(md.parser),'box',175)

class SummaryPattern(Pattern):
    def handleMatch(self, matched):

        title = matched.group("title")
        cls = matched.group("class")
        cls_option = matched.group("class_option")

        cls_str=''
        if cls != "" :
            count = len(cls)
            cls_str=cls_str + 'h'+str(count)

        if cls_option != '':
            cls_str=cls_str + self.check_str(cls_str) + cls_option

        # line = markdown.util.etree.Element("p")
        # summary = markdown.util.etree.SubElement(line , "summary")
        # summary.set("class", cls_str )
        # summary.text = markdown.util.AtomicString(title)

        return line
    def check_str(self , text ):
        if text == '':
            return ''
        else :
            return ' '


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

if __name__ == "__main__":
    import doctest
    doctest.testmod(
            #verbose=True
            )
    
