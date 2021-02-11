<<<<<<< HEAD
import os
import json
import argparse
from datetime import datetime
import yaml

from demisto_sdk.commands.common.constants import UNRELEASE_HEADER, INTEGRATIONS_DIR, SCRIPTS_DIR, PLAYBOOKS_DIR, \
    REPORTS_DIR, DASHBOARDS_DIR, WIDGETS_DIR, INCIDENT_FIELDS_DIR, LAYOUTS_DIR, CLASSIFIERS_DIR, INDICATOR_TYPES_DIR
from demisto_sdk.commands.common.tools import server_version_compare, run_command, get_release_notes_file_path, \
    print_warning
from demisto_sdk.commands.validate.validate_manager import ValidateManager
from release_notes import LAYOUT_TYPE_TO_NAME


CHANGE_LOG_FORMAT = UNRELEASE_HEADER + '\n\n## [{version}] - {date}\n'

FILE_TYPE_DICT = {
    '.yml': yaml.safe_load,
    '.json': json.load,
}


def get_changed_content_entities(modified_files, added_files):
    # when renaming a file, it will appear as a tuple of (old path, new path) under modified_files
    return added_files.union([(file_path[1] if isinstance(file_path, tuple) else file_path)
                              for file_path in modified_files])


def get_file_data(file_path):
    extension = os.path.splitext(file_path)[1]
    if extension not in FILE_TYPE_DICT:
        return {}

    load_function = FILE_TYPE_DICT[extension]
    with open(file_path, 'r') as file_obj:
        data = load_function(file_obj)

    return data


def should_clear(file_path, current_server_version="0.0.0"):
    """
    scan folder and remove all references to release notes
    :param file_path: path of the yml/json file
    :param current_server_version: current server version
    """
    data = get_file_data(file_path)
    if not data:
        return False

    version = data.get('fromversion') or data.get('fromVersion')
    if version and server_version_compare(current_server_version, str(version)) < 0:
        print_warning('keeping release notes for ({})\nto be published on {} version release'.format(file_path,
                                                                                                     version))
        return False

    return True


def get_new_header(file_path):
    data = get_file_data(file_path)
    mapping = {
        # description
        INTEGRATIONS_DIR: ('Integration', data.get('description', '')),
        PLAYBOOKS_DIR: ('Playbook', data.get('description', '')),
        REPORTS_DIR: ('Report', data.get('description', '')),
        DASHBOARDS_DIR: ('Dashboard', data.get('description', '')),
        WIDGETS_DIR: ('Widget', data.get('description', '')),

        # comment
        SCRIPTS_DIR: ('Script', data.get('comment', '')),

        # custom
        LAYOUTS_DIR: ('Layout', '{} - {}'.format(data.get('typeId'), LAYOUT_TYPE_TO_NAME.get(data.get('kind', '')))),

        # should have RN when added
        INCIDENT_FIELDS_DIR: ('Incident Field', data.get('name', '')),
        CLASSIFIERS_DIR: ('Classifier', data.get('brandName', '')),
        # reputations.json has name at first layer
        INDICATOR_TYPES_DIR: ('Reputation', data.get('id', data.get('name', ''))),
    }

    for entity_dir in mapping:
        if entity_dir in file_path:
            entity_type, description = mapping[entity_dir]
            return '#### New {}\n{}'.format(entity_type, description)

    # should never get here
    return '#### New Content File'


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('version', help='Release version')
    arg_parser.add_argument('git_sha1', help='commit sha1 to compare changes with')
    arg_parser.add_argument('server_version', help='Server version')
    arg_parser.add_argument('-d', '--date', help='release date in the format %Y-%m-%d', required=False)
    args = arg_parser.parse_args()

    date = args.date if args.date else datetime.now().strftime('%Y-%m-%d')

    # get changed yaml/json files (filter only relevant changed files)
    validate_manager = ValidateManager()
    change_log = run_command('git diff --name-status {}'.format(args.git_sha1))
    modified_files, added_files, _, _, _ = validate_manager.filter_changed_files(change_log)

    for file_path in get_changed_content_entities(modified_files, added_files):
        if not should_clear(file_path, args.server_version):
            continue
        rn_path = get_release_notes_file_path(file_path)
        if os.path.isfile(rn_path):
            # if file exist, mark the current notes as release relevant
            with open(rn_path, 'r+') as rn_file:
                text = rn_file.read()
                rn_file.seek(0)
                text = text.replace(UNRELEASE_HEADER, CHANGE_LOG_FORMAT.format(version=args.version, date=date))
                rn_file.write(text)
        else:
            # if file doesn't exist, create it with new header
            with open(rn_path, 'w') as rn_file:
                text = CHANGE_LOG_FORMAT.format(version=args.version, date=date) + get_new_header(file_path)
                rn_file.write(text)
            run_command('git add {}'.format(rn_path))


if __name__ == '__main__':
    main()
=======
# remove all releaseNotes from files in: Itegrations, Playbooks, Reports and Scripts.
# Note: using yaml will destroy the file structures so filtering as regular text-file.\
# Note2: file must be run from root directory with 4 sub-directories: Integration, Playbook, Reports, Scripts
# Usage: python release_notes_clear.py
import os
import glob

def yml_remove_releaseNote_record(file_path):
    '''
    locate and remove release notes from a yaml file.
    :param file_path: path of the file
    :return: True if file was changed, otherwise False.
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    orig_size = len(lines)
    consider_multiline_notes = False
    new_lines = []
    for line in lines:
        if line.startswith('releaseNotes:'):
            # releaseNote title: ignore current line and consider following lines as part of it (multiline notes)
            consider_multiline_notes = True

        elif consider_multiline_notes:
            # not a releaseNote title (right after a releaseNote block (single or multi line)
            if not line[0].isspace():
                # regular line
                consider_multiline_notes = False
                new_lines.append(line)
            else:
                # line is part of a multiline releaseNote: ignore it
                pass
        else:
            # regular line
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.write(''.join(new_lines))

    return orig_size != len(new_lines)


def json_remove_releaseNote_record(file_path):
    '''
    locate and remove release notes from a json file.
    :param file_path: path of the file
    :return: True if file was changed, otherwise False.
    '''
    with open(file_path, 'r') as f:
        lines = f.readlines()

    orig_size = len(lines)
    consider_multiline_notes = False
    new_lines = []
    for line in lines:
        if line.strip().startswith('"releaseNotes"'):
            # releaseNote title: ignore current line and consider following lines as part of it (multiline notes)
            consider_multiline_notes = True

        elif consider_multiline_notes:
            # not a releaseNote title (right after a releaseNote block (single or multi line)
            if line.strip():
                if line.strip()[0] == '"': # regular line
                    consider_multiline_notes = False
                    new_lines.append(line)
                elif line.strip() == '}': # releaseNote was at end of dict
                    # needs to remove ',' from last line
                    idx = new_lines[-1].rfind(',')
                    new_lines[-1] = new_lines[-1][:idx] + new_lines[-1][idx+1:]
                    consider_multiline_notes = False
                    new_lines.append(line)
                    pass
            else:
                # line is part of a multiline releaseNote: ignore it
                pass
        else:
            # regular line
            new_lines.append(line)

    with open(file_path, 'w') as f:
        f.write(''.join(new_lines))

    return orig_size != len(new_lines)


FILE_EXTRACTER_DICT = {
    '*.yml' : yml_remove_releaseNote_record,
    '*.json' : json_remove_releaseNote_record,
}


def remove_releaseNotes_folder(folder_path, files_extension):
    '''
    scan folder and remove all references to release notes
    :param folder_path: path of the folder
    :param files_extension: type of file to look for (json or yml)
    '''
    scan_files = glob.glob(os.path.join(folder_path, files_extension))

    count = 0
    for path in scan_files:
        if FILE_EXTRACTER_DICT[files_extension](path):
            count += 1

    print '--> Changed %d out of %d files' % (count, len(scan_files), )


def main(root_dir):
    yml_folders_to_scan = ['Integrations', 'Playbooks', 'Scripts', 'TestPlaybooks'] # yml
    json_folders_to_scan = ['Reports', 'Misc', 'Dashboards', 'Widgets', 'Classifiers', 'Layouts', 'IncidentFields' ] # json

    for folder in yml_folders_to_scan:
        print 'Scanning directory: "%s"' % (folder, )
        remove_releaseNotes_folder(os.path.join(root_dir, folder), '*.yml')

    for folder in json_folders_to_scan:
        print 'Scanning directory: "%s"' % (folder, )
        remove_releaseNotes_folder(os.path.join(root_dir, folder), '*.json')


if __name__ == '__main__':
    main(os.path.dirname(__file__))
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
