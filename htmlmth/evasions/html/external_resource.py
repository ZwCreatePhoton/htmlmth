from . import TransformFunction, mime_type_based_transform
import htmlmth.mods.html


external_resource_internal_script = TransformFunction("",
                                         "internal scripts changed to external scripts",
                                         mime_type_based_transform({
                                             'text/html': htmlmth.mods.html.external_resource_internal_script
                                         }))
