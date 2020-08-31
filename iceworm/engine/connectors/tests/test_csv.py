import csv
import io


def test_csv_stuff():
    buf = io.StringIO()

    fieldnames = ['id integer', 'name varchar(512)']
    writer = csv.writer(buf, quoting=csv.QUOTE_MINIMAL)
    writer.writerow(fieldnames)
    writer.writerow((1, 'Beans'))
    writer.writerow((2, 'Spam'))
    writer.writerow((3, 'Spam'))

    print(buf.getvalue())

    buf.seek(0)
    reader = csv.reader(buf)
    for row in reader:
        print(row)

    # fieldnames = ['first_name', 'last_name']
    # writer = csv.DictWriter(buf, fieldnames=fieldnames)
    # writer.writeheader()
    # writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
    # writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    # writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})
