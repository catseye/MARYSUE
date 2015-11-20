import marysue.util as random
from marysue.ast import AST


# - - - -


class Event(AST):
    exciting = False
    new_para = False
    slots = (
        'subject', 'object',
        'object2',  # rarely used
    )

    @property
    def is_conjoinable(self):
        if not self.templates:
            return False
        if any([t[0] in ('"', "'") for t in self.templates]):
            return False
        return True


# - - - - mood modifier events


class MoodModifierEvent(Event):
    def __init__(self, subject, **kwargs):
        # this is just to debug where we might be constructing it with wrong args
        assert subject is not None
        super(MoodModifierEvent, self).__init__(subject=subject, **kwargs)

    def mood(self):
        raise NotImplementedError


class BecomeHappyEvent(MoodModifierEvent):
    templates = (
        '{subj.pronoun} became HAPPY',
    )

    def mood(self):
        return 'happy'


class BecomeSadEvent(MoodModifierEvent):
    templates = (
        '{subj.pronoun} became SAD',
    )

    def mood(self):
        return 'sad'


class BecomeAngryEvent(MoodModifierEvent):
    templates = (
        '{subj.pronoun} became ANGRY',
    )

    def mood(self):
        return 'angry'


class BecomeEmbarrassedEvent(MoodModifierEvent):
    templates = (
        '{subj.pronoun} became EMBARRASSED',
    )

    def mood(self):
        return 'embarrassed'


# - - - - duty acquisition events.  object is the duty acquired, subject is the character acquiring it


class AcquireDutyEvent(Event):
    templates = (
        '{subj.pronoun} acquired DUTY `{obj.name}`',
    )


class RelieveDutyEvent(Event):
    templates = (
        '{subj.pronoun} was released from DUTY `{obj.name}`',
    )


# - - - - actions and affect


class PickUpEvent(Event):
    templates = (
        '{subj.motion}{subj.pronoun} picked up {obj.pronoun} that {obj.was} nearby',
    )


class HoldEvent(Event):
    templates = (
        '{subj.pronoun} held {obj.pronoun} in {subj.possessive} hand',
        '{subj.motion}{subj.pronoun} lifted {obj.pronoun}< to eye level| into the light|>',
    )


class ContemplateEvent(Event):
    templates = (
        '"{obj.proximal} represents how I feel inside," {subj.pronoun} {subj.said} {subj.adverb}',
    )


class ApproachEvent(Event):
    templates = (
        '{subj.motion}{subj.pronoun} walked towards {obj.accusative}',
        '{subj.motion}{subj.pronoun} took two steps in {obj.possessive} direction, then stopped',
    )


class GestureAtEvent(Event):
    templates = (
        '{subj.motion}{subj.pronoun} <pointed|gestured> towards {obj.accusative}',
        '{subj.pronoun} moved {subj.her} {subj.yet} <arm|hand> in the direction of {obj.accusative}',
    )


class LookAtEvent(Event):
    templates = (
        '{subj.pronoun} looked at {obj.accusative}',
        '{subj.pronoun} glanced {subj.adverb} at {obj.accusative}',
        '{subj.pronoun} glared in the direction of {obj.accusative}',
    )


class LookAroundEvent(Event):
    templates = (
        '{subj.pronoun} looked around',
        '{subj.pronoun} surveyed the area<| with {subj.her} eyes>',
    )


class PunchPalmWithFistEvent(Event):
    # NOTUSED
    templates = (
        '{subj.pronoun} made a fist and punched {subj.his} other palm with {subj.his} fist',
    )


class RepeatForEmphasisEvent(Event):
    # NOTUSED
    templates = (
        '{subj.pronoun} did this <again|a second time>, for emphasis',
    )


class EmoteEvent(Event):
    templates = (
        '{subj.pronoun} {subj.emoted} {subj.adverb}',
    )


class CackleEvent(Event):
    templates = (
        '{subj.pronoun} cackled <evilly|wildly|maniacally|despicably|wickedly|hatefully|disdainfully>',
    )


class StateDutyEvent(Event):
    templates = (
        '"We have a duty to {subj.pick_duty.name}!" {subj.said} {subj.pronoun} {subj.adverb}',
    )


class GreetEvent(Event):
    templates = (
        '"Hello, {obj.def}," {subj.said} {subj.pronoun} {subj.adverb}',
        '"Hello, {obj.def}," {subj.said} {subj.pronoun} with an enigmatic twitch of {sub.his} <nose|mouth|ears>',
    )


class CharacterStaysHappyEvent(Event):
    templates = (
        'this was bad, but {subj.pronoun} didn`t let it <get {subj.accusative_pronoun} down|affect {subj.his} mood|cramp {subj.his} style|dampen {subj.his} cheer>',
        '{subj.pronoun} wasn`t going to let a little thing like this <get {subj.accusative_pronoun} down|affect {subj.his} mood|cramp {subj.his} style|dampen {subj.his} cheer>, though',
        '{subj.pronoun} gritted {subj.his} teeth and determined to stay <cheerful|upbeat|chipper|positive|optimistic>',
    )


# - - - - events for chekov's gun - - - -


class IntroduceItemEvent(Event):
    templates = (
        '{subj.pronoun} was cracking open <walnuts|pecans> with {obj.pronoun}',
        '{subj.pronoun} was <studiously|meticulously|intently> <polishing|cleaning|buffing> {obj.pronoun}',
    )


class AskAboutItemEvent(Event):
    templates = (
        '"{obj.distal} means a lot to you, doesn`t it?" asked {subj.pronoun}',
        '"{obj.distal}, it`s <kind of|pretty> special, isn`t it?" asked {subj.pronoun}',
    )


class ReplyAboutItemEvent(Event):
    templates = (
        '"It means a lot to all of us, {obj.def}," {subj.pronoun} {subj.said} {subj.adverb}',
        '"Space Fighters Command doesn`t entrust us with just any old thing, {obj.def}," {subj.pronoun} {subj.said} {subj.adverb}',
        '"It`s not the <sort|kind|type> of thing you can just order <on|off|from> Omnizon, {obj.def}," {subj.pronoun} {subj.said} {subj.adverb}',
    )


# - - - - events for cave-in plot - - - -


class RumblingSoundEvent(Event):
    templates = (
        'there was a rumbling sound',
    )


class WhatWasThatNoiseEvent(Event):
    templates = (
        '"What was that noise?" {subj.said} {subj.pronoun}',
        '"Did you hear something?" {subj.pronoun} {subj.said}',
    )


class CaveInEvent(Event):
    # FIXME subj.pronoun works badly here :/
    exciting = True
    templates = (
        'suddenly, {subj.def} caved in',
        'without warning, with a <tremendous|stupendous|overwhelming> <crash|boom|bang>, {subj.def} caved in',
        'too quickly for anyone to react, {subj.def} caved in',
    )


class StunnedEvent(Event):
    templates = (
        '{subj.pronoun} just stared, seemingly paralyzed',
        '{subj.pronoun} stood frozen like a deer in headlights',
    )


class BuriedUnderRubbleEvent(Event):
    templates = (
        '{subj.pronoun} was buried under rubble',
    )


class DigOutEvent(Event):
    templates = (
        '{subj.pronoun} helped dig {obj.pronoun} out from the rubble',
    )


# - - - - events for kidnapping plot - - - -


class AppearEvent(Event):
    exciting = True
    templates = (
        '<then|suddenly|all of a sudden>, out of <nowhere|thin air>, {subj.pronoun} appeared',
    )


class DisappearEvent(Event):
    templates = (
        'in a flash, {subj.pronoun} disappeared into thin air, taking {obj.pronoun} with {subj.accusative}',
    )


class NoticeAntagonistEvent(Event):
    templates = (
        '"<It`s |>YOU!" {subj.shouted} {subj.pronoun}',
        '"<It`s |>{obj.def}!" {subj.pronoun} {subj.shouted}',
    )


class AntagonistBanterEvent(Event):
    templates = (
        '"I have you now!" {subj.said} {subj.pronoun} {subj.withvoice}',
        '"What have we here!" {subj.said} {subj.pronoun} {subj.withvoice}',
        '"We meet again, <kiddies|chums|do-gooders>!" {subj.said} {subj.pronoun} {subj.withvoice}',
        '"So sorry to spoil your <little|> party, <kiddies|chums|do-gooders>!" {subj.said} {subj.pronoun} {subj.withvoice}',
    )


class AbductEvent(Event):
    templates = (
        '{subj.pronoun} <grabbed|snatched> {obj.pronoun} from behind',
    )


class WeMustFindThemEvent(Event):
    templates = (
        '"We must find out where {obj.pronoun} is being held!" {subj.said} {subj.pronoun} {subj.adverb}',
        '"We must find out where that villian has taken {obj.pronoun}!" {subj.said} {subj.pronoun} {subj.adverb}',
    )


class LocationHunchEvent(Event):
    templates = (
        '"I have a strong feeling {obj.pronoun} is in {object2.pronoun}," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class SetCourseEvent(Event):
    templates = (
        '"Set course for {object.pronoun}!," {subj.shouted} {subj.pronoun} {subj.adverb}',
    )


class WeMustGoToEvent(Event):
    templates = (
        '"Quickly!  We must make our way to {object.pronoun}!," {subj.shouted} {subj.pronoun} {subj.adverb}',
    )


class RescueEvent(Event):
    templates = (
        '{subj.pronoun} together broke the cage and pulled out {obj.def}',
    )


class BumpIntoForceFieldEvent(Event):
    templates = (
        'walking along, {subj.pronoun} <suddenly|unexpectedly|surprisedly> <smacked|whacked|bonked> {subj.his} head against an invisible force field',
    )


class MustRetraceStepsEvent(Event):
    templates = (
        '"There`s no way we can get through this we`ll have to find another way in!" {subj.said} {subj.pronoun} {subj.adverb}',
    )


# - - - - events for lost item plot - - - -


class CommentOnItemEvent(Event):
    # NOTUSED
    templates = (
        '"<This is|What> a <great|superb> {obj.name} this is, <isn`t it|don`t you think|don`t you agree>?" {subj.pronoun} {subj.said} {subj.adverb}',
    )


class TripEvent(Event):
    templates = (
        "<Just then|Suddenly|All of a sudden|Without warning>, {subj.pronoun} <tripped|stumbled|lost {subj.his} balance|stubbed {subj.his} toe|was distracted>",
    )


class DropEvent(Event):
    templates = (
        "{subj.pronoun} lost {subj.his} grip on {obj.pronoun}",
        "{obj.pronoun} slipped out of {subj.possessive} <grasp|hand|grip>",
    )


class LoseEvent(Event):
    templates = (
        "{subj.pronoun} tumbled and rolled away out of sight",
        "a <drone|Space Magpie> flew by and made off with {subj.pronoun}",
    )


class OopsEvent(Event):
    templates = (
        '"<Whoops|Oops|Oopsie-daisy|Whoopsy-daisy|Uh-oh|Drat>," {subj.said} {subj.pronoun} quietly',
        'a <sheepish|embarrassed|crestfallen|sour> look crept across {subj.possessive} face',
    )


class HunchEvent(Event):
    templates = (
        '{subj.pronoun} <suddenly|all of a sudden> had a <funny|strange|unusual|odd|> <hunch|inkling|intuition>',
    )


class LookBehindEvent(Event):
    templates = (
        '{subj.pronoun} looked behind the nearby {obj.name}',
    )


class FindEvent(Event):
    templates = (
        '{subj.pronoun} found {obj.pronoun}',
    )


# - - - - events for fight plot


class AttackEvent(Event):
    templates = (
        'suddenly, {subj.indef} attacked {obj.pronoun}',
        'suddenly, {obj.pronoun} {obj.was} attacked by {subj.indef}',
    )


class EncounterEvent(Event):
    templates = (
        'suddenly, {obj.pronoun} spotted {subj.indef} in the distance',
        'suddenly, {subj.indef} came around the corner',
    )


class GoonBanterEvent(Event):
    templates = (
        '"{obj.name}!" <hissed|mouthed|squeaked> {subj.def}',
        '"<Uh oh, |>looks like <we`ve got company|they`ve spotted us|they`ve found us>," {subj.said} {subj.def} {subj.adverb}',
    )


class GoonParlayEvent(Event):
    templates = (
        '"{subj.gibberish}!!!" shouted {subj.def} in {subj.his} <weird|strange> {subj.singular} language',
    )


class AfterBattleEvent(Event):
    templates = (
        'when the dust had <cleared|settled>, <stunned|dazed> {subj.name} <littered|were strewn across> the <battlefield|area>',
    )


class AfterBattleBanterEvent(Event):
    templates = (
        '"That was a <close one|close call>!" {subj.said} {subj.pronoun} {subj.adverb}',
    )


class ObserveAfterBattleEvent(Event):
    templates = (
        '"It looked like {obj.distal} had {object2.possessive} insignia on their <uniforms|jerseys|clothes|armor>," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class RemindReportEvent(Event):
    templates = (
        '"Remember to include that in the report when we get home."',
    )


class IfWeGetHomeEvent(Event):
    templates = (
        '"IF we get home," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class WarCryEvent(Event):
    templates = (
        '"{subj.war_cry}!!!" {subj.shouted} {subj.pronoun}',
    )


class UnsheathEvent(Event):
    templates = (
        '{subj.pronoun} drew {obj.pronoun} out of {subj.his} <belt|equipment bag|backpack>',
    )


class LiftWeaponEvent(Event):
    templates = (
        '{subj.pronoun} <lifted|heaved|raised> {obj.pronoun} <above|over> {subj.her} head',
    )


class BringDownWeaponEvent(Event):
    templates = (
        '{subj.pronoun} brought down {obj.pronoun} with a <mighty|tremendous|awesome> <force|movement|power>',
    )


class WeaponContactEvent(Event):
    templates = (
        '{subj.pronoun} made contact with {obj.pronoun} with a <mighty|tremendous|awesome> <thud|whack|impact>',
    )


class FlyAcrossEvent(Event):
    templates = (
        '{subj.pronoun} went flying across the room',
    )


class TryToGetBehindEvent(Event):
    templates = (
        '{subj.pronoun} <ran|sprinted> to the side, <looking to|to try to|trying to> attack {obj.pronoun} from <behind|the rear>',
    )


class RushIntoFrayEvent(Event):
    templates = (
        'unperturbed, {subj.pronoun} rushed back into the <fray|melee|fight>',
    )


# - - - - romantic tension events - - - -


class PullAsideEvent(Event):
    templates = (
        '{subj.motion}{subj.pronoun} <motioned|gestured to> {obj.accusative} to step <away|aside|back> from the others for a moment',
    )


class WantToTalkToYouEvent(Event):
    templates = (
        '"There`s <something|a thing> I <wanted|need> to <talk to you about|talk about|say to you>", {subj.pronoun} <began|{subj.said}> {subj.adverb}',
    )


class WhatIsItEvent(Event):
    templates = (
        '"<Yes|What is it>, {obj.def}?" asked {subj.pronoun}',
    )


class RecallPastEventEvent(Event):
    templates = (
        '"<Uh|Um|Well|You know>, about <that time|last night|the other day> in the <mess hall|engine room|loading bay>..." {subj.said} {subj.pronoun} {subj.adverb}',
    )


class SayNoMoreEvent(Event):
    templates = (
        '"Hush, {obj.def}, there`s no need, you know that," {subj.said} {subj.pronoun} {subj.adverb}',
        '"It`s all right, {obj.def}, you don`t need to say anything," {subj.said} {subj.pronoun} {subj.adverb}',
        '"Speak not of it, {obj.def}" {subj.said} {subj.pronoun} {subj.adverb}',
        '{subj.pronoun} held {subj.her} finger up to {obj.possessive} lips',
        '"Words are not necessary, {obj.def}" {subj.said} {subj.pronoun} {subj.adverb}',
    )


class BumpIntoAwkwardlyEvent(Event):
    templates = (
        '{subj.pronoun} wasn`t <looking|watching> where {sub.pronoun} was going and bumped into {obj.pronoun} in a most embarrassing fashion',
    )


class BlushEvent(Event):
    templates = (
        '{subj.pronoun} blushed a deep red',
        '{subj.pronoun} went beet red with blushing',
    )


class PreludeToKissEvent(Event):
    templates = (
        '"<Uh|Um|Well|You know>, ... there comes a time when..." {subj.said} {subj.pronoun} {subj.adverb}',
    )


class FidgetEvent(Event):
    templates = (
        '"<Uh|Um|Well|You know>, ..." {subj.said} {subj.pronoun} {subj.adverb}',
        '{subj.pronoun} put {subj.his} hand behind {subj.his} head',
        '{subj.pronoun} scratched {subj.his} <head|knee|neck>',
        '{subj.pronoun} looked away',
    )

class FacesCloseTogetherEvent(Event):
    new_para = True
    templates = (
        'The faces of {subj.definite} and {obj.definite} moved centimeters closer',
        'The faces of {obj.definite} and {subj.definite} moved centimeters closer',
        'Their faces inched closer and closer',
    )


class MushyStuffEvent(Event):
    templates = (
        '"{obj.def}, you are so exquisitely beautiful, like a jewel," {sub.said} {subj.pronoun}. "I must kiss you!"',
    )


class KissEvent(Event):
    exciting = True
    new_para = True
    templates = (
        '{subj.def} and {obj.def} kissed',
    )


class AndTheyKissedEvent(Event):
    exciting = True
    templates = (
        ('And they kissed' + (' and they kissed' * 20)),
    )


# - - - - events for drone "plot" - - - -


class DroneEvent(Event):
    templates = (
        '<Suddenly|From out of nowhere|Out of the blue>, a <courier|messenger|delivery|security|surveillance|cooking|cleaning> drone <whizzed past|buzzed by|flew close by> {subj.possessive} head',
    )


class WhatWasThatEvent(Event):
    templates = (
        '"What <in blazes|in Sam Hill|in the world|the devil|> was that?" {subj.said} {subj.pronoun} {subj.adverb}',
    )


# - - - - generic plot-related events - - - -


class KeepMovingEvent(Event):
    templates = (
        '"Let`s keep moving," {subj.pronoun} {subj.said} {subj.adverb}',
    )


class TurnCornerEvent(Event):
    templates = (
        '{subj.pronoun} <went around|turned> a corner',
    )


class PanicEvent(Event):
    templates = (
        '{subj.pronoun} {subj.shouted} "<OH NO|NOOO|Nooooooooooooo>!"',
        '"<OH NO|NOOO|Nooooooooooooo>!" {subj.shouted} {subj.pronoun} <{subj.adverb}|{subj.withvoice}>',
        '{subj.pronoun} <put|clapped> {subj.her} hands '
          '<on|to> <the sides of {subj.her} face|{subj.her} cheeks> in <disbelief|surprise|shock>',
        '{subj.possessive} mouth <opened|gaped|gawped> wide in <disbelief|surprise|shock>',
        '{subj.pronoun} made <motions|gestures> of <disbelief|surprise|shock> with {subj.her} <arms|hands>',
    )


class WasteNoTimeEvent(Event):
    templates = (
        '{subj.pronoun} wasted no time',
        '"There`s no time to lose!" {subj.pronoun} {subj.shouted}',
        '"We must <act quickly|hurry>!" {subj.pronoun} {subj.said}',
        '"Hurry!" {subj.pronoun} {subj.said}',
    )


class ThankEvent(Event):
    templates = (
        '"Thank you, {obj.def}," {subj.said} {subj.pronoun} {subj.adverb}',
        '"I would have been <lost|a goner|toast> without you, {obj.def}," {subj.said} {subj.pronoun} {subj.adverb}',
        '"I am <indebted|in debt> to you, {obj.def}," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class ReliefEvent(Event):
    templates = (
        '"<What|That`s> a relief!" {subj.shouted} {subj.pronoun}',
    )


# - - - - end-of-story events


class ComplimentActionEvent(Event):
    templates = (
        '"<That|there> was some <quick|top notch|ace> <thinking|action> <I saw|> from you today, {obj.def}!" {subj.said} {subj.pronoun} {subj.adverb}',
        '"<You displayed|I saw you display> some <quick|top notch|ace> <thinking|action> today, {obj.def}!" {subj.said} {subj.pronoun} {subj.adverb}',
    )


class OfferPromotionEvent(Event):
    templates = (
        '"I think I should promote you to {obj.next_rank}, {obj.def}!" {subj.said} {subj.pronoun} {subj.adverb}',
        '"How would you like a promotion to the rank of {obj.next_rank}, {obj.def}!" {subj.said} {subj.pronoun} {subj.adverb}',
    )


class OhYouEvent(Event):
    templates = (
        '"Oh, {obj.def}!" <{subj.said}|blushed> {subj.pronoun} {subj.adverb}',
        '"Oh, {obj.def}!" {subj.said} {subj.pronoun}, blushing fiercely like <a tiger|a bonfire>',
    )


class RefusePromotionEvent(Event):
    templates = (
        '"I`m too modest, I like being a {subj.rank} too!"',
        '"I`m not in this for rank, I do it out of love!"',
        '"it`s enough to know I`m fighting on the side of good!"',
    )


class ConvalesceEvent(Event):
    templates = (
        '"What an adventure that was!" exclaimed {subj.pronoun}',
        '"I could really go for a <curry|pizza|hamburger|hot dog|soda|parmo> <after that|right now>," {subj.said} {subj.pronoun} {subj.adverb}',
        '"I think we all learned a valuable lesson today," {subj.said} {subj.pronoun} {subj.adverb}',
        '"All in a day`s work for the Space Fighters!" {subj.said} {subj.pronoun} {subj.adverb}',
        '{subj.motion}{subj.pronoun} <slumped|flumped> down on the <couch|sofa|bean bag chair>',
    )


class RememberMacGuffinEvent(Event):
    templates = (
        '"Maybe next time you`ll be more careful with {object2.distal}, {obj.def}," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class AllLaughEvent(Event):
    templates = (
        "they all laughed",
        "everyone laughed",
    )


# - - - - travel events


class TravelToEvent(Event):
    templates = (
        '{subj.pronoun} travelled to {obj.pronoun}',
    )


class CommentOnPlaceEvent(Event):
    templates = (
        '"I don`t like the look of this place," {subj.said} {subj.pronoun} {subj.adverb}',
        '"This place gives me the <creeps|chills|willies>," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class TakeReadingsEvent(Event):
    templates = (
        '"Enviro <readings|measurements|metrics> look normal," {subj.said} {subj.pronoun}, <looking|peering|gazing> down at <the enviro probe app on {subj.his} hyper crystal|{subj.his} hyper crystal`s enviro probe app>',
        '{subj.motion}{subj.pronoun} <dialed up|opened up|started|launched> the enviro probe app on {subj.his} hyper crystal. "Enviro <readings|measurements|metrics> look normal," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class ReadingsBanterEvent(Event):
    templates = (
        '"<Yeah, normal|Sure, normal|Normal, yeah|Normal, sure|>... for a <PIT|DUMP|DISASTER AREA|TOXIC WASTE SITE>!!" {subj.said} {subj.pronoun} {subj.adverb}',
    )


class BlastOfHotAirEvent(Event):
    templates = (
        '{subj.pronoun} close {subj.his} eyes as a <blast|gust> of warm fetid air rushed through the passage',
    )


# - - - - misc


class OutOfEggsEvent(Event):
    templates = (
        '"I have just come back from the <kitchen|pantry> and it looks like we are <fresh|plum> out of <eggs|Space Sugar|nutri worms>," {subj.said} {subj.pronoun} {subj.adverb}',
    )


class GenericHyperCrystalUsageEvent(Event):
    templates = (
        '{subj.pronoun} was playing that new match three game on {subj.her} hyper crystal',
    )


# - - - - descriptions, not events - - - -


class PoseDescription(Event):
    templates = (
        '{subj.pronoun} {subj.was} leaning on {obj.pronoun}',
        '{subj.pronoun} {subj.was} standing near {obj.pronoun}',
        '{subj.pronoun} {subj.was} standing near {obj.pronoun}',
    )


class SettingDescription(Event):
    templates = (
        'all was quiet {subj.preposition} {subj.def}',
        '{subj.def} was a sight to behold',
        "{subj.def} was pretty much what you'd expect",
    )


class NearbyDescription(Event):
    # subject is the setting, so it joins up with SettingDescription
    templates = (
        '<Nearby|Not too far away|In the centre of the area> {obj.was} {obj.indef}',
        'there {obj.was} {obj.indef} off in the <corner|distance>',
        '{obj.indef} seemed to dominate the environment',
        '{obj.indef} gleamed in the {obj.location.light}',
    )


class GenericSettingDescription(Event):
    # subject is the setting, so it joins up with SettingDescription
    templates = (
        'a Space Mouse scurried by',
        'a few Space <Bees|Gnats|Mosquitoes> <flew|buzzed> around',
        'there seemed to be electricity in the air',
        'it was truly an unusual sight',
    )


class CharacterDescription(Event):
    is_conjoinable = False
    templates = (
        '{subj.pronoun} was {subj.stature}, with {subj.hair_length} {subj.hair_colour} hair and {subj.eye_colour} eyes',
    )


class CharacterFeaturesDescription(Event):
    templates = (
        '{subj.pronoun} had a {subj.feature_adj} {subj.feature}, the <sort|kind|type> you only see in old movies',
        '{subj.pronoun} had a {subj.feature_adj} {subj.feature}, the <sort|kind|type> you only see in Westerns',
        '{subj.pronoun} had a {subj.feature_adj} {subj.feature}, the <sort|kind|type> you only see in comic books',
        '{subj.pronoun} had a {subj.feature_adj} {subj.feature}, the <sort|kind|type> you only see in the Outer Colonies',
        '{subj.pronoun} had a {subj.feature_adj} {subj.feature} that {subj.she} <inherited|inherited from|got> from {subj.her} <mother|father><`s side|`s side of the family|>',
        '{subj.pronoun} had a {subj.feature_adj} {subj.feature} that the other kids <teased|made fun of> back when {subj.he} <was in school|was a kid>',
        '{subj.her} {subj.feature_adj} {subj.feature} complemented {subj.her} other features <well|strongly|nicely|perfectly|highly>',
    )


class CharacterReminder(Event):
    templates = (
        '{subj.pronoun} put {subj.his} hand up to {subj.his} {subj.feature_adj} {subj.feature}',
        '{subj.his} {subj.feature_adj} {subj.feature} seemed to <gleam|glow|shine> in the {subj.location.light}',
        '{subj.his} {subj.hair_length} {subj.hair_colour} hair seemed to <gleam|glow|shine> in the {subj.location.light}',
        'the {subj.location.light} of {subj.location.definite} cast highlights on {subj.his} {subj.hair_length} {subj.hair_colour} <hair|locks>',
        '{subj.his} {subj.feature_adj} {subj.feature} in profile cast a shadow against {subj.location.nearby_scenery.definite}',
        '{subj.his} {subj.feature_adj} {subj.feature} in profile threw a shadow on {subj.location.nearby_scenery.definite}',
    )


class TorsoCostumeDescription(Event):
    two_piece_templates = (
        '{subj.pronoun} {subj.was} {subj.wearing} {subj.torso_costume.indef} and {subj.legs_costume.indef}',
    )

    one_piece_templates = (
        '{subj.pronoun} {subj.was} {subj.wearing} {subj.torso_costume.indef}',
    )

    def render(self):
        if self.subject.legs_costume:
            template = random.choice(self.two_piece_templates)
        else:
            template = random.choice(self.one_piece_templates)
        return self.render_t(template)


class FeetCostumeDescription(Event):
    templates = (
        'on {subj.her} feet {subj.pronoun} wore {subj.feet_costume.indef}',
        '{subj.feet_costume.indef} <graced|were on> {subj.her} feet',
        '{subj.his} feet were shod <with|in> {subj.feet_costume.indef}',
        '{subj.feet_costume.def} that <were on {subj.his} feet|{subj.pronoun} had on> looked almost new',
    )


class TorsoCostumeReminder(Event):
    two_piece_templates = (
        '{subj.torso_costume.definite} {subj.pronoun} {subj.was} {subj.wearing} seemed to <gleam|glow|shine> in the {subj.location.light}',
    )

    one_piece_templates = (
        '{subj.torso_costume.definite} {subj.pronoun} {subj.was} {subj.wearing} seemed to <gleam|glow|shine> in the {subj.location.light}',
    )

    def render(self):
        if self.subject.legs_costume:
            template = random.choice(self.two_piece_templates)
        else:
            template = random.choice(self.one_piece_templates)
        return self.render_t(template)


class FeetCostumeReminder(Event):
    templates = (
        '{subj.feet_costume.definite} {subj.pronoun} {subj.was} {subj.wearing} seemed to <gleam|glow|shine> in the {subj.location.light}',
        '{subj.feet_costume.definite} on {subj.her} feet seemed to <gleam|glow|shine> in the {subj.location.light}',
    )


class BehindBarsDescription(Event):
    exciting = True
    new_para = True
    templates = (
        '{subj.pronoun} was there, locked in a cage',
    )


class GenericBattleDescription(Event):
    exciting = True
    new_para = True
    templates = (
        'a <fierce|intense|harrowing|epic> <battle|skirmish> <ensued|took place|began|had begun|commenced|started>',
    )


# - - - -


class ConjoinedEvent(Event):
    slots = (
        'subject', 'object', 'object2',  # MEH
        'event1', 'event2',
    )

    def render(self):
        return self.event1.render() + ", and " + self.event2.render()


# - - - -


def get_event_class(name):
    cls = globals().get(name)
    return cls


def get_all_event_classes():
    return [c for c in globals().values() if c.__class__ == type and issubclass(c, Event)]
