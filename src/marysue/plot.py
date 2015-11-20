import marysue.util as random
from marysue.ast import AST
from marysue.storytree import EventSequence
from marysue.events import *
from marysue.duties import RescueDuty, RetrieveDuty
from marysue.characters import Character, TheOptimist, MarySue


class Plot(AST):
    slots = (
        'subject',        # often a Group instead of a single character
        'object',         # usually a single characters
        'object2',        # used rarely
        'bystanders',     # other characters witnessing this
        'exeunt',         # characters eligible to travel to another setting
        'disqualified',
        'requalified',
        'setting',        # the current setting
    )


class PlotSequence(Plot):
    """Acts as a container for (sub)sequences of PlotDevelopments."""

    def render(self):
        return '.  '.join([child.render() for child in self]) + '.'

    def print_synopsis(self):
        for n, point in enumerate(self):
            assert point.setting, point
            print "%s. %s %s,\n   %s." % (
                n, point.setting.preposition, point.setting.definite,
                point.render()
            )

    def flatten(self):
        return self.__class__(*list(self.all_children()), **dict(self.iteritems()))

    def all_children(self):
        for child in self:
            if isinstance(child, self.__class__):
                for descendant in child.all_children():
                    yield descendant
            else:
                yield child


class PlotDevelopment(Plot):
    def create_events(self):
        raise NotImplementedError

    def all_involved_characters(self):
        return Character.characters_to_set(self.subject, self.object, self.object2, self.bystanders)
        


# - - - -


class Introduction(PlotDevelopment):
    templates = (
        "We are introduced to {subject.def}",
    )

    def create_events(self):
        e = [BecomeHappyEvent(subject=s) for s in self.subject]
        seen = set()
        for s in self.subject:
            if not seen or random.chance(66):
                if random.chance(85):
                    e.append(PoseDescription(subject=s))
                else:
                    e.append(random.choice((
                        OutOfEggsEvent(subject=s),
                        GenericHyperCrystalUsageEvent(subject=s),
                    )))
            if seen and random.chance(66):
                e.append(GreetEvent(subject=s, object=random.choice(seen)))
            seen.add(s)
        return e


class ChekovsGun(PlotDevelopment):
    templates = (
        "{object.def} is foreshadowed by {subject.def}, witnessed by {bystanders.def}",
    )

    def create_events(self):
        holder = self.subject
        asker = random.choice(self.bystanders)
        return [
            EventSequence(
                IntroduceItemEvent(subject=holder, object=self.object),
                AskAboutItemEvent(subject=asker, object=self.object),
                ReplyAboutItemEvent(subject=holder, object=asker),
            )
        ]


class ChekovsFun(PlotDevelopment):
    templates = (
        "{subject.def} is reminded of their mishaps with {object.def}, witnessed by {bystanders.def}",
    )

    def create_events(self):
        holder = self.subject
        asker = random.choice(self.bystanders)
        return [
            EventSequence(
                RememberMacGuffinEvent(subject=asker, object=holder, object2=self.object),
            )
        ]


class Convalescence(PlotDevelopment):
    templates = (
        "{subject.def} convalesce after their adventures",
    )

    def create_events(self):
        prots = set(self.subject)

        ms = random.extract(prots, filter=lambda x: isinstance(x, MarySue))
        capt = random.extract(prots, filter=lambda x: isinstance(x, TheOptimist))

        assert ms and capt
        e = [
            ComplimentActionEvent(subject=capt, object=ms),
            OfferPromotionEvent(subject=capt, object=ms),
            OhYouEvent(subject=ms, object=capt),
            RefusePromotionEvent(subject=ms, object=capt),
        ]
        e += [
            EventSequence(
                BecomeHappyEvent(subject=s),
                ConvalesceEvent(subject=s),
            ) for s in self.subject
        ]
        return e


class AllLaugh(PlotDevelopment):
    # It may seem odd for this to be a plot development, but it
    # turns out to be the easiest way to do it in the current architecture
    templates = (
        "{subject.def} all laugh",
    )

    def create_events(self):
        return [
            AllLaughEvent(),
        ]


# - - - -


class Kidnapping(PlotDevelopment):
    templates = (
        "{subject.def} kidnaps {obj.def}, witnessed by {bystanders.def}",
    )

    def create_events(self):
        all_protagonists = list(self.bystanders) + [self.object]
        perp = self.subject
        duty = RescueDuty(self.object)
        return [
            BecomeHappyEvent(subject=perp),
            AppearEvent(subject=perp),
        ] + [
            BecomeAngryEvent(subject=s) for s in all_protagonists
        ] + [
            NoticeAntagonistEvent(subject=random.choice(self.bystanders), object=perp),
            CackleEvent(subject=perp),
            AntagonistBanterEvent(subject=perp),
            AbductEvent(subject=perp, object=self.object),
            DisappearEvent(subject=perp, object=self.object),
        ] + [
            EventSequence(
                BecomeAngryEvent(subject=s),
                PanicEvent(subject=s),
                AcquireDutyEvent(subject=s, object=duty),
            ) for s in self.bystanders
        ]


class LocateAbductee(PlotDevelopment):
    templates = (
        "{subject.def} must locate where {object.def} is being held",
    )

    def create_events(self):
        prots = set(self.subject)
        b = random.extract(prots, filter=lambda x: isinstance(x, MarySue))
        if not b:
            b = random.extract(prots)
        a = random.extract(prots)
        if not a:
            a = b
        e = [
            WeMustFindThemEvent(subject=a, object=self.object),
            LocationHunchEvent(subject=b, object=self.object, object2=self.object2),
        ]
        if self.setting == a.home:
            e.append(SetCourseEvent(subject=a, object=self.object2))
        else:
            e.append(WeMustGoToEvent(subject=a, object=self.object2))
        return e


class WayBlocked(PlotDevelopment):
    templates = (
        "{subject.def} finds {subject.his} way is blocked",
    )

    def create_events(self):
        prots = set(self.subject)
        a = random.extract(prots)
        b = random.extract(prots)
        return [
            BumpIntoForceFieldEvent(subject=a),
            BecomeSadEvent(subject=a),
            EventSequence(
                WhatWasThatEvent(subject=b),
                BumpIntoForceFieldEvent(subject=b),
                BecomeSadEvent(subject=b),
            ) if b else None,
            MustRetraceStepsEvent(subject=a),
            StateDutyEvent(subject=a),
        ]


class Rescue(PlotDevelopment):
    templates = (
        "{subject.def} rescues {obj.def}",
    )

    def create_events(self):
        # Note: even though this is a different Duty object than was
        # put in the character's duties list, apparently it will work
        # because we made these things immutable -- they hash the same.
        duty = RescueDuty(self.object)
        return [
            KeepMovingEvent(subject=random.choice(self.subject)),
            #WhatWasThatNoiseEvent(subject=random.choice(self.subject)),
            TurnCornerEvent(subject=self.subject),
            BehindBarsDescription(subject=self.object),
        ] + [
            RescueEvent(subject=self.subject, object=self.object),
            BecomeHappyEvent(subject=self.object),
        ] + [
            RelieveDutyEvent(subject=s, object=duty) for s in self.subject
        ] + [
            EventSequence(
                ThankEvent(subject=self.object, object=s),
                BecomeHappyEvent(subject=s),
            ) for s in self.subject
        ]


# - - - -


class LoseItem(PlotDevelopment):
    templates = (
        "{subject.def} loses {obj.def}, witnessed by {bystanders.def}",
    )

    def create_events(self):
        s = self.subject
        duty = RetrieveDuty(self.object)
        e = [
            LookAroundEvent(subject=s),
            HoldEvent(subject=s, object=self.object),
            #CommentOnItemEvent(subject=s, object=self.object),
            TripEvent(subject=s),
            DropEvent(subject=s, object=self.object),
            LoseEvent(subject=self.object),
            BecomeEmbarrassedEvent(subject=s),
            OopsEvent(subject=s),
            AcquireDutyEvent(subject=s, object=duty),
        ]
        for bystander in self.bystanders:
            e.append(BecomeSadEvent(subject=bystander))
            e.append(AcquireDutyEvent(subject=bystander, object=duty))
            e.append(
                random.choice((
                    LookAtEvent(subject=bystander, object=s),
                    GestureAtEvent(subject=bystander, object=s),
                ))
            )

        return e


class RecoverItem(PlotDevelopment):
    templates = (
        "{subject.def} recovers {obj.def}, witnessed by {bystanders.def}",
    )

    def create_events(self):
        s = self.subject
        duty = RetrieveDuty(self.object)
        return [
            LookAroundEvent(subject=s),
            HunchEvent(subject=s),
            LookBehindEvent(subject=s, object=self.setting.nearby_scenery),
            FindEvent(subject=s, object=self.object),
            RelieveDutyEvent(subject=s, object=duty),
            BecomeHappyEvent(subject=s),
        ] + [
            EventSequence(
                RelieveDutyEvent(subject=bystander, object=duty),
                BecomeHappyEvent(subject=bystander),
            ) for bystander in self.bystanders
        ] + [
            ReliefEvent(subject=random.choice(self.bystanders))
        ]


# - - - -


class TrappedInRubble(PlotDevelopment):
    templates = (
        "{subject.def} is trapped under rubble, witnessed by {bystanders.def}",
    )

    def create_events(self):
        s = self.subject
        duty = RescueDuty(self.subject)
        return [
            RumblingSoundEvent(),
            WhatWasThatNoiseEvent(subject=random.choice(self.bystanders)),
            CaveInEvent(subject=self.setting.roof),
            StunnedEvent(subject=s),
            BuriedUnderRubbleEvent(subject=s),
            BecomeSadEvent(subject=s),
        ] + [
            EventSequence(
                BecomeSadEvent(subject=bystander),
                PanicEvent(subject=bystander),
                AcquireDutyEvent(subject=bystander, object=duty),
            ) for bystander in self.bystanders
        ]


class ExtractedFromRubble(PlotDevelopment):
    templates = (
        "{subject.def} dig {obj.def} out of the rubble",
    )

    def create_events(self):
        duty = RescueDuty(self.object)
        return [
            EventSequence(
                WasteNoTimeEvent(subject=s),
                DigOutEvent(subject=s, object=self.object)
            ) for s in self.subject
        ] + [
            BecomeHappyEvent(subject=self.object),
        ] + [
            EventSequence(
                ThankEvent(subject=self.object, object=s),
                BecomeHappyEvent(subject=s),
                RelieveDutyEvent(subject=s, object=duty),
            ) for s in self.subject
        ]


# - - - -


class GoonAmbush(PlotDevelopment):
    templates = (
        "{subject.def} are ambushed by {obj.def}",
    )

    def create_events(self):
        return [
            AttackEvent(subject=self.object, object=self.subject),
        ] + [
            EventSequence(
                BecomeAngryEvent(subject=s),
            ) for s in self.subject
        ] + [
            EventSequence(    
                GenericBattleDescription(),
            )
        ]


class GoonEncounter(PlotDevelopment):
    templates = (
        "{subject.def} encounter a band of {obj.def}",
    )

    def create_events(self):
        prots = set(self.subject)
        a = random.extract(prots)
        return [
            EncounterEvent(subject=self.object, object=self.subject),
            GoonBanterEvent(subject=a, object=self.object),
            GoonParlayEvent(subject=self.object),
        ] + [
            EventSequence(
                BecomeAngryEvent(subject=s),
            ) for s in self.subject
        ] + [
            EventSequence(    
                GenericBattleDescription(),
            )
        ]


class ProtagonistAttack(PlotDevelopment):
    templates = (
        "{subject.def} attack {obj.def}",
    )

    def create_events(self):
        e = []
        # maybe later a fight will have all subjects.  FOR NOW,
        s = random.choice(self.subject)
        w = s.weapon
        e.append(
            EventSequence(
                WarCryEvent(subject=s),
                UnsheathEvent(subject=s, object=w),
                LiftWeaponEvent(subject=s, object=w),
                BringDownWeaponEvent(subject=s, object=w),
                WeaponContactEvent(subject=w, object=self.object),
                FlyAcrossEvent(subject=self.object),
            )
        )
        return e


class AwkwardCombat(PlotDevelopment):
    templates = (
        "{subject.def} get in awkward situation during combat with {obj.def}",
    )

    def create_events(self):
        mary_sue = self.subject[0]
        dreamboat = self.subject[1]
        return [
            EventSequence(
                TryToGetBehindEvent(subject=mary_sue, object=self.object),
                BumpIntoAwkwardlyEvent(subject=mary_sue, object=dreamboat),
                LookAtEvent(subject=dreamboat, object=mary_sue),
                BlushEvent(subject=mary_sue),
                BecomeEmbarrassedEvent(subject=mary_sue),
                RushIntoFrayEvent(subject=dreamboat),
            )
        ]


class Vanquished(PlotDevelopment):
    templates = (
        "{subject.def} vanquish {obj.def} (they were sent by {object2.def})",
    )

    def create_events(self):
        e = [
            AfterBattleEvent(subject=self.object),
        ]
        s = random.choice(self.subject)
        e.append(
            EventSequence(
                AfterBattleBanterEvent(subject=random.choice(self.subject)),
            )
        )
        for s in self.subject:
            e.append(BecomeHappyEvent(subject=s))

        subjects = set(self.subject)
        a = random.extract(subjects)
        b = random.extract(subjects, filter=lambda x: not isinstance(x, TheOptimist))
        e.append(
            EventSequence(
                BecomeAngryEvent(subject=self.object2),  # b/c they need to have a mood assigned first!
                ObserveAfterBattleEvent(subject=a, object=self.object, object2=self.object2),
                RemindReportEvent(subject=a),
            )
        )
        if b:
            e.append(
                EventSequence(
                    BecomeSadEvent(subject=b),
                    IfWeGetHomeEvent(subject=b),
                )
            )

        return e


# - - - -


class AwkwardTension(PlotDevelopment):
    templates = (
        "There is an awkward moment between {subject.def} and {obj.def}",
    )

    def create_events(self):
        s = self.subject
        return [
            BecomeEmbarrassedEvent(subject=self.subject),
            PullAsideEvent(subject=self.subject, object=self.object),
            WantToTalkToYouEvent(subject=self.subject, object=self.object),
            WhatIsItEvent(subject=self.object, object=self.subject),
            RecallPastEventEvent(subject=self.subject, object=self.object),
            BecomeEmbarrassedEvent(subject=self.object),
            BlushEvent(subject=self.object),
            SayNoMoreEvent(subject=self.object, object=self.subject),
            BecomeSadEvent(subject=self.subject),
            BecomeHappyEvent(subject=self.object),
        ]


class RomanticTension(PlotDevelopment):
    templates = (
        "{subject.def} and {obj.def} do mushy stuff (almost)",
    )

    def create_events(self):
        s = self.subject
        e = [
            BecomeEmbarrassedEvent(subject=self.subject),
            PullAsideEvent(subject=self.subject, object=self.object),
            WantToTalkToYouEvent(subject=self.subject, object=self.object),
            WhatIsItEvent(subject=self.object, object=self.subject),
        ]
        done = False
        while not done:
            e.append(EventSequence(
                 FidgetEvent(subject=self.subject, object=self.object),
                 BecomeEmbarrassedEvent(subject=self.object),
                 WhatIsItEvent(subject=self.object, object=self.subject),
                 FacesCloseTogetherEvent(subject=self.object, object=self.subject),
            ))
            if random.chance(33):
                done = True
        e.append(PreludeToKissEvent(subject=self.subject, object=self.object))
        return e


class RomanticResolution(PlotDevelopment):
    templates = (
        "{subject.def} and {obj.def} do mushy stuff",
    )

    def create_events(self):
        s = self.subject
        e = [
            BecomeHappyEvent(subject=self.subject),
            BecomeHappyEvent(subject=self.object),
            PullAsideEvent(subject=self.subject, object=self.object),
            WhatIsItEvent(subject=self.object, object=self.subject),
            MushyStuffEvent(subject=self.subject, object=self.object),
            OhYouEvent(subject=self.object, object=self.subject),
            KissEvent(subject=self.object, object=self.subject),
            AndTheyKissedEvent(subject=self.object, object=self.subject),
            OhYouEvent(subject=self.object, object=self.subject),
        ]
        return e


# - - - -


class Drone(PlotDevelopment):
    templates = (
        "{subject.def} is startled by a drone",
    )

    def create_events(self):
        s = self.subject
        return [
            DroneEvent(subject=s),
            BecomeAngryEvent(subject=s),
            WhatWasThatEvent(subject=s),
            EmoteEvent(subject=s),
        ]


class ContemplateRock(PlotDevelopment):
    templates = (
        "{subject.def} contemplates {obj.indef}",
    )

    def create_events(self):
        s = self.subject
        return [
            PickUpEvent(subject=s, object=self.object),
            HoldEvent(subject=s, object=self.object),
            ContemplateEvent(subject=s, object=self.object),
            BecomeSadEvent(subject=s),
        ]


# - - - -


class Journey(PlotDevelopment):
    templates = (
        "{subject.def} travel to {obj.def}",
    )

    def create_events(self):
        return [
            TravelToEvent(subject=self.subject, object=self.object)
        ]


class EncounterNewSetting(PlotDevelopment):
    templates = (
        "{subject.def} encounter a new setting",  #, {setting.def}",
    )

    def create_events(self):
        prots = set(self.subject)
        snarker = random.extract(prots, filter=lambda x: not isinstance(x, TheOptimist))
        reader = random.extract(prots)
        e = []
        if snarker:
            e.append(EventSequence(
                BecomeSadEvent(subject=snarker),
                CommentOnPlaceEvent(subject=snarker),
            ))
            if reader:
                e.append(EventSequence(
                    TakeReadingsEvent(subject=reader),
                    ReadingsBanterEvent(subject=snarker),
                ))
        elif reader:
            e.append(TakeReadingsEvent(subject=reader))
        return e


class DreamSequence(PlotDevelopment):
    """purely proof-of-concept"""
    def create_events(self):
        from marysue.events import get_all_event_classes

        classes = get_all_event_classes()
        z = [random.choice(classes) for x in xrange(0, 20)]
        z = [cls(subject=random.choice(subjects),
                 object=random.choice(subjects)) for cls in z]

        return z

# - - - -


def all_plot_classes():
    return [
        c for c in globals().values() if c.__class__ == type and
                                         issubclass(c, Plot) and
                                         c != Plot
    ]


def get_plot_class(name):
    try:
        return globals()[name]
    except KeyError:
        for cls in all_plot_classes():
            print cls.__name__
        raise
