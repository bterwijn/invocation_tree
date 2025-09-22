import re

class Regex_Set:

    def __init__(self, target_set=None):
        self.target_set = None
        self.compiled_pattern = None
        if target_set is not None:
            self.update_pattern(target_set)

    def update_pattern(self, target_set):
        if not target_set == self.target_set:
            self.target_set = target_set.copy()
            pattern = '^('
            sep = ''
            for target in self.target_set:
                target = target.strip()
                if target[:3] == 're:':
                    pattern += sep + '(' + target[3:] + ')'
                else:
                    pattern += sep + re.escape(target)
                sep = '|'
            pattern += ')$'
            self.compiled_pattern = re.compile(pattern)

    def match(self, s, target_set):
        self.update_pattern(target_set)
        return self.compiled_pattern.match(s) is not None

