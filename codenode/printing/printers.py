######################################################################### 
# Copyright (C) 2007, 2008, 2009 
# Alex Clemesha <alex@clemesha.org> & Dorian Raymer <deldotdr@gmail.com>
# 
# This module is part of codenode, and is distributed under the terms 
# of the BSD License:  http://www.opensource.org/licenses/bsd-license.php
#########################################################################

import os
import re

from twisted.internet import protocol, defer

from codenode.backend.kernel import process



class Base(object):
    """This needs to accept a notebook database session, extract the cells
    and store them in a standard way for the different printers to use.

    """

    def __init__(self, notebook_db, env_path):
        notebook_db = notebook_db
        self.env_path = env_path
        nbdata = notebook_db.get_notebook_data()
        self.nbid = str(nbdata['nbid'])
        self.title = str(nbdata['title'])
        self.orderlist = nbdata['orderlist'].split(',')
        self.cells = nbdata['cells']

    def save_file(self, format_ext, data):
        files_dir_path = os.path.join(self.env_path, 'prints')
        file_name = self.nbid + format_ext
        file_path = os.path.join(files_dir_path, file_name)
        f = file(file_path, 'w')
        f.write(data)
        f.close()
        return file_name

class ExtPrinterProtocol(protocol.ProcessProtocol):

    def processEnded(self, status_object):
        """try to get file...
        """
        self.control.done()

class PdfPrinter(process.BaseProcessControl):

    processProtocol = ExtPrinterProtocol
    executable = 'pdflatex'

    def __init__(self, deferred):
        self.deferred = deferred

    def go(self):
        self.start()

    def done(self):
        self.deferred.callback('done')

    def buildProcess(self, tex_file_name, env_path):
        self.protocol = self.buildProtocol()
        self.args = (self.executable, tex_file_name)
        self.env = {'PATH':os.getenv('PATH')}
        self.path = os.path.join(env_path, 'prints')



class Latex(Base):
    def escape_latex(self, text):
        """escape any occurrance of a special latex character:
        #, $, %, ^, &, _, {, }, ~, '\'
        \#, \$, \%, \^{}, \&, \_, \{, \}, \~{}
        """
        escape_a = re.compile('(#|\$|%|&|_|\}|\{)')
        escape_b = re.compile('(\^|`)')
        output_image = re.compile('[a-zA-Z0-9/:]*/images/(\w+/\w+.png)\\n?')
        text = escape_a.sub(r'\\\1', text)
        text = escape_b.sub(r'\\\1{}', text)
        image_match = output_image.match(text)
        if image_match is not None:
            text = image_match.groups()[0]
        return text

    def _make_print(self):
        texfile = r"""
\documentclass{report}
\usepackage{codenode_notebook}
\graphicspath{{%s}}
\begin{document}
        """ % (self.env_path) 
        def format_cell(style, content):
            content = self.escape_latex(content)
            a = "\\%scell{%s}\n"%(style, content)
            return a
        for cell in self.orderlist:
            data = self.cells[cell]
            content = data['content']
            style = data['cellstyle']
            texfile += format_cell(style, content)
        texfile += r"\end{document}"
        self.tex = texfile
        file_name = self.save_file('.tex', texfile)
        return file_name

    def make_print(self):
        self._make_print()

class PDF(Latex):
    def make_print(self):
        """Make a Latex, then run pdflatex
        """
        file_name = self._make_print()
        d = defer.Deferred()
        eprinter = PdfPrinter(d)
        eprinter.buildProcess(file_name, self.env_path)
        eprinter.go()
        d.addCallback(self._get_pdf_file)
        return d

    def _get_pdf_file(self, res):
        file_path = os.path.join(self.env_path, 'prints', self.nbid + '.pdf')
        f = file(file_path, 'rb')
        data = f.read()
        f.close()
        return data


class ReST(Base):
    """
    Generate reST format of notebook from databade.

    .. role:: input
    .. role:: outputtext
    .. role:: outputimage

    Section definitions:

    Title
    =====

    Subtitle
    --------

    Section
    ```````

    Subsection
    ~~~~~~~~~~

    """

    sections = ('title', 'subtitle', 'section', 'subsection')
    roles = {
            'input':':input:',
            'outputtext':':outputtext:',
            'outputimage':':outputimage:'
            }
    classes = {
            'input':'.. class:: input',
            'outputtext':'.. class:: outputtext',
            'outputimage':'.. class:: outputimage'
            }
    section_marks = {
            'title':'=',
            'subtitle':'-',
            'section':'`',
            'subsection':'~'
            }


    def format_cell(self, style, content):
        if style in self.sections:
            s = "\n" + content + "\n"
            s += str(self.section_marks[style] * len(content))
            s += "\n\n"
        elif style == 'outputimage':
            #content = content.decode('string escape')
            #xxx Uh, might not, uh, what 
            basepath = self.env_path
            fullpath = basepath + content[7:] 
            s = '.. image:: ' + fullpath + '\n\n'
        else:
            #content = content.decode('string escape')
            c = content.splitlines()
            c = '\n| ' + '\n| '.join(c)
            s = self.classes[style]
            s += '\n\n'
            s += c
            s += '\n\n'
        return s

        
    def make_print(self):
        restfile = """
.. role:: hideme 

:hideme:`no title`
"""
        for cell in self.orderlist:
            data = self.cells[cell]
            content = data['content']
            style = data['cellstyle']
            restfile += self.format_cell(style, content)
        self.rest = restfile
        self.save_file('.rst', restfile)
        return str(self.rest)

class Python(Base):
    """Print plain python file with non input cell data commented.
    """

    def make_print(self):
        py_file = """#codenode notebook\n#Title: %s\n\n"""%self.title
        def format_cell(style, content):
            content = str(content)
            if style == 'input':
                return content+'\n'
            elif style == 'outputtext':
                c = content.split('\n')
                c = '#'+'\n#'.join(c)+'\n\n'
                return c
            elif style == 'outputimage':
                return '#Graphics\n\n'
            else:
                return '\"""%s\"""\n\n'%content

        for cell in self.orderlist:
            data = self.cells[cell]
            content = data['content']
            style = data['cellstyle']
            py_file += format_cell(style, content)
        return py_file




formats = {'latex':Latex,'rest':ReST}
