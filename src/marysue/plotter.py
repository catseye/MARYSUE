from marysue.util import log
from marysue.storytree import Story, Scene, EventSequence
from marysue.events import *
from marysue.objects import Group
from marysue.characters import MarySue, DreamBoat

from marysue.plot import *


# - - - -


class PlotHole(AST):
    """Represents a place in the plot tree that will be filled in with
    a subplot."""

    slots = (
        'rules',
        'setting',
        'goons',
        'abductee',
        'abductee_location',
    )

    def flatten(self):
        raise NotImplementedError

    def render(self):
        return "((to be written))"


# - - - -


class InapplicableRuleError(ValueError):
    pass


class PlotRewritingRule(object):
    def assign_participants(self, plotter, plot_hole, unavailable):
        """plotter is the Plotter object that is applying this rule.

        plot_hole is the PlotHole that is being rewritten into a (sub)plot.

        """
        self.plotter = plotter
        self.plot_hole = plot_hole
        self.setting = plot_hole.setting
        self.unavailable = unavailable
        try:
            self.assign_participants_impl()
            return True
        except InapplicableRuleError:
            return False

    def assign_participants_impl(self):
        raise NotImplementedError

    def only_at_home(self):
        if self.plot_hole.setting != self.plotter.home:
            raise InapplicableRuleError

    def not_at_home(self):
        if self.plot_hole.setting == self.plotter.home:
            raise InapplicableRuleError

    def compute_protagonists(self):
        self.protagonists = set(self.plotter.protagonists) - self.unavailable

    def pick_protagonist_and_others(self, filter=None):
        if filter is None:
            filter = lambda x: True
        eligible = set([x for x in self.protagonists if filter(x)])
        if not eligible:
            raise InapplicableRuleError
        self.p1 = random.choice(eligible)
        self.others = set(self.protagonists)
        self.others.remove(self.p1)
        if not self.others:
            raise InapplicableRuleError

    def pick_antagonist(self):
        self.a1 = random.choice(self.plotter.antagonists)

    def pick_macguffin(self):
        eligible = set(self.plotter.macguffins) - self.unavailable
        if not eligible:
            raise InapplicableRuleError
        self.m1 = random.choice(eligible)

    def pick_mary_sue_and_dreamboat(self):
        self.mary_sues = tuple([p for p in self.protagonists if isinstance(p, MarySue)])
        self.dreamboats = tuple([p for p in self.protagonists if isinstance(p, DreamBoat)])
        if not self.mary_sues or not self.dreamboats:
            raise InapplicableRuleError
        self.mary_sue = random.choice(self.mary_sues)
        self.dreamboat = random.choice(self.dreamboats)

    def generate(self, plotter):
        raise NotImplementedError


def not_mary_sue(obj):
    return not isinstance(obj, MarySue)


# - - - -


class KidnappingRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.pick_protagonist_and_others(filter=not_mary_sue)
        self.pick_antagonist()

    def generate(self, plotter):
        bystanders = Group(*self.others)
        abductee_location = self.a1.home
        return PlotSequence(
            Kidnapping(
                subject=self.a1, object=self.p1, setting=self.setting,
                bystanders=bystanders, disqualified=self.p1,
                exeunt=bystanders
            ),
            PlotHole(
                setting=self.setting,
                abductee=self.p1,
                abductee_location=abductee_location,
                rules=(
                    FindAbducteeRule,
                    ContemplateRockRule,
                )
            ),
            PlotHole(
                setting=abductee_location,
                rules=(
                    KidnappingRule,
                    FindAnotherWayRule,
                    LostItemRule,
                    CaveInRule,
                    GoonSkirmishRule,
                    AwkwardTensionRule,
                    RomanticTensionRule,
                    RomanticResolutionRule,
                    ContemplateRockRule,
                )
            ),
            Rescue(
                subject=Group(*self.others), object=self.p1,
                setting=self.a1.home, requalified=self.p1,
                exeunt=Group(*self.protagonists)
            ),
        )


class FindAbducteeRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()

    def generate(self, plotter):
        return PlotSequence(
            LocateAbductee(
                subject=Group(*self.protagonists),
                object=self.plot_hole.abductee,
                object2=self.plot_hole.abductee_location,
                setting=self.setting
            ),
            PlotHole(
                setting=self.setting,
                abductee=self.plot_hole.abductee_location,
                rules=(
                    ContemplateRockRule,
                )
            ),
        )


class FindAnotherWayRule(PlotRewritingRule):
    def assign_participants_impl(self):
        if not self.plot_hole.setting.outside_setting:
            raise InapplicableRuleError
        self.plot_hole.setting
        self.compute_protagonists()

    def generate(self, plotter):
        new_setting = self.plot_hole.setting.outside_setting
        return PlotSequence(
            WayBlocked(
                subject=Group(*self.protagonists), setting=self.setting
            ),
            PlotHole(
                setting=new_setting,
                rules=(
                    KidnappingRule,
                    LostItemRule,
                    CaveInRule,
                    GoonSkirmishRule,
                    AwkwardTensionRule,
                    RomanticTensionRule,
                    ContemplateRockRule,
                )
            ),
        )


class LostItemRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.pick_protagonist_and_others()
        self.pick_macguffin()
        self.mary_sues = tuple([p for p in self.protagonists if isinstance(p, MarySue)])

    def generate(self, plotter):
        recoverer = self.p1
        if self.mary_sues:
            recoverer = random.choice(self.mary_sues)

        # recompute bystanders so that we dont have them overlapping w/ subject
        non_losers = self.protagonists - set([self.p1])
        non_recoverers = self.protagonists - set([recoverer])

        return PlotSequence(
            LoseItem(
                subject=self.p1, object=self.m1, setting=self.setting,
                bystanders=Group(*non_losers), disqualified=self.m1
            ),
            PlotHole(
                setting=self.setting,
                rules=(
                    KidnappingRule,
                    CaveInRule,
                    GoonSkirmishRule,
                    AwkwardTensionRule,
                    RomanticTensionRule,
                    ContemplateRockRule,
                    DroneRule,
                )
            ),
            RecoverItem(
                subject=recoverer, object=self.m1, setting=self.setting,
                bystanders=Group(*non_recoverers), requalified=self.m1
            ),
        )


class CaveInRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.not_at_home()
        self.compute_protagonists()
        self.pick_protagonist_and_others(filter=not_mary_sue)

    def generate(self, plotter):
        return PlotSequence(
            TrappedInRubble(subject=self.p1, bystanders=Group(*self.others),
                            setting=self.setting, disqualified=self.p1),
            PlotHole(
                setting=self.setting,
                rules=(
                    KidnappingRule,
                    GoonSkirmishRule,
                )
            ),
            ExtractedFromRubble(
                subject=Group(*self.others), object=self.p1,
                setting=self.setting, requalified=self.p1
            ),
            PlotHole(
                setting=self.setting,
                rules=(
                    GoonSkirmishRule,
                    AwkwardTensionRule,
                    RomanticTensionRule,
                    ContemplateRockRule,
                )
            ),
        )


class GoonSkirmishRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.not_at_home()
        self.compute_protagonists()
        self.goons = random.choice(self.plotter.goons)

    def generate(self, plotter):
        meeting = random.choice((
            GoonEncounter(
                setting=self.setting,
                subject=Group(*self.protagonists),
                object=self.goons,
            ),
            GoonAmbush(
                setting=self.setting,
                subject=Group(*self.protagonists),
                object=self.goons,
            ),
        ))

        return PlotSequence(
            meeting,
            PlotHole(
                setting=self.setting,
                goons=self.goons,
                rules=(
                    ProtagonistAttackRule,
                    AwkwardCombatRule,
                )
            ),
            Vanquished(
                setting=self.setting,
                subject=Group(*self.protagonists),
                object=self.goons,
                object2=random.choice(self.plotter.antagonists),
            ),
            #PlotHole(setting=self.setting),
        )


class ProtagonistAttackRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.goons = self.plot_hole.goons
        # for hilarious effect:
        #   self.goons = random.choice(self.plotter.goons)

    def generate(self, plotter):
        return PlotSequence(
            PlotHole(
                setting=self.setting,
                goons=self.goons,
                rules=(
                    ProtagonistAttackRule,
                    AwkwardCombatRule,
                )
            ),
            ProtagonistAttack(
                subject=Group(*self.protagonists),
                object=self.goons, setting=self.setting
            ),
        )


class AwkwardCombatRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.pick_mary_sue_and_dreamboat()
        self.goons = self.plot_hole.goons

    def generate(self, plotter):
        return PlotSequence(
            PlotHole(
                setting=self.setting,
                goons=self.goons,
                rules=(
                    ProtagonistAttackRule,
                    AwkwardCombatRule,
                )
            ),
            AwkwardCombat(
                subject=Group(self.mary_sue, self.dreamboat),
                object=self.goons,
                setting=self.setting
            ),
        )


class AwkwardTensionRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.pick_mary_sue_and_dreamboat()

    def generate(self, plotter):
        a = self.dreamboat
        b = self.mary_sue
        if random.chance(33):
            a, b = b, a

        return PlotSequence(
            AwkwardTension(
                setting=self.setting,
                subject=a, object=b,
            ),
            PlotHole(
                setting=self.setting,
                rules=(
                    KidnappingRule,
                    LostItemRule,
                    CaveInRule,
                    GoonSkirmishRule,
                    ContemplateRockRule,
                    DroneRule,
                )
            ),
        )


class RomanticTensionRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.pick_mary_sue_and_dreamboat()

    def generate(self, plotter):
        a = self.dreamboat
        b = self.mary_sue
        if random.chance(33):
            a, b = b, a

        return PlotSequence(
            RomanticTension(
                setting=self.setting,
                subject=a, object=b,
            ),
            PlotHole(
                setting=self.setting,
                # we should try to interrupt this with something exciting!
                rules=(
                    KidnappingRule,
                    LostItemRule,
                    CaveInRule,
                    GoonSkirmishRule,
                )
            ),
        )


class RomanticResolutionRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.pick_mary_sue_and_dreamboat()

    def generate(self, plotter):
        return PlotSequence(
            RomanticResolution(
                setting=self.setting,
                subject=self.dreamboat, object=self.mary_sue,
            )
        )


class ContemplateRockRule(PlotRewritingRule):
    def assign_participants_impl(self):
        self.compute_protagonists()
        self.pick_protagonist_and_others()   # Note: this prevents solo
        self.o1 = self.setting.nearby_takeable

    def generate(self, plotter):
        return PlotSequence(
            ContemplateRock(subject=self.p1, object=self.o1,
                            setting=self.setting,),
            PlotHole(
                setting=self.setting,
                rules=(
                    KidnappingRule,
                    LostItemRule,
                    CaveInRule,
                    GoonSkirmishRule,
                    AwkwardTensionRule,
                    RomanticTensionRule,
                    DroneRule,
                )
            ),
        )


class DroneRule(PlotRewritingRule):
    def assign_participants_impl(self):
        if not self.plot_hole.setting.has_drones:
            raise InapplicableRuleError
        self.compute_protagonists()
        self.pick_protagonist_and_others()   # Note: this prevents solo

    def generate(self, plotter):
        return PlotSequence(
            Drone(subject=self.p1, setting=self.setting),
            PlotHole(
                setting=self.setting,
                rules=(
                    KidnappingRule,
                    LostItemRule,
                    AwkwardTensionRule,
                    RomanticTensionRule,
                )
            ),
        )


def all_rules():
    return [
        c for c in globals().values() if c.__class__ == type and
                                         issubclass(c, PlotRewritingRule) and
                                         c != PlotRewritingRule
    ]


# - - - -


class Plotter(object):
    def __init__(self, protagonists, antagonists, goons, macguffins, settings):
        """All arguments should be iterables"""
        self.protagonists = tuple(protagonists)
        self.antagonists = tuple(antagonists)
        self.goons = tuple(goons)
        self.macguffins = tuple(macguffins)
        self.settings = tuple(settings)
        self.home = self.settings[0]

    def fill_plot_hole(self, plot_hole, unavailable):
        generators = [cls() for cls in plot_hole.rules]
        generators = [
            g for g in generators
            if g.assign_participants(self, plot_hole, unavailable)
        ]
        if not generators:
            #print "no applicable plot rule found!"
            return plot_hole
        else:
            # NOTE: must be tuple()!  Not set()!  Much badness with set()!
            # (It's because these Rule objects are not hashable/immutable.)
            generators = tuple(generators)
            return random.choice(generators).generate(self)

    def complicate_plot(self, plot, unavailable=None):
        if unavailable is None:
            unavailable = set()

        if isinstance(plot, PlotHole):
            return self.fill_plot_hole(plot, unavailable)

        if plot.disqualified:
            unavailable.add(plot.disqualified)
        if plot.requalified:
            unavailable.remove(plot.requalified)

        children = [
            self.complicate_plot(c, unavailable=unavailable) for c in plot
        ]
        return plot.__class__(*children, **dict(plot.iteritems()))

    # - - - -

    def remove_plot_holes(self, plot):
        if isinstance(plot, PlotHole):
            raise ValueError

        children = [
            self.remove_plot_holes(c) for c in plot if not isinstance(c, PlotHole)
        ]
        return plot.__class__(*children, **dict(plot.iteritems()))

    def commute_commutable_plots(self, plot):
        # requires flat plot
        children = []
        for child in plot:
            if children:
                last_scene = children[-1]
                if last_scene.setting == child.setting and \
                   isinstance(last_scene, (Rescue, RecoverItem)) and \
                   isinstance(child, (Rescue, RecoverItem)):
                    p1 = last_scene.all_involved_characters()
                    p2 = child.all_involved_characters()

                    if p2 <= p1:
                        self.commuted_plots.append(
                            (last_scene.__class__.__name__,
                             last_scene.object.definite,
                             child.__class__.__name__,
                             child.object.definite)
                        )
                        children[-1] = child
                        child = last_scene
            children.append(child)

        return plot.__class__(*[self.commute_commutable_plots(c) for c in children], **dict(plot.iteritems()))

    def remove_repetitive_plots(self, plot):
        # requires flat plot
        children = []
        for child in plot:
            add_it = True
            if children:
                last_scene = children[-1]
                # other possibilities: ContemplateRock
                if isinstance(last_scene, AwkwardTension) and isinstance(child, AwkwardTension):
                    add_it = False
            if add_it:
                children.append(child)

        return plot.__class__(*children, **dict(plot.iteritems()))

    def add_journeys(self, plot):
        # requires flat plot
        children = []
        for child in plot:
            if children:
                last_scene = children[-1]
                if not isinstance(last_scene, Journey) and last_scene.setting != child.setting:
                    travellers = last_scene.exeunt
                    if not travellers:
                        # ideally, we should always compute exeunt in the
                        # plot node, but for now we try to do it here
                        travellers = []
                        if isinstance(last_scene.bystanders, Group):
                            for b in last_scene.bystanders:
                                travellers.append(b)
                        elif last_scene.bystanders:
                            raise AssertionError
                        if isinstance(last_scene.subject, Group):
                            for s in last_scene.subject:
                                travellers.append(s)
                        elif last_scene.subject:
                            travellers.append(last_scene.subject)
                    children.append(Journey(
                        subject=Group(*travellers),
                        setting=children[-1].setting,
                        object=child.setting,
                    ))
            children.append(child)

        return plot.__class__(*children, **dict(plot.iteritems()))

    def encounter_new_settings(self, plot, context=None):
        # rerquires flat plot (for reasons which are not *very* good)
        if context is None:
            context = {
                'setting': plot.setting,
                'seen': set([self.home]),
                'unavailable': set(),
            }

        if plot.disqualified:
            context['unavailable'].add(plot.disqualified)
        if plot.requalified:
            context['unavailable'].remove(plot.requalified)

        available = set(self.protagonists) - context['unavailable']

        if available and plot.setting != context['setting'] and \
           plot.setting not in context['seen']:
            context['setting'] = plot.setting
            context['seen'].add(plot.setting)
            plot = PlotSequence(
                EncounterNewSetting(
                    subject=Group(*list(available)),
                    setting=plot.setting,
                ),
                plot,
            )
            return plot

        children = [self.encounter_new_settings(c, context=context) for c in plot]
        return plot.__class__(*children, **dict(plot.iteritems()))

    def find_chekovs_guns(self, plot, gun_holders):
        if isinstance(plot, LoseItem):
            if plot.object not in gun_holders:
                gun_holders.setdefault(plot.object, set()).add(plot.subject)

        for child in plot:
            self.find_chekovs_guns(child, gun_holders)

    def add_chekovs_gun(self, plot, holder, chekovs_gun):
        if isinstance(plot, Introduction):
            others = set(plot.subject)
            others.remove(holder)
            return PlotSequence(
                plot,
                ChekovsGun(
                    subject=holder,
                    object=chekovs_gun,
                    bystanders=Group(*list(others)),
                    setting=plot.setting
                )
            )
        elif not self.added_chekovs_fun and isinstance(plot, Convalescence):
            self.added_chekovs_fun = True
            others = set(plot.subject)
            others.remove(holder)
            return PlotSequence(
                plot,
                ChekovsFun(
                    subject=holder,
                    object=chekovs_gun,
                    bystanders=Group(*list(others)),
                    setting=plot.setting
                )
            )
        else:
            children = [self.add_chekovs_gun(c, holder, chekovs_gun) for c in plot]
            return plot.__class__(*children, **dict(plot.iteritems()))

    # - - - -

    def write_plot(self, depth=5):
        home = self.home
        plot = PlotSequence(
            Introduction(
                setting=home,
                subject=Group(*self.protagonists),
            ),
            PlotHole(
                setting=home,
                rules=(
                    ContemplateRockRule,
                    LostItemRule,
                    AwkwardTensionRule,
                    KidnappingRule,
                    DroneRule,
                ),
            ),
            Convalescence(
                setting=home,
                subject=Group(*self.protagonists),
            ),
            AllLaugh(
                setting=home,
                subject=Group(*self.protagonists),
            )
        )

        # we flatten the plot frequently to help stay under max recursion depth
        for i in xrange(0, depth):
            plot = self.complicate_plot(plot)
            plot = plot.flatten()
        plot = self.remove_plot_holes(plot)
        plot = plot.flatten()
        plot = self.remove_repetitive_plots(plot)

        self.commuted_plots = []
        plot = plot.flatten()
        plot = self.commute_commutable_plots(plot)

        plot = plot.flatten()
        plot = self.encounter_new_settings(plot)
        plot = plot.flatten()
        plot = self.add_journeys(plot)

        chekovs_guns = {}
        self.find_chekovs_guns(plot, chekovs_guns)

        self.added_chekovs_fun = False
        for chekovs_gun, holders in chekovs_guns.iteritems():
            # TODO interesting variation: could we have BOTH of them as holders?
            holder = random.choice(holders)
            plot = self.add_chekovs_gun(plot, holder, chekovs_gun)
            plot = plot.flatten()

        return plot

    def plot_to_story(self, plot):
        plot = plot.flatten()
        scenes = []
        for plot_point in plot:
            events = [e for e in plot_point.create_events() if e is not None]
            scenes.append(Scene(EventSequence(*events), setting=plot_point.setting))
    
        return Story(*scenes)

    def count_plot_classes(self, plot, cls):
        if isinstance(plot, cls):
            return 1
        return sum([self.plot_contains_class(c, cls) for c in plot])

    def plot_contains_class(self, plot, cls):
        if isinstance(plot, cls):
            return True
        return any([self.plot_contains_class(c, cls) for c in plot])

    def generate_acceptable_plot(self, plot_min=(), plot_max=(),
                                 plot_depth=5, **kwargs):
        acceptable_plot = False
        while not acceptable_plot:
            plot = self.write_plot(depth=plot_depth)
            acceptable_plot = True
            for (cls, min) in plot_min:
                if self.count_plot_classes(plot, cls) < min:
                    acceptable_plot = False
                    #log('unacceptable, violates', constraint)
                    break
            for (cls, max) in plot_max:
                if self.count_plot_classes(plot, cls) > max:
                    acceptable_plot = False
                    #log('unacceptable, violates', constraint)
                    break
        #log('commuted plots:', self.commuted_plots)
        return plot
