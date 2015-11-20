import sys

import marysue.util as random
from marysue.objects import Object
from marysue.characters import Character, MarySue, TheOptimist
from marysue.storytree import Story, Scene, EventSequence, Paragraph
from marysue.events import *
from marysue.state import State
from marysue.costume import (
    make_torso_costume, make_legs_costume,
    make_onesie_costume, make_feet_costume
)


def edit_story(story, introduced, **kwargs):
    """Standard story-revising pipeline.  Takes a basic Story
    that was generated from a plot and returns a Story that is
    closer to something that you can actually read.
    
    `introduced` is a set of objects that have already been
    introduced in previous stories and that need no introduction
    here.  Objects will be added to it as they are introduced in
    this story.
    """

    ### Massage the generated story ###

    story = merge_adjacent_scenes(story)
    story = resolve_setting_references(story)

    ### Initialize story instant-states and context ###

    all_objects = set()
    collect_objects(story, all_objects)
    story = assign_empty_states(story, objects=all_objects)

    ### Assign locations ###

    story = assign_locations(story)

    ### Assign moods and duties ###

    story = assign_moods(story)
    story = remove_mood_modifier_events(story)

    story = assign_duties(story)
    story = remove_duty_acquisition_events(story)

    ### Elaborate the story ###

    story = describe_scene(story)

    story = assign_costumes(story)
    story = describe_costumes(story)

    newly_introduced = set()
    story = describe_characters(story, introduced, newly_introduced)
    reminded = set(newly_introduced)
    story = remind_characters(story, reminded)

    ### Diction ###

    story = assign_first_occurrence(story)

    story = story.flatten()

    story = split_into_paragraphs(story)
    story = assign_referents(story)
    story = conjoin_sentences(story)

    return story


# - - - - for debugging - - -


def show_state(ast, attr, cls):
    """Example usage: show_state(story, 'subject', StateDutyEvent)"""
    for child in ast:
        show_state(child, cls)
    if isinstance(ast, cls):
        print "%s state is: %r" % (attr, getattr(ast, attr))
        print


# - - - - editor stages - - - -


def collect_objects(ast, object_set):
    """Places all the objects found in the given story tree into the given
    object_set.  Does not return anything, modifies object_set instead."""
    for child in ast:
        collect_objects(child, object_set)
    for key, value in ast.iteritems():
        if isinstance(value, Object):
            object_set.add(value)


def assign_empty_states(ast, context=None, objects=None):
    """Replaces all Object references in a story tree with State objects
    which proxy for those Objects.  These State objects are initially
    empty; further passes will make them reflect what's actually going on."""

    if context is None:
        context = dict((object, State(object)) for object in objects)

    attrs = {}
    for key, value in ast.iteritems():
        if isinstance(value, Object):
            attrs[key] = context[value]
        else:
            attrs[key] = value
    return ast.__class__(*[assign_empty_states(c, context=context) for c in ast], **attrs)


def assign_locations(ast, context=None):
    # And this is entirely so we can say "Her scarf shone in the dim light of the tunnel!"

    if context is None:
        context = {}

    if isinstance(ast, Scene):
        context['location'] = ast.setting

    attrs = {}
    for role, state in ast.iteritems():
        if isinstance(state, State) and isinstance(state.object, Character):
            state = state.clone(location=context['location'])
        attrs[role] = state

    return ast.__class__(*[assign_locations(c, context=context) for c in ast], **attrs)


def assign_costumes(ast, context=None):
    if context is None:
        context = {}

    # reset costumes in each scene
    if isinstance(ast, Scene):
        context = {}

    attrs = {}
    for role, state in ast.iteritems():
        if isinstance(state, State) and isinstance(state.object, Character):
            character = state.object
            if state.object not in context:
                context[character] = {
                    'feet': make_feet_costume(character),
                }
                if random.chance(66):
                    context[character].update({
                        'torso': make_torso_costume(character),
                        'legs': make_legs_costume(character)
                    })
                else:
                    context[character].update({
                        'torso': make_onesie_costume(character),
                        'legs': None
                    })

            entry = context[character]
            state = state.clone(
                torso_costume=entry['torso'],
                legs_costume=entry['legs'],
                feet_costume=entry['feet'],
            )
        attrs[role] = state

    return ast.__class__(*[assign_costumes(c, context) for c in ast], **attrs)


def assign_moods(ast, moods=None):
    if moods is None:
        moods = {}

    if isinstance(ast, MoodModifierEvent):
        moods[ast.subject.object] = ast.mood()

    attrs = {}
    for role, state in ast.iteritems():
        if isinstance(state, State) and isinstance(state.object, Character):
            character = state.object
            if character not in moods:
                print "ERROR", character, "appears before mood assigned, assuming happy"
                moods[character] = 'happy'
            if isinstance(character, TheOptimist):
                # No, I'm not going to let it get me down!
                moods[character] = 'happy'
            state = state.clone(mood=moods[character])
        attrs[role] = state

    return ast.__class__(*[assign_moods(c, moods=moods) for c in ast], **attrs)


def remove_mood_modifier_events(ast):
    children = []
    for child in ast:
        if isinstance(child, MoodModifierEvent):
            if random.chance(10) and isinstance(child.subject.object, TheOptimist) and child.mood() != 'happy':
                children.append(CharacterStaysHappyEvent(subject=child.subject))
        else:
            children.append(remove_mood_modifier_events(child))

    return ast.__class__(*children, **dict(ast.iteritems()))


def assign_duties(ast, duties=None):
    if duties is None:
        duties = {}

    if isinstance(ast, AcquireDutyEvent):
        duties.setdefault(ast.subject.object, set()).add(ast.object.object)

    if isinstance(ast, RelieveDutyEvent):
        duties.setdefault(ast.subject.object, set())
        if ast.object.object not in duties[ast.subject.object]:
            print >>sys.stderr, '%r not in %r`s %r' % (
                ast.object.object, ast.subject.object, duties[ast.subject.object]
            )
        else:
            duties[ast.subject.object].remove(ast.object.object)

    attrs = {}
    for role, state in ast.iteritems():
        if isinstance(state, State) and isinstance(state.object, Character):
            character = state.object
            if character not in duties:
                duties[character] = set()
            state = state.clone(duties=set(duties[character]))
        attrs[role] = state

    return ast.__class__(*[assign_duties(c, duties=duties) for c in ast], **attrs)


def remove_duty_acquisition_events(ast):
    children = []
    for child in ast:
        if not isinstance(child, (AcquireDutyEvent, RelieveDutyEvent)):
            children.append(remove_duty_acquisition_events(child))

    return ast.__class__(*children, **dict(ast.iteritems()))


def assign_referents(ast, context=None):
    if context is None:
        context = {'referent': None}

    # reset referent in each... eventually this will be paragraph
    #if isinstance(ast, Turn):
    #    context['referent'] = None

    attrs = {}
    for role, state in ast.iteritems():
        if isinstance(state, State):
            attrs[role] = state.clone(is_referent=(state.object == context['referent']))
            if role == 'subject':
                context['referent'] = state.object
        else:
            attrs[role] = state

    return ast.__class__(*[assign_referents(c, context) for c in ast], **attrs)


def resolve_setting_references(ast, setting=None):
    if isinstance(ast, Scene):
        setting = ast.setting

    attrs = dict((k, v) for (k, v) in ast.iteritems())

    if isinstance(ast, PoseDescription):
        attrs['object'] = State(setting.nearby_scenery)

    return ast.__class__(*[resolve_setting_references(c, setting=setting) for c in ast], **attrs)


def assign_first_occurrence(ast, occurred=None):
    """We use this to select between definite and indefinite article"""
    # TODO: mentioning in dialogue does not count as first occurrence
    if occurred is None:
        occurred = set()

    attrs = {}
    for role, state in ast.iteritems():
        # first of these is to avoid counting objects in Scene, etc as occurrence
        if isinstance(ast, Event) and isinstance(state, State):
            if state.object not in occurred:
                state = state.clone(first_occurrence=True)
                occurred.add(state.object)
        attrs[role] = state

    return ast.__class__(*[assign_first_occurrence(c, occurred=occurred) for c in ast], **attrs)


def describe_scene(ast):
    children = [c for c in ast]

    if isinstance(ast, Scene):
        children = [EventSequence(
            SettingDescription(
                subject=ast.setting
            ),
            NearbyDescription(
                subject=ast.setting,
                object=State(
                    object=ast.setting.nearby_scenery,
                    location=ast.setting
                )
            ),
            GenericSettingDescription(
                subject=ast.setting,
            ),
            EventSequence(*children)
        )]

    return ast.__class__(*[describe_scene(c) for c in children], **dict(ast.iteritems()))


def describe_characters(ast, described, newly_introduced):
    """Describes them as if we are meeting them for the first time.
    `described` is a set of characters who have already been described.

    `described` persists across several stories, but anyone we do
    describe here, we put in newly_introduced (it's essentially output
    only) so that we can tell not to e.g. remind the reader of their
    appearance overmuch.
    """

    if isinstance(ast, Event):
        if isinstance(ast.subject, State) and isinstance(ast.subject.object, Character):
            if ast.subject.object not in described:
                if isinstance(ast.subject.object, MarySue) or random.chance(50):
                    described.add(ast.subject.object)
                    newly_introduced.add(ast.subject.object)
                    return EventSequence(
                        ast,
                        CharacterDescription(subject=ast.subject),
                        CharacterFeaturesDescription(subject=ast.subject)
                    )

    return ast.__class__(*[describe_characters(c, described, newly_introduced) for c in ast], **dict(ast.iteritems()))


def remind_characters(ast, reminded):
    """Describes them assuming we have already been introduced to them,
    by subtly (hah) reminding us about what they look like."""

    if isinstance(ast, Event):
        if isinstance(ast.subject, State) and isinstance(ast.subject.object, Character):
            if ast.subject.object not in reminded:
                if random.chance(20):
                    reminded.add(ast.subject.object)
                    return EventSequence(
                        ast,
                        CharacterReminder(subject=ast.subject),
                    )

    return ast.__class__(*[remind_characters(c, reminded) for c in ast], **dict(ast.iteritems()))


def describe_costumes(ast, described=None):
    if described is None:
        described = set()

    if isinstance(ast, Scene):
        described = set()

    if isinstance(ast, Event):
        if isinstance(ast.subject, State) and isinstance(ast.subject.object, Character):
            if ast.subject.object not in described:
                if isinstance(ast.subject.object, MarySue) or random.chance(50):
                    described.add(ast.subject.object)
                    return EventSequence(
                        ast,
                        TorsoCostumeReminder(subject=ast.subject) if random.chance(10) else TorsoCostumeDescription(subject=ast.subject),
                        FeetCostumeReminder(subject=ast.subject) if random.chance(10) else FeetCostumeDescription(subject=ast.subject)
                    )

    return ast.__class__(*[describe_costumes(c, described=described) for c in ast], **dict(ast.iteritems()))


def collect_objects_from_states(ast, object_set):
    for child in ast:
        collect_objects_from_states(child, object_set)
    for key, value in ast.iteritems():
        if isinstance(value, State):
            object_set.add(value.object)


def add_crickets(ast):
    if isinstance(ast, LookAtEvent):
        return EventSequence(ast, CricketsEvent())

    return ast.__class__(*[add_crickets(c) for c in ast], **dict(ast.iteritems()))


def merge_adjacent_scenes(ast):
    children = []
    for child in ast:
        if isinstance(child, Scene) and children and isinstance(children[-1], Scene) and child.setting == children[-1].setting:
            new_scene_contents = [gc for gc in children[-1]] + [gc for gc in child]
            # TODO: what if the Scenes differ in OTHER attributes?
            # for now there are none (assume characters are assigned later on)
            children[-1] = Scene(*new_scene_contents, **dict(children[-1].iteritems()))
        else:
            # note that this does not recurse
            children.append(child)

    return ast.__class__(*children, **dict(ast.iteritems()))


def split_into_paragraphs(ast):
    if isinstance(ast, Scene):
        assert len([c for c in ast]) == 1
        eseq = ast[0]
        assert isinstance(eseq, EventSequence)

        children = []
        parachilds = []
        subject = None
        for child in eseq:
            assert isinstance(child, Event), repr(child)
            if child.new_para or (isinstance(child.subject, State) and child.subject.object != subject):
                if parachilds:
                    children.append(parachilds)
                parachilds = []
                if child.subject:
                    subject = child.subject.object
                else:
                    subject = None
            elif not isinstance(child.subject, State):
                if parachilds:
                    children.append(parachilds)
                parachilds = []
                subject = None
            parachilds.append(child)
        if parachilds:
            children.append(parachilds)

        children = [EventSequence(*[Paragraph(*r) for r in children])]
    else:
        children = [split_into_paragraphs(c) for c in ast]

    return ast.__class__(*children, **dict(ast.iteritems()))


def conjoin_sentences(ast):
    if isinstance(ast, Paragraph):
        children = []
        for child in ast:
            if not children or \
               not child.is_conjoinable or \
               isinstance(children[-1], ConjoinedEvent) or \
               random.chance(100):  # DISABLED because for now it's kind of awful to read
                children.append(child)
            else:
                last = children[-1]
                compound = ConjoinedEvent(event1=last, event2=child)
                children[-1] = compound
    else:
        children = [conjoin_sentences(c) for c in ast]

    return ast.__class__(*children, **dict(ast.iteritems()))
