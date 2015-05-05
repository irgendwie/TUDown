#!/usr/bin/python3
import tudown

user = ''
passwd = ''


path = "./"
sample_entry = {"id": "example",
                "url": "http://example.org/ss15",
                "files": [(r"regex_to_match", "folder_to_save_to")],
                "user": user,
                "passwd": passwd
                }

theo = {"id": "theo_skript",
                "url": "http://wwwmayr.informatik.tu-muenchen.de/lehre/2015SS/theo/",
                "files": [('2015-theo\.pdf', 'Skript'),
                          ('2015-\d{2}-\d{2}\.pdf', 'Skript')],
                "user": user,
                "passwd": passwd
        }

config_list = [sample_entry, theo]


def main(arg):
    if arg == "list":
        for item in config_list:
            print(item)
            return 0
    if arg == 'all':
        for item in config_list:
            tudown.main(item["url"], item["files"])
        return 0

    item = next((item for item in config_list if item["id"] == arg), None)
    if item:
        tudown.main(item["url"], item["files"])
        return 0
    else:
        print("config not found, \'list\' to list all")
        return -1


    # # +--------+
    # # | Skript |
    # # +--------+
    #
    # url = 'http://wwwmayr.informatik.tu-muenchen.de/lehre/2015SS/theo/'
    #
    # files = [
    #     ('2015-theo\.pdf', 'Skript'),
    #     ('2015-\d{2}-\d{2}\.pdf', 'Skript'),
    # ]
    #
    # tudown.main(url, files)
    #
    # # +-------+
    # # | Übung |
    # # +-------+
    #
    # url = 'http://wwwmayr.informatik.tu-muenchen.de/lehre/2015SS/theo/uebung/'
    #
    # files = [
    #     ('ue\d{2}\.pdf', 'Übungsblätter'),
    #     ('lo\d{2}_HA\.pdf', 'Lösungsblätter'),
    #     ('theo15zue\d{2}_druck\.pdf', 'Skript/ZÜ'),
    # ]
    #
    # tudown.main(url, files, user=user, passwd=passwd)


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Specify id to update, \'all\' to update all, \'list\' to list all configs")
        sys.exit(-1)
    else:
        main(sys.argv[1])
