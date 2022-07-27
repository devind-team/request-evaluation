from os.path import join, exists
from settings import get_settings
from docxtpl import DocxTemplate
from datetime import date, timedelta


def create_report(counter: int, avg_load: float, max_load: float, site_name: str):
    template_word = DocxTemplate(join(get_settings().template_dir, 'report.docx'))
    template_word.render(
        {
            'date': f"{(date.today() - timedelta(days=1)).strftime('%d.%m.%Y')}",
            'counter': counter,
            'avg_load': avg_load,
            'max_load': max_load

        }
    )
    current_date = (date.today() - timedelta(days=1)).strftime('%d-%m-%Y')
    path_report = join(get_settings().static_dir, f"{current_date}-{site_name.replace('/', '').replace('https:', '')}.docx")
    template_word.save(path_report)
    return path_report
