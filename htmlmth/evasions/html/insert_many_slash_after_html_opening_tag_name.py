from . import TransformFunction, string_to_tfarg_function, mime_type_based_transform
import htmlmth.mods.html

insert_many_slash_after_html_opening_tag_name = TransformFunction("",
                                                                  'insert many "/" after html opening tag name',
                                                                  mime_type_based_transform({
                                                                      'text/html': string_to_tfarg_function(lambda x : htmlmth.mods.html.insert_slash_after_opening_tag_names(x, 1650, include=["html"]))
                                                                  }))
