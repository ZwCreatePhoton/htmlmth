from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html


def _generate_insert_many_slash_after_opening_tag_names(*args, **kwargs):
    N = kwargs.get("N", 10000)
    return TransformFunction("",
                              'insert many "/" after opening tag names excluding html tag',
                              mime_type_based_transform({
                                  'text/html': string_to_tfarg_function(lambda x: htmlmth.mods.html.insert_slash_after_opening_tag_names(x, N, exclude=["html"]))
                              }))

insert_many_slash_after_opening_tag_names = _generate_insert_many_slash_after_opening_tag_names()
insert_many_slash_after_opening_tag_names.parameterize = _generate_insert_many_slash_after_opening_tag_names

