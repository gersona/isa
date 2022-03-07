#http://tenymalagasy.org/bins/contextLists?ctxt=math_arit&lang=mg
# https://github.com/moul/number-to-words
# add topic number converter in git branch
import sys

class NumberGroup():
    INDEX = None
    NAMES = []
    AND = "sy"

    def __init__(self, value: int):
        if self.INDEX is None:
            raise ValueError(self.__class__.__name__, " improperly configured: no INDEX provided")
        if len(self.NAMES) < 10:
            raise ValueError(self.__class__.__name__, " improperly configured: not enough NAMES provided")
        if value > 9:
            raise ValueError("`value` must be between 0 and 9")
        self.value = value
        self.current_result = self.NAMES[self.value]

    def render(self, past_result: str = "") -> str:
        result = ""
        if self.current_result:
            if past_result:
                result = past_result + " " + self.AND + " "
            result += self.current_result
        return result

class Ones(NumberGroup):
    INDEX = 0
    NAMES = (
        '', 'iray', 'roa', 'telo', 'efatra', 'dimy', 'enina', 'fito', 
        'valo', 'sivy'
    )

    def render(self, past_result: str = ""):
        return f"{self.NAMES[self.value]}"

class Tens(NumberGroup):
    INDEX = 1
    TEENS = (
        "", "iraika ambin' ny folo", "roambinifolo", "telo ambinifolo",
        "efatra ambin' ny folo", "dimy ambin' ny folo", "enina ambinifolo",
        "fahafitoambinifolo", "valo ambin' ny folo", "sivy ambin' ny folo"
    )
    NAMES = [
        '', 'folo', 'roapolo', 'telopolo', 'efapolo', 'dimampolo', 'enimpolo',
        'fitopolo', 'valopolo', 'sivifolo'
    ]
    AND = "amby"
    
    def render(self, past_result: str = "") -> str:
        if past_result and self.value == 1:  # teens: [11 -19]
            teens_index = Ones.NAMES.index(past_result)
            return self.TEENS[teens_index]
        return super().render(past_result)

class Hundreds(NumberGroup):
    INDEX = 2
    NAMES = (
        '', 'zato', 'roanjato', 'telonjato', 'efajato', 'dimanjato',
        'eninjato', 'fitonjato', 'valonjato', 'sivinjato'
    )
    def __init__(self, value: int):
        super().__init__(value)
        if value == 1:
            self.AND = "amby"


class NumberGroupFactory(object):
    ALL_CLASSES = (
        Ones, Tens, Hundreds
    )

    def __new__(cls, index):
        try:
            return [c for c in cls.ALL_CLASSES if c.INDEX == index][0]
        except IndexError:
            highest_number_supporter = "9"*len(cls.ALL_CLASSES)
            print(
                "Tsy mbola hainay ny manoratra ny isa ambonin'ny", highest_number_supporter
            )
            sys.exit(1)

class NumberRenderer(object):
    def __init__(self, value: int):
        self.value = value
    
    def render(self) -> str:
        if self.value == 0:
            return "aotra"

        _list = reversed([e for e in str(number)])
        result = ""
        for index, num in enumerate(_list):
            result = NumberGroupFactory(index)(int(num)).render(result)
        return result

if __name__ == '__main__':
    # python3 isa 890
    number = int(sys.argv[1])
    print(NumberRenderer(number).render())
