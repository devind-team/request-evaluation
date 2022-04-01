from os.path import join
from settings import get_settings
from docxtpl import DocxTemplate
from datetime import date, timedelta

CURRENT_DATE = date.today() - timedelta(days=1)
PATH_REPORT = join(get_settings().static_dir, f'{CURRENT_DATE}.docx')


def create_report(counter, avg_load, max_load):
    template_word = DocxTemplate(join(get_settings().template_dir, 'report.docx'))
    template_word.render(
        {
            'date': f'{CURRENT_DATE.day}.{CURRENT_DATE.month}.{CURRENT_DATE.year}',
            'counter': counter,
            'avg_load': avg_load,
            'max_load': max_load

        }
    )
    template_word.save(PATH_REPORT)
    return PATH_REPORT
