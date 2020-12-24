"""
Markdown Custom class extension for Python-Markdown
=========================================

    >>> import markdown
    >>> md = markdown.Markdown(extensions=['a_markdown_simple'])
    >>> md.convert('i love!!red|spam!!')
    u'<p>i love<span class="red">spam</span></p>'

    >>> md.convert('{{summary_title}}')
    u'<p><summary>summary_title</summary></p>'


"""
from __future__ import absolute_import
from __future__ import unicode_literals
import markdown
from markdown import Extension
from markdown.inlinepatterns import Pattern
from markdown.blockprocessors import BlockProcessor
import re
import xml.etree.ElementTree as etree



#!!red|str!! >> <span class="red">spam</span>'
SPAN_CLASS = r'[!]{2}(?P<class>.+?)[|](?P<text>.+?)[!]{2}'

#{{summary}} >> <summary>summary_title</summary>
SUMMARY = r'[{]{2}(?P<title>.+?)[}]{2}'

#--div--

#detail
RE_FENCE_START = r'^{{3}\n'
RE_FENCE_END = r'}{3}'

class MyExtension(Extension):
    def extendMarkdown(self, md, md_globals):

        #span_class
        span_class=SpanClassPattern(SPAN_CLASS, md)
        md.inlinePatterns['custom_span_class'] = span_class

        #summary
        summary=SummaryPattern(SUMMARY, md)
        md.inlinePatterns['custom_summary'] = summary
    
        #detail
        md.parser.blockprocessors.register(DetailBlock(md.parser),'box',175)

class SpanClassPattern(Pattern):
    def handleMatch(self, matched):

        cls = matched.group("class")
        text = matched.group("text")

        line = markdown.util.etree.Element("span")
        line.set("class", cls)
        line.text = markdown.util.AtomicString(text)
        return line

class SummaryPattern(Pattern):
    def handleMatch(self, matched):

        text = matched.group("title")
        line = markdown.util.etree.Element("summary")
        line.text = markdown.util.AtomicString(text)
        return line

class DetailBlock(BlockProcessor):
    def test(self,parent,block):
        return re.match(RE_FENCE_START,block)

    def run(self,parent,blocks):
        original_block = blocks[0]
        blocks[0] = re.sub(RE_FENCE_START,'',blocks[0])

        for block_num,block in enumerate(blocks):
            if re.search(RE_FENCE_END,block):
                blocks[block_num] = re.sub(RE_FENCE_END,'',block)
                e = etree.SubElement(parent,'details')
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
    
