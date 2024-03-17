'''
Personal Schedule Planner designed to be used at the University of Oregon.
This program will take into account when classes are offered (spring, fall, winter)
but will not take into account the specific time or days of the week the classes will be offered.
This will serve as a broad schedule over a couple years, rather than a specific schedule for the term,
as it can't be known what times classes are in future terms.

Classes will be imported from a csv file that has the name of the class and the term it is offered.
The classes can be any class, regardless of major, and  its recommended to add classes that pertain
to the desired major and other necessary classes needed to graduate. The program will be based off
the quota of 180 credits required to graduate, and will assume a 4 year plan. It also will make sure
each term has a maximum of 18 credits.

This will not factor in Summer term.
'''

import pandas as pd

QUOTA = 180
MAX_CREDS = 18

class Planner:
    '''Main class for schedule planner.'''
    def __init__(self, filename, start_year: int):
        '''
        Filename: csv file with classes, terms, credits
        start_year: first year of university, only last two digits (ex. 2020 -> 20)
        '''
        self.filename = filename
        self.start_year = start_year
        self.df = pd.read_csv(filename)

        if self.df.columns.tolist() != ['Class', 'Term', 'Credits']:
            raise ValueError('CSV file must have columns: Class, Term, Credits')
        
        self.classes = self.df['Class'].tolist() # Format is CLASS ### (ex. MATH 101)
        self.terms = self.df['Term'].apply(lambda x: x.split(', ')).tolist() # Terms are F (Fall), W (Winter), S (Spring)
        self.credits = self.df['Credits'].tolist()
        self.class_terms = dict(zip(self.classes, self.terms))
        self.class_credits = dict(zip(self.classes, self.credits))

    def add_class(self, class_name: str, terms: list, credits: int):
        '''Add class to the planner'''
        if class_name in self.classes:
            raise ValueError('Class already exists in the planner')
        for term in terms:
            if term not in ['F', 'W', 'S']:
                raise ValueError('Term must be F, W, or S')
        if credits <= 0:
            raise ValueError('Credits must be a positive integer')
        self.classes.append(class_name)
        self.terms.append(terms)
        self.credits.append(credits)
        self.class_terms[class_name] = terms
        self.class_credits[class_name] = credits
        self.df = pd.DataFrame({'Class': self.classes, 'Term': self.terms, 'Credits': self.credits})
    
    def remove_class(self, class_name: str):
        '''Remove class from the planner'''
        if class_name not in self.classes:
            raise ValueError('Class does not exist in the planner')
        index = self.classes.index(class_name)
        self.classes.pop(index)
        self.terms.pop(index)
        self.credits.pop(index)
        self.class_terms.pop(class_name)
        self.class_credits.pop(class_name)
        self.df = pd.DataFrame({'Class': self.classes, 'Term': self.terms, 'Credits': self.credits})

    def get_class_terms(self, class_name: str):
        '''Get the terms when the class is offered'''
        return self.class_terms[class_name]
    
    def get_class_credits(self, class_name: str):
        '''Get the credits of the class'''
        return self.class_credits[class_name]
    
    def create_schedule(self):
        '''Create a schedule based on classes, terms, credits'''
        if self.get_total_credits() < QUOTA:
            print(f'===============================================================')
            print(f'Warning: Total credits are less than 180 ({self.get_total_credits()}), schedule may be incomplete.')
            print(f'===============================================================')
        schedule = {}
        total_credits = 0
        class_terms_copy = self.class_terms.copy()
        years = [self.start_year, self.start_year + 1, self.start_year + 2, self.start_year + 3]
        for year in years:
            schedule[year] = {'F': {}, 'W': {}, 'S': {}}
            classes_added = []
            for class_name, terms in class_terms_copy.items():
                for term in terms:
                    if sum(schedule[year][term].values()) + self.get_class_credits(class_name) <= MAX_CREDS:
                        schedule[year][term][class_name] = self.get_class_credits(class_name)
                        total_credits += self.get_class_credits(class_name)
                        classes_added.append(class_name)
            for c in classes_added:
                print(f'{c} in {classes_added}')
                class_terms_copy.pop(c)
        if len(class_terms_copy) > 0:
            print(f'Warning: Not all classes could be added to the schedule. Remaining classes: {class_terms_copy.keys()}')

        return schedule
    
    def get_total_credits(self):
        '''Get the total credits of the schedule'''
        return sum(self.credits)
    
    def display_schedule(self, schedule: dict):
        '''Display the schedule'''
        for year, terms in schedule.items():
            print(f'Year {year}')
            for term, classes in terms.items():
                print(f'{term}: {classes}')
            print()

    def save_schedule(self, schedule: dict, filename: str):
        '''Save the schedule to a csv file'''
        df = pd.DataFrame(schedule)
        df.to_csv(filename, index=False)
    
    def __str__(self):
        return f'Planner based on: {self.filename}'
    
    def __repr__(self):
        return f'Planner({self.filename}, {self.start_year})'
    
def main():
    planner = Planner('B:\\VSCode\\personal projects\\schedule planner\\sample_classes.csv', 22)
    print(planner)
    planner.display_schedule(planner.create_schedule())

if __name__ == '__main__':
    main()