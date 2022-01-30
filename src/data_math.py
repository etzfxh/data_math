#!/usr/bin/env python3

from collections import defaultdict
import random
import subprocess

MAX_NUM_TIMES_QUESTION_ASKED = 2
GREETING = 'Hallo Edda!'
COMPLIMENTS = [
    'Prima!',
    'Sehr gut!',
    'Gut gemacht!',
    'Sehr schön!',
    'Toll!']
CONDOLENCES = [
    'Leider nicht richtig.',
    'Versuchs nochmal.',
    'Knapp daneben.']

class Data(object):

    def __init__(self):
        # {problem: num_mistakes}
        self.mistakes = defaultdict(int)

    def get_new_problem(self):
        a = random.choice(range(1, 10))
        b = random.choice(range(1, 10))
        c = a * b
        return a, b, c

    def get_old_problem(self):
        if any(num_mistakes > 0 for num_mistakes in self.mistakes.values()):
            return sorted(self.mistakes.items(), key=lambda x: x[1])[-1][0]
        return self.get_new_problem()

    def speak(self, phrase):
        subprocess.run(f"echo '{phrase}' | espeak -vde", shell=True)

    def ask(self, is_new=True):
        '''
        Create a problem.
            Alternate between new problems (randomly created) and the most often made mistake.
        Format question and solution from the problem.
        Ask the question at most MAX_NUM_TIMES_QUESTION_ASKED times.
        If it is answered correctly, set its mistake count to zero.
        If it is not answered correctly (including the case where the solution was given), increase the mistake count by one.
        TODO: Consider time used to answer.
        '''
        problem = self.get_new_problem() if is_new else self.get_old_problem()
        a, b, c = problem
        question = f'Was ist {a} mal {b}?'
        solution = f'{a} mal {b} ist {c}.'
        self.speak(question)
        num_times_question_asked = 1
        answer = input('').strip()
        while (answer != str(c)) and (num_times_question_asked < MAX_NUM_TIMES_QUESTION_ASKED):
            if answer and (answer != '?'):
                self.mistakes[problem] += 1
                self.speak(random.choice(CONDOLENCES))
            elif answer == '?':
                self.speak(solution)
                # Maybe pause
                return
            self.speak(question)
            num_times_question_asked += 1
            answer = input('')
        if num_times_question_asked < MAX_NUM_TIMES_QUESTION_ASKED:
            self.speak(random.choice(COMPLIMENTS))
            self.mistakes[problem] = 0
        else:
            self.speak(solution)

    def run_training(self):
        self.speak(GREETING)
        while True:
            self.ask(is_new=True)
            self.ask(is_new=False)

if __name__ == '__main__':
    Data().run_training()
