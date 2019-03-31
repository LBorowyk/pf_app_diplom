from app.documentdata import documentData

class pdfDefinition:
    def __init__(self):
        self.defFontSize = 8
        self.definition = self.getPdfDefinition()
        print(self.definition)

    def getPdfDefinition(self):
        return {
            'content': self.getPdfContent(),
            'styles': self.getStyles(),
            'defaultStyle': self.getDefaultStyle(),
            'pageMargins': 30
        }

    def getPdfContent(self):
        return documentData(1).content

        # return [
        #     *(self.getCaption()),
        #     self.getVSpace(),
        #     *(self.getIntro()),
        #     self.getVSpace(),
        #     *(self.getQualification()),
        #     self.getVSpace(),
        #     *(self.getInfoQualification()),
        #     self.getPageBreak(),
        #     *(self.getInfoGained())
        # ]

    def getVSpace(self, lineCount=1):
        return [{'text':'\n'} for _ in range(lineCount)]
            
    def getPageBreak(self):
        return {'text': '', 'pageBreak': 'after'}

    def getUList(self, items):
        return {
            'table': {
                'widths': [5, 7, '*'],
                'body': list(map(lambda row: ['', {'text':'–', 'alignment': 'center'}, row], items))
            },
            'layout': 'noBordersAndPaddings'
        }
    
    def getTableRow(self, rowData):
        return list(map(lambda cell: {'text': cell}, rowData))

    def getText(self, textstr):
        return {
            'text': textstr
        }

    def getCaption(self):
        return [
            {'text': 'ДОДАТОК ДО ДИПЛОМА', 'style': 'caption'},
            {'text': 'DIPLOMA SUPPLEMENT', 'style': 'caption'},
            {'text': '\n'},
            {'text': '<<Серія документа>> № <<Номер документа>> <<Дата вручення>>/ <<Дата вручення англ>>', 'style': 'subcaption'},
            {'text': 'серія, реєстраційний номер та дата видачі диплома', 'style': 'subcaption'},
            {'text': 'series, registration number and date of issue of the diploma', 'style': 'subcaption'},
            {'text': '\n'},
            {'text': ' № <<Номер документа>> <<Дата закінчення навчального закладу>>/<<Дата вручення англ>>', 'style': 'subcaption'},
            {'text': 'реєстраційний номер та дата видачі додатка', 'style': 'subcaption'},
            {'text': 'registration number and date of issue of the supplement', 'style': 'subcaption'},
            {'text': '\n'},
            {'text': '(без диплома не дійсний)', 'style': 'subcaptionstrait'},
            {'text': '(not valid without diploma)', 'style': 'subcaptionstrait'},
            *(self.getVSpace(10))
        ]

    def getIntro(self):
        return [
            self.getHeader(1, 'ІНФОРМАЦІЯ ПРО ВИПУСКНИКА', 'INFORMATION ABOUT THE GRADUATE'),
            {
                'table': {
                    'widths': ['*', 10, '*'],
                    'body': [
                        [
                            self.getSubHeader('1.1', 'Прізвище', 'Family name(s)'),
                            '',
                            self.getSubHeader('1.2', 'Ім\'я та по батькові', 'Given name(s)')
                        ],
                        # [
                        #     *(self.getVSpace(3))
                        # ],
                        [
                            {'text': '<<Прізвище>>'},
                            '',
                            {'text': '<<Ім\'я>> <<По батькові>>'}
                        ],
                        [
                            {'text': '<<Прізвище англ.>>'},
                            '',
                            {'text': '<<Ім\'я англ.>>'}
                        ],
                        # [
                        #     *(self.getVSpace(3))
                        # ],
                        [
                            self.getSubHeader('1.3', 'Дата народження', 'Date of birth'),
                            '',
                            ''
                        ],
                        # [
                        #     *(self.getVSpace(3))
                        # ],
                        [
                            {'text': '<<Дата народження>> р.'},
                            '',
                            ''
                        ],
                        [
                            {'text': '<<Дата народження англ>>'},
                            '',
                            ''
                        ]
                    ]
                },
                'layout': 'noBordersAndPaddings'
            }
        ]
    
    def getQualification(self):
        return [
            self.getHeader('2', 'ІНФОРМАЦІЯ ПРО ЗДОБУТУ КВАЛІФІКАЦІЮ', 'INFORMATION ABOUT THE QUALIFICATION'),
            self.getSubHeader('2.1', 'Кваліфікація випускника: ступінь вищої освіти, спеціальність (за необхідності – спеціалізація, освітня програма, професійна кваліфікація)', 'Qualification: Degree, Program Subject Area (if necessary Study program, Educational program, Professional qualification)'),
            {'text': 'Ступінь вищої освіти -- <<ОКР>>. Спеціальність -- <<Спеціальність>>'},
            {'text': '<<ОКР англ.>>. Program Subject Area -- <<Спеціальність англ.>>'},
            self.getSubHeader('2.2', 'Галузь знань', 'Field of Study'),
            {'text': '<<Галузь знань>>'},
            {'text': '<<Галузь знань англ.>>'},
            self.getSubHeader('2.3', 'Найменування і статус навчального закладу (наукової установи), який (яка) виконував(ла) освітню програму та присвоїв(ла) кваліфікацію', 'Name and status of the higher education (research) institution delivered the study program and conferred the qualification'),
            {'text': 'Національний університет харчових технологій. Державної форми власності, сертифікат про акредитацію серія РД-IV № 1159252 від 27.11.2013р.'},
            {'text': 'National University of Food Technologies. State ownership. The certificate of accreditation Series RD-IV № 1159252 of 27.11.2013'},
            self.getSubHeader('2.4', 'Мова(и) навчання', 'Language(s) of instruction'),
            {'text': 'Українська'},
            {'text': 'Ukrainian'},            
        ]

    def getInfoQualification(self):
        return [
            self.getHeader('3', 'ІНФОРМАЦІЯ ПРО РІВЕНЬ КВАЛІФІКАЦІЇ ЗА НАЦІОНАЛЬНОЮ РАМКОЮ КВАЛІФІКАЦІЙ', 'INFORMATION ABOUT THE LEVEL OF THE QUALIFICATION'),
            self.getSubHeader('3.1', 'Рівень кваліфікації', 'Level of qualification'),
            {'text': 'Перший (бакалаврський) рівень вищої освіти відповідає 7 рівню Національної рамки кваліфікацій,  передбачає здатність особи вирішувати складні спеціалізовані задачі та практичні проблеми у певній галузі професійної діяльності або у процесі навчання, що передбачає застосування певних теорій та методів відповідних наук і характеризується комплексністю та невизначеністю умов.'},
            {'text': "The first (Bachelor's) level of higher education corresponds to level 7 of the National Qualifications Framework, provides the ability of a person to solve complex specialized problems and practical problems in a particular area of professional activity or in the process of study which provides for application of certain theories and methods of corresponding sciences and is characterized by complexity and uncertainty of the conditions."},
            self.getSubHeader('3.2', 'Офіційна тривалість програми', 'Official duration of programme'),
            {'text': '2 роки, заочна форма навчання (<<Всього кредитів>> кредитів ЄКТС)'},
            {'text': '2 years, part-time form of studies (<<Всього кредитів>> credits ECTS)'},
            self.getSubHeader('3.3', 'Вимоги до вступу', 'Admission requirements(s)'),
            {'text': 'Освітньо-кваліфікаційний рівень молодшого спеціаліста, на основі результатів фахових вступних випробувань'},
            {'text': 'Education and qualification level of a Junior Specialist on the basis of admission tests in profession '}
        ]

    def getInfoGained(self):
        return [
            self.getHeader('4', 'ІНФОРМАЦІЯ ПРО ЗМІСТ ТА РЕЗУЛЬТАТИ НАВЧАННЯ', 'INFORMATION ABOUT THE CONTENTS AND OUTCOMES GAINED'),
            *(self.getModeOfStudy()),
            *(self.getProgrammeRequirements()),

        ]

    def getModeOfStudy(self):
        return [
            self.getSubHeader('4.1', 'Форма навчання', 'Mode of study'),
            self.getText('Заочна / Part-time')
        ]

    def getProgrammeRequirements(self):
        return [
            self.getSubHeader('4.2', 'Вимоги освітньої програми та результати навчання за нею', 'Programme requirements'),
            {'text': 'Студент повинен виконати програму підготовки (<<Всього кредитів>> кредитів ЄКТС) згідно навчального плану, який включає:'},
            self.getUList(['теоретичне навчання (цикли гуманітарних та соціально-економічних дисциплін (<<Кредитів гуманітарних>> кредитів ЄКТС), природничо-науковох дисциплін (<<Кредитів природничих>> кредитів ЄКТС), цикл професійної і практичної підготовку (<<Кредитів професійної підготовки>> кредитів ЄКТС), цикл дисциплін самостійного вибору навчального закладу (<<Кредитів вибору НЗ>> кредитів ЄКТС), цикл дисциплін вільного вибору студентів (<<Кредитів вибору студента>> кредитів ЄКТС) у вигляді аудиторних занять (лекційні, семінарські, лабораторні і практичні заняття) і самостійної роботи;',
            'виконання курсових робіт і проектів (<<Кредитів курсові>> кредитів ЄКТС);',
            'проходження переддипломної практики (<<Тижнів практики>> тижні, <<Кредитів практики>> кредити ЄКТС);',
            'виконання дипломного проекту (<<Кредитів диплом>> кредитів ЄКТС).']),
            self.getText('Кредити студенту зараховуються у випадку успішного (критерії оцінювання наведені в п.4.4) складання письмових (усних) заліків або екзаменів з навчальних дисциплін, захисту курсових робіт, захисту звітів з практик, проходження підсумкової атестації.'),
            self.getVSpace(1),
            self.getText('Learner must satisfy the programme requirements in the Programme Specification(<<Всього кредитів>> ECTS credits), which includes:'),
            self.getUList(['theoretical study in humanities and social-economic subjects (<<Кредитів гуманітарних>> ECTS credits), natural-sciences subjects (<<Кредитів природничих>> ECTS credits), professional and practical studies (<<Кредитів професійної підготовки>> ECTS credits), subjects selected by the university (<<Кредитів вибору НЗ>> ECTS credits), subjects selected by students(<<Кредитів вибору студента> ECTS credits) through class activities (lectures, seminars and practicals) and independent work;',
            'term papers and projects (<<Кредитів курсові>> ECTS credits);',
            'pre-diploma training (<<Тижнів практики>> weeks, <<Кредитів практики>> ECTS credits);',
            'graduate project (<<Кредитів диплом>> ECTS credits).']),
            self.getText('Credits are assigned to the student when he/she successfully (see Grading scheme in 4.4) passes written (or oral) tests and examinations in subjects, defends course papers, reports results of his/her practical training, passes final examinations.'),
            self.getVSpace(),
            self.getText('Набуті компетентності:'),
            self.getText('Знання і розуміння:'),
            
        ]

    def getStyles(self):
        return {
            'caption': {
                'fontSize': self.defFontSize + 2,
                'color': 'darkblue',
                'alignment': 'center',
                'bold': True
            },
            'header': {
                'fontSize': self.defFontSize,
                'color': 'darkblue',
                'bold': True,
                'alignment': 'justify'
            },
            'subcaption': {
                'fontSize': self.defFontSize,
                'color': 'darkblue',
                'bold': True,
                'alignment': 'center',
            },
            'subcaptionstrait': {
                'fontSize': self.defFontSize,
                'color': 'darkblue',
                'alignment': 'center',
            },
            'subHeader': {
                'fontSize': self.defFontSize,
                'bold': True,
                'alignment': 'justify'
            }
        }

    def getDefaultStyle(self):
        return {
            'fontSize': self.defFontSize,
            'alignment': 'justify',
        }

    def getHeaderElement(self, index, ua_str, en_str, style):
        return {
            'table': {
                'widths': ['*'],
                # 'headerRows': 1,
                'body': [
                    [{
                        'text': f'{index}. {ua_str}',
                        'style': style,
                        'border': [False, False, False, True]
                    }],
                    [{
                        'text': en_str,
                        'style': style,
                        'border': [False, True, False, False]
                    }],
                ]
            },
            'layout': f'{style}Line'
        }

    def getHeader(self, index, ua_str, en_str):
        return self.getHeaderElement(index, ua_str, en_str, 'header')

    def getSubHeader(self, index, ua_str, en_str):
        return self.getHeaderElement(index, ua_str, en_str, 'subHeader')
    
