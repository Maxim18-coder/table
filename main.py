import argparse
from prettytable import PrettyTable


def read_csv_files(file_paths):
    data = []
    for path in file_paths:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            if not lines:
                continue
            headers = lines[0].split(',')
            for line in lines[1:]:
                values = line.split(',')
                row_dict = {}
                for header, value in zip(headers, values):
                    row_dict[header.strip()] = value.strip()
                data.append(row_dict)
    return data


def get_column_name(possible_names, headers):
    for name in possible_names:
        if name in headers:
            return name
    return None


def generate_payout_report(data):
    salary_keys = ['hourly_rate', 'rate', 'salary']

    all_headers = set()
    for row in data:
        all_headers.update(row.keys())

    salary_col = get_column_name(salary_keys, all_headers)

    table = PrettyTable()
    table.field_names = ['id', 'email', 'name', 'department', 'hours_worked', 'salary']

    for row in data:
        id_ = row.get('id') or ''
        email = row.get('email') or ''
        name = row.get('name') or ''
        department = row.get('department') or ''
        hours_worked_str = row.get('hours_worked') or ''
        hours_worked = float(hours_worked_str) if hours_worked_str else 0.0

        if salary_col and salary_col in row:
            salary_str = row[salary_col]
            try:
                salary_value = float(salary_str)
            except ValueError:
                salary_value = 0.0
        else:
            rate_str = None
            for key in ['hourly_rate', 'rate']:
                if key in row:
                    rate_str = row[key]
                    break
            rate_value = float(rate_str) if rate_str else 0.0
            salary_value = hours_worked * rate_value

        table.add_row([id_, email, name, department, hours_worked_str, f"{salary_value:.2f}"])

    print(table)


def main():
    parser = argparse.ArgumentParser(description='Генерация отчетов по сотрудникам.')
    parser.add_argument('files', metavar='F', type=str, nargs='+',
                        help='Пути к CSV файлам')
    parser.add_argument('--report', choices=['payout'], required=True,
                        help='Тип отчета (например payout)')

    args = parser.parse_args()

    data = read_csv_files(args.files)

    if args.report == 'payout':
        generate_payout_report(data)
    else:
        print(f"Отчёт типа {args.report} не реализован.")


if __name__ == '__main__':
    main()

