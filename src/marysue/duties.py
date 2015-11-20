from marysue.objects import Object


class Duty(Object):
    pass


class RescueDuty(Duty):
    def __init__(self, object, **kwargs):
        name = 'rescue ' + object.name
        super(RescueDuty, self).__init__((name,), **kwargs)


class RetrieveDuty(Duty):
    def __init__(self, object, **kwargs):
        name = 'retrieve ' + object.definite
        super(RetrieveDuty, self).__init__((name,), **kwargs)
