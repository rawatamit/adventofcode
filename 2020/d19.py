from io import StringIO
from collections import defaultdict
import re
from collections import deque
import copy


class Rule:
    def __init__(self, rule_id, definition, is_terminal=False) -> None:
        self.rule_id = rule_id
        self.definition = definition
        self.is_terminal = is_terminal


## The grammar in the example is left recursive most likely,
## a top-down parse will need to be clever to deal with these.
class Grammar:
    def __init__(self) -> None:
        self.rules = {}
    
    def add_rule(self, rule):
        self.rules[rule.rule_id] = rule
    
    def _parse(self, rule, s, cur_stack):
        return False
   
    def parse(self, s):
        cur_stack = defaultdict(int)
        cur_stack[0] = 1
        is_match = self._parse(self.rules[0], s, cur_stack)
        return is_match and s.read(1) == ''


def parse_rule(s):
    rule_id, definition = [x.strip() for x in s.split(':')]

    is_terminal = False
    if definition[0] == '"':
        is_terminal = True
        definition = definition[1:-1]
    else:
        definition = [[int(y) for y in x.split()]
                        for x in definition.split('|')]

    return Rule(int(rule_id), definition, is_terminal)


def parse_pda(rules, s, i, pda):
    if i >= len(s):
        return len(pda) == 0
    elif len(pda) == 0:
        return i == len(s)
    else:
        rule_id = pda.popleft()
        rule = rules[rule_id]

        if rule.is_terminal:
            return s[i] == rule.definition and parse_pda(rules, s, i+1, pda)
        else:
            for choice in rule.definition:
                new_pda = deque(choice) + pda
                if parse_pda(rules, s, i, new_pda): return True
            
            return False


def parse(rules, s):
    return parse_pda(rules, s, 0, deque([0]))


def main_pda():
    rules = {}
    strings = []

    with open('d19.txt') as fin:
        for line in fin:
            line = line.strip()
            if line and line[0].isdigit():
                rule = parse_rule(line)
                rules[rule.rule_id] = rule
            elif line:
                strings.append(line)
    
    count = sum(1 for s in strings if parse(rules, s))
    print(count)

    rules[8] = Rule(8, [[42], [42, 8]])
    rules[11] = Rule(11, [[42, 31], [42, 11, 31]])

    count = sum(1 for s in strings if parse(rules, s))
    print(count)


def generate_regex(rules, rule, depth=10):
    if depth == 0:
        return ''
    elif rule.is_terminal:
        return rule.definition
    else:
        or_regex = []
        for or_rule in rule.definition:
            part_regex = [generate_regex(rules, rules[rule_id], depth-1)
                          for rule_id in or_rule]
            or_regex.append(''.join(part_regex))
        return '('+ '|'.join(or_regex) + ')'


def is_match(regex, s):
    m = re.match(regex, s)
    return m is not None and len(m.group(0)) == len(s)


def main_regex():
    # a regex based solution
    rules = {}
    strings = []

    with open('d19.txt') as fin:
        for line in fin:
            line = line.strip()
            if line and line[0].isdigit():
                rule = parse_rule(line)
                rules[rule.rule_id] = rule
            elif line:
                strings.append(line)

    # part 1
    regex = generate_regex(rules, rules[0], depth=11)

    count = sum(1 for s in strings if is_match(regex, s))
    print(count)

    # part 2
    rules[8] = Rule(8, [[42], [42, 8]])
    rules[11] = Rule(11, [[42, 31], [42, 11, 31]])

    regex = generate_regex(rules, rules[0], depth=15)

    count = sum(1 for s in strings if is_match(regex, s))
    print(count)


#main_regex()
main_pda()
