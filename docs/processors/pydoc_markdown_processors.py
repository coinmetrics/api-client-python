from pydoc_markdown.interfaces import Processor


class DeprecationProcessor(Processor):
    def process(self, graph):
        for module in graph.modules:
            for obj in module.members.values():
                if obj.decorators and 'deprecated' in obj.decorators:
                    obj.docstring = f"**Deprecated:** {obj.docstring or ''}"
