import chevron
from case_conversion import case_conversion

from accio.errors import TemplateError
from accio.sandbox.context import Context


def render(content: str, context: Context) -> str:
    code, template = _parse(content)
    run_code(code, context)
    return chevron.render(template, context.variables)


def run_code(code, context):
    # sandbox exec environment allowing only most common libraries
    exec(code, {
        # '__builtins__': None,
        "context": context,
        "case_conversion": case_conversion
    })


def _parse(template):
    if template[:4] != '---\n':
        raise TemplateError('Template must start with the front matter indicator')

    closing_pos = template.find('\n---\n')

    if closing_pos == -1:
        raise TemplateError('No closing for front matter found')

    front_matter = template[4:closing_pos]
    content = template[closing_pos+5:]

    return front_matter, content
