import re


class OutputBin:
    def __init__(self, name):
        self.name = name
        self.holding = []

    def take_input_value(self, value):
        self.holding.append(value)

    def can_take_input(self):
        return True

    def set_give_directive_targets(self, lowdest, highdest):
        assert(False, "Output bins do not support give directives")

    def can_perform_give_directive(self, bots_and_bins):
        return False


class Bot:
    def __init__(self, name):
        self.name = name
        self.holding = []

        self.lowdest = None
        self.highdest = None

    def take_input_value(self, value):
        assert(len(self.holding)<2)
        self.holding.append(value)

    def can_take_input(self):
        return len(self.holding)<2

    def set_give_directive_targets(self, lowdest, highdest):
        self.lowdest = lowdest
        self.highdest = highdest

    def can_perform_give_directive(self, bots_and_bins):
        can_perform = ( len(self.holding)==2 and
                        (bots_and_bins[self.lowdest].can_take_input()) and
                        (bots_and_bins[self.highdest].can_take_input()) )
        return can_perform

    def perform_give_directive(self, bots_and_bins, oncompare = None):
        assert(len(self.holding)==2)
        if oncompare:
            oncompare(self.name, min(self.holding), max(self.holding))

        bots_and_bins[self.lowdest].take_input_value(min(self.holding))
        bots_and_bins[self.highdest].take_input_value(max(self.holding))

        self.holding=[]


def ensure_bot_or_bin_exists(bots_and_bins, name):
    if name not in bots_and_bins:
        if name.startswith('bot'):
            bots_and_bins[name] = Bot(name)
        elif name.startswith('output'):
            bots_and_bins[name] = OutputBin(name)
        else:
            assert(False, "Unknown kind of receiver object name")




match_value_move_re = re.compile('value ([0-9]+) goes to bot ([0-9]+)')

def match_value_move_and_update_bots(directive, bots_and_bins):
    match = match_value_move_re.match(directive)
    if not match:
        return False

    value = int(match.group(1))
    bot = 'bot ' + match.group(2)

    ensure_bot_or_bin_exists(bots_and_bins, bot)
    bots_and_bins[bot].take_input_value(value)

    return True


match_give_directive_re = re.compile('bot ([0-9]+) gives low to (bot|output) ([0-9]+) and high to (bot|output) ([0-9]+)')

def match_give_directive_and_update_bots(directive, bots_and_bins):
    match = match_give_directive_re.match(directive)
    if not match:
        return False

    frombot = 'bot ' + match.group(1)
    lowdest = match.group(2) + ' ' + match.group(3)
    highdest = match.group(4) + ' ' + match.group(5)

    ensure_bot_or_bin_exists(bots_and_bins, frombot)
    ensure_bot_or_bin_exists(bots_and_bins, lowdest)
    ensure_bot_or_bin_exists(bots_and_bins, highdest)

    bots_and_bins[frombot].set_give_directive_targets(lowdest, highdest)

    return True


robot_directives=[match_value_move_and_update_bots, match_give_directive_and_update_bots]


def create_bots_and_bins_from_directives(directives):
    bots_and_bins={}

    # parse the directive
    done = False
    for directive in directives:
        for directive_matcher in robot_directives:
            done = directive_matcher(directive, bots_and_bins)
            if done:
                break
        assert(done, "Encountered a directive that didn't match any known directives")

    return bots_and_bins


def perform_bots_step(bots_and_bins, oncompare=None):
    # find the first bot that can perform it's give step
    runnable_bot = None
    for bot in bots_and_bins.values():
        if bot.can_perform_give_directive(bots_and_bins):
            runnable_bot = bot
            break

    # if there's nothing less to run, report False
    if not runnable_bot:
        return False

    # otherwise run the bot
    runnable_bot.perform_give_directive(bots_and_bins, oncompare)
    return True


def day10_solver(directives):
    bots_and_bins = create_bots_and_bins_from_directives(directives)

    logoutput = ''
    def oncompare(name, low, high):
        nonlocal logoutput

        if low==17 and high==61:
            logoutput += name + ' compared ' + str(low) + ' with ' + str(high) + '\n'

    while perform_bots_step(bots_and_bins, oncompare):
        pass

    logoutput += '\n'
    product = 1
    for i in range(3):
        name = 'output '+str(i)
        logoutput += name + ' holds ' + str(bots_and_bins[name].holding) + '\n'
        product *= bots_and_bins[name].holding[0]

    logoutput += 'product = ' + str(product) + '\n'

    return logoutput


if __name__ == '__main__':
    with(open('input_10a.txt', 'r')) as infile:
        directives = infile.read().splitlines()

    print(day10_solver(directives))
