from __future__ import unicode_literals

from subprocess import Popen, PIPE
try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')
import hashlib
import logging
import os
import re

from backports.tempfile import TemporaryDirectory
from django.core.cache import cache
from django.template.loader import render_to_string
from pandocfilters import RawBlock, applyJSONFilters


logger = logging.getLogger(__name__)

ARGUMENT_RE = re.compile(r'^[-]+(.*)$')


def tex_to_svg(template_name, context):
    tex_content = render_to_string(
        template_name,
        context=context,
    ).encode('utf-8')

    tex_hash = hashlib.md5(tex_content).hexdigest()
    key = 'django_tikz:' + tex_hash

    cached = cache.get(key)
    if cached is not None:
        return cached

    with TemporaryDirectory() as tmp_dir:
        pdflatex_proc = Popen(
            ['pdflatex', '-output-directory', tmp_dir, '-jobname', tex_hash, '--'],
            stdin=PIPE,
            stdout=DEVNULL, stderr=DEVNULL,
        )
        pdflatex_proc.communicate(tex_content)

        pdf_file = os.path.join(tmp_dir, tex_hash + '.pdf')
        svg_file = os.path.join(tmp_dir, tex_hash + '.svg')

        pdf2svg_proc = Popen(
            ['pdf2svg', pdf_file, svg_file],
            stdout=DEVNULL, stderr=DEVNULL,
        )
        pdf2svg_proc.wait()

        with open(svg_file, 'r') as f:
            svg_content = f.read()

    cache.set(key, svg_content)

    return svg_content


def convert(input, *args):
    """
    Converts the given string input with pandoc and the given arguments.
    """
    p = Popen(('pandoc',) + args, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    if p.returncode is not None:
        raise RuntimeError('Pandoc exited with status {} before conversion: {}'.format(
            p.returncode,
            p.stderr.read(),
        ))

    try:
        out, err = p.communicate(input.encode('utf-8'))
    except OSError:
        raise RuntimeError('Pandoc exited with status {} during conversion'.format(
            p.returncode,
        ))

    if p.returncode != 0:
        raise RuntimeError('Pandoc exited with status {} during conversion: {}'.format(
            p.returncode,
            err,
        ))

    return out.decode('utf-8')


def tex_filter(key, value, format, _):
    """
    A pandoc filter which converts block of raw latex into standalone svg
    elements.
    """
    if key != 'RawBlock':
        return

    fmt, content = value

    if fmt != 'latex' or r'\begin{tikzpicture}' not in content:
        return

    svg = tex_to_svg('standalone.tex', {'content': content})
    if svg.startswith(r'<?xml'):
        svg = svg.split('\n', 1)[1]

    return RawBlock('html', svg)


def convert_with_tex(content):
    json = convert(content, '--from', 'markdown', '--to', 'json', '--katex')

    altered = applyJSONFilters([tex_filter], json)

    return convert(altered, '--from', 'json', '--to', 'html')
