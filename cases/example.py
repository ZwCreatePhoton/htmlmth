from collections import OrderedDict

from htmlmth.utils import TransformFunction
import htmlmth.evasions.html
import htmlmth.evasions.http


# returns an OrderedDict of cases with (casenames, case) as items
def get_cases(long_descriptions=False):
    cases = []

    # A case is defined as an instance of TransformFunction.
    # Arguments are (casename, description, ...) where ... are instances of TransformFunction (predefined in package: htmlmth.evasions)
    cases.append(TransformFunction("example-null-001", None, htmlmth.evasions.http.null))
    cases.append(TransformFunction("example-middle-011", None,
                                   htmlmth.evasions.html.remove_html_comments,
                                   htmlmth.evasions.http.status_code_4xx.parameterize(statuscode=414)))

    simple_index = len(cases)

    # description cleanup
    if not long_descriptions:
        TransformFunction.cleanup_descriptions(cases, simple_index)

    return OrderedDict([(c.name, c) for c in cases])
