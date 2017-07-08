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
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from pandocfilters import RawBlock, applyJSONFilters


logger = logging.getLogger(__name__)
static_storage = FileSystemStorage(
    settings.STATIC_ROOT,
    base_url=settings.STATIC_URL,
)

ARGUMENT_RE = re.compile(r'^[-]+(.*)$')


def run_with_checks(command, args, input=None):
    """
    Runs the given executable with error reporting.
    """
    p = Popen(
        (command,) + args,
        stdin=None if input is None else PIPE,
        stdout=PIPE, stderr=PIPE,
    )

    if p.returncode is not None:
        raise RuntimeError('{} exited with status {} before communication: {}'.format(
            command,
            p.returncode,
            p.stderr.read(),
        ))

    try:
        out, err = p.communicate(input=input)
    except OSError:
        raise RuntimeError('{} exited with status {} during communication'.format(
            command,
            p.returncode,
        ))

    if p.returncode != 0:
        raise RuntimeError('{} exited with status {} during communication. stdout: {}, stderr: {}'.format(
            command,
            p.returncode,
            out.decode('utf-8'),
            err.decode('utf-8'),
        ))

    return out.decode('utf-8')


def tex_to_svg(template_name, context, crop=False):
    tex_content = render_to_string(
        template_name,
        context=context,
    ).encode('utf-8')

    hsh = hashlib.md5(tex_content).hexdigest()
    path = os.path.join('tex-cache', '{}.svg'.format(hsh))

    if static_storage.exists(path):
        return static_storage.url(path)

    with TemporaryDirectory() as tmp_dir:
        run_with_checks(
            'pdflatex',
            ('-output-directory', tmp_dir, '-jobname', hsh, '--'),
            input=tex_content,
        )

        pdf_file = os.path.join(tmp_dir, hsh + '.pdf')
        pdf_cropped_file = os.path.join(tmp_dir, hsh + '-cropped.pdf')
        svg_file = os.path.join(tmp_dir, hsh + '.svg')

        if crop:
            run_with_checks('pdfcrop', (pdf_file, pdf_cropped_file))
            run_with_checks('pdf2svg', (pdf_cropped_file, svg_file))
        else:
            run_with_checks('pdf2svg', (pdf_file, svg_file))

        with open(svg_file, 'r') as f:
            static_storage.save(path, f)

    return static_storage.url(path)


def convert(input, *args):
    """
    Converts the given string input with pandoc and the given arguments.
    """
    return run_with_checks('pandoc', ('-S',) + args, input=input.encode('utf-8'))


TEX_ENVS = (
    r'\begin{tikzpicture}',
    r'\begin{equation*}',
    r'\begin{equation}',
    r'\begin{align*}',
    r'\begin{align}',
)


def tex_filter(key, value, format, _):
    """
    A pandoc filter which converts block of raw latex into standalone svg
    elements.
    """
    if key != 'RawBlock':
        return

    fmt, content = value

    if fmt != 'latex':
        return

    if not any(content.startswith(env) for env in TEX_ENVS):
        return

    if content.startswith(r'\begin{tikzpicture}'):
        url = tex_to_svg('figure.tex', {'content': content})
    else:
        url = tex_to_svg('math.tex', {'content': content}, crop=True)

    img = '<img class="uk-align-center" src="{}"/>'.format(url)

    return RawBlock('html', img)


def convert_with_tex(content):
    json = convert(content, '--from', 'markdown', '--to', 'json', '--katex')

    altered = applyJSONFilters([tex_filter], json)

    return convert(altered, '--from', 'json', '--to', 'html')
