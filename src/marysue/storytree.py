from marysue.ast import AST
from marysue.util import capitalize


class Story(AST):
    def render(self):
        return (
            '\n\n- - - -\n\n'.join([child.render() for child in self])
        )


class Scene(AST):
    slots = ('setting',)

    def render(self):
        return '\n\n'.join([child.render() for child in self])


class EventSequence(AST):
    def render(self):
        return '\n\n'.join([capitalize(child.render()) for child in self])

    def flatten(self):
        return EventSequence(*list(self.all_children()), **dict(self.iteritems()))

    def all_children(self):
        for child in self:
            if isinstance(child, EventSequence):
                for descendant in child.all_children():
                    yield descendant
            else:
                yield child


# - - - -


class Paragraph(AST):
    """Only used at the end"""
    def render(self):
        from marysue.events import Event

        s = ''
        for child in self:
            s += capitalize(child.render())
            if isinstance(child, Event) and child.exciting:
                s += '!  '
            else:
                s += '.  '
        return s.rstrip()

    def flatten(self):
        return Paragraph(*list(self.all_children()), **dict(self.iteritems()))

    def all_children(self):
        for child in self:
            if isinstance(child, Paragraph):
                for descendant in child.all_children():
                    yield descendant
            else:
                yield child
