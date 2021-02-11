<<<<<<< HEAD
from __future__ import print_function
import os
import re
import sys
import abc
import json
import datetime
import argparse
import requests
import yaml

from demisto_sdk.commands.common.constants import INTEGRATIONS_DIR, SCRIPTS_DIR, PLAYBOOKS_DIR, REPORTS_DIR, \
    DASHBOARDS_DIR, WIDGETS_DIR, INCIDENT_FIELDS_DIR, LAYOUTS_DIR, CLASSIFIERS_DIR, INDICATOR_TYPES_DIR
from demisto_sdk.commands.common.tools import print_error, print_warning, get_last_release_version, \
    filter_packagify_changes, is_file_path_in_pack, \
    run_command, server_version_compare, old_get_release_notes_file_path, old_get_latest_release_notes_text, get_remote_file
from demisto_sdk.commands.validate.validate_manager import ValidateManager

CONTENT_LIB_PATH = "./"

NEXT_VERSION = "5.5.0"
NEW_RN = "New"
MODIFIED_RN = "Improved"
IGNORE_RN = '-'

CONTENT_FILE_SUFFIXES = [
    ".yml",
    ".yaml",
    ".json"
]
=======
import abc
import datetime
import json
import sys
import yaml

from Tests.test_utils import print_error

contentLibPath = "./"
limitedVersion = False


NEW_RN = "New"
MODIFIED_RN = "Improved"
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

LAYOUT_TYPE_TO_NAME = {
    "details": "Summary",
    "edit": "New/Edit",
    "close": "Close",
<<<<<<< HEAD
    "quickView": "Quick View",
    "indicatorsDetails": "Indicator Details",
    "mobile": "Mobile",
}

RELEASE_NOTES_ORDER = [INTEGRATIONS_DIR, SCRIPTS_DIR, PLAYBOOKS_DIR, REPORTS_DIR,
                       DASHBOARDS_DIR, WIDGETS_DIR, INCIDENT_FIELDS_DIR, LAYOUTS_DIR,
                       CLASSIFIERS_DIR, INDICATOR_TYPES_DIR]


def add_dot(text):
    if not text or len(text) < 2:
        return ''

    text = text.rstrip().replace('```', '***').replace('`', '*')

    if '\n' in text:
        # multi-record release notes
        record_regex = re.compile(r'^((?: {2})- .*\.)|( {4}- \*{3}[\w-]*\*{3})$')
        formatted_text = []
        for line in text.split('\n'):
            if not line.strip():
                continue
            if record_regex.match(line):
                formatted_text.append(line)
            else:
                line = line.strip(' -.')
                if line.startswith('***') and line.endswith('***'):
                    formatted_text.append('    - {}'.format(line))
                else:
                    formatted_text.append('  - {}.'.format(line))

        return '\n'.join(formatted_text)

    # single record release notes
    text = text[0].upper() + text[1:]
    return text if text.endswith('.') else text + '.'


def release_notes_item(header, body):
    return '- __{}__  \n{}\n'.format(header, add_dot(body))


class Content(object):  # pylint: disable=useless-object-inheritance
=======
}

INTEGRATIONS_DIR = "Integrations"
SCRIPTS_DIR = "Scripts"
PLAYBOOKS_DIR = "Playbooks"
REPORTS_DIR = "Reports"
DASHBOARDS_DIR = "Dashboards"
WIDGETS_DIR = "Widgets"
INCIDENT_FIELDS_DIR = "IncidentFields"
LAYOUTS_DIR = "Layouts"
CLASSIFIERS_DIR = "Classifiers"
REPUTATIONS_DIR = "Misc"

RELEASE_NOTES_ORDER = [INTEGRATIONS_DIR, SCRIPTS_DIR, PLAYBOOKS_DIR, REPORTS_DIR,
                       DASHBOARDS_DIR, WIDGETS_DIR, INCIDENT_FIELDS_DIR, LAYOUTS_DIR,
                       CLASSIFIERS_DIR, REPUTATIONS_DIR]


def add_dot(text):
    if text.endswith('.'):
        return text
    return text + '.'


def release_notes_item(header, body):
    return '- __' + header + '__\n' + add_dot(body) + '\n'


class Content:
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.modified_store = []  # holds modified file paths
        self.added_store = []  # holds added file paths
        self.deleted_store = []  # holds deleted file paths
        self.show_secondary_header = True
<<<<<<< HEAD
        self.is_missing_release_notes = False
=======
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

    def add(self, change_type, data):
        if change_type == "M":
            self.modified_store.append(data)
        elif change_type == "A":
            self.added_store.append(data)
        elif change_type == "D":
            self.deleted_store.append(data)
        else:
<<<<<<< HEAD
            print("Unknown change type " + change_type)
=======
            print "Unknown change type " + change_type
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

    @abc.abstractmethod
    def get_header(self):
        return

<<<<<<< HEAD
    @classmethod
    def get_release_notes(cls, file_path, data):  # pylint: disable=unused-argument
        """
        Return the release notes relevant to the added yml file.

        :param file_path: yml/json (or package yml)
        :param data: object data
        :return: raw release notes or None in case of an error.
        """
        release_note_path = old_get_release_notes_file_path(file_path)

        return old_get_latest_release_notes_text(release_note_path)

    @abc.abstractmethod
    def added_release_notes(self, file_path, data):
        """
        Return the release notes relevant to the added yml file.

        :param file_path: yml/json added (or package yml)
        :param data: object data
        :return: raw release notes or None in case of an error.
        """
        return self.get_release_notes(file_path, data)

    def modified_release_notes(self, file_path, data):
        """
        Return the release notes relevant to the modified yml/json file (or modified package yml).

        :param file_path: yml/json (or package yml)
        :param data: yml data
        :return: raw release notes or None in case of an error.
        """
        release_note = self.get_release_notes(file_path, data)

        if release_note and release_note.strip() == IGNORE_RN:
            release_note = ''

        return release_note
=======
    @abc.abstractmethod
    def added_release_notes(self, data):
        return

    @abc.abstractmethod
    def modified_release_notes(self, data):
        return
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

    @abc.abstractmethod
    def load_data(self, data):
        return

    # create a release notes section for store (add or modified) - return None if found missing release notes
<<<<<<< HEAD
    def release_notes_section(self, store, title_prefix, current_server_version):
        res = ""
        beta_rn_paths = list()
        if store:
            new_str = ""
            new_count = 0
            for path in store:
                with open(path, 'r') as file_obj:
                    raw_content = file_obj.read()
                    cnt = self.load_data(raw_content)

                    from_version = cnt.get("fromversion") or cnt.get("fromVersion")
                    to_version = cnt.get("toversion") or cnt.get("toVersion")
                    if from_version is not None and server_version_compare(current_server_version, from_version) < 0:
                        print(f'{path}: Skipped because from version: {from_version}'
                              f' is greater than current server version: {current_server_version}')
                        beta_rn_paths.append(path)
                        print(f"{path} has added to beta release notes")
                        continue
                    if to_version is not None and server_version_compare(to_version, current_server_version) < 0:
                        print(f'{path}: Skipped because of to version" {to_version}'
                              f' is smaller: than current server version: {current_server_version}')
                        continue
                    if title_prefix == NEW_RN:
                        ans = self.added_release_notes(path, cnt)
                    elif title_prefix == MODIFIED_RN:
                        ans = self.modified_release_notes(path, cnt)
                    else:
                        # should never get here
                        print_error('Error:\n Unknown release notes type {}'.format(title_prefix))
                        return None

                    if ans is None:
                        print_error("Error:\n[{}] is missing releaseNotes entry, Please add it under {}".format(
                            path, old_get_release_notes_file_path(path)))
                        self.is_missing_release_notes = True
                    elif ans:
                        new_count += 1
                        new_str += ans

            if new_str:
=======
    def release_notes_section(self, store, title_prefix):
        res = ""
        missing_rn = False
        if len(store) > 0:
            new_str = ""
            new_count = 0
            for path in store:
                with open(path, 'r') as f:
                    print " - adding release notes (%s) for file - [%s]... " % (path, title_prefix),
                    raw_content = f.read()
                    cnt = self.load_data(raw_content)

                    if title_prefix == NEW_RN:
                        ans = self.added_release_notes(cnt)
                    elif title_prefix == MODIFIED_RN:
                        ans = self.modified_release_notes(cnt)
                    else:
                        # should never get here
                        print_error("Error:\n Unknown release notes type" % (title_prefix,))
                        return None

                    if ans is None:
                        print_error("Error:\n[%s] is missing releaseNotes/description entry" % (path,))
                        missing_rn = True
                    elif ans:
                        new_count += 1
                        new_str += ans
                        print "Success"
                    else:
                        print "Skipped"

            if len(new_str) > 0:
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
                if self.show_secondary_header:
                    count_str = ""
                    if new_count > 1:
                        count_str = " " + str(new_count)

                    res = "\n#### %s %s %s\n" % (count_str, title_prefix, self.get_header())
                res += new_str
<<<<<<< HEAD
        print("Collected {} beta notes".format(len(beta_rn_paths)))
        return res, beta_rn_paths

    def generate_release_notes(self, current_server_version):
        res = ""
        beta_res = ""
        if len(self.modified_store) + len(self.deleted_store) + len(self.added_store) > 0:
            print("starting {} RN".format(self.get_header()))

            # Added files
            add_rn, add_beta_paths = self.release_notes_section(self.added_store, NEW_RN, current_server_version,)
            # Modified files
            modified_rn, mod_beta_paths = self.release_notes_section(self.modified_store, MODIFIED_RN,
                                                                     current_server_version)
            add_beta_res, _ = self.release_notes_section(add_beta_paths, NEW_RN, NEXT_VERSION)
            mod_beta_res, _ = self.release_notes_section(mod_beta_paths, MODIFIED_RN, NEXT_VERSION)

            section_body = add_rn + modified_rn
            beta_section_body = add_beta_res + mod_beta_res
            # Deleted files
            if self.deleted_store:
                section_body += "\n##### Removed {}\n".format(self.get_header())
                for name in self.deleted_store:
                    print(' - adding release notes (Removed) for - [{}]'.format(name), end='')
                    section_body += "- __" + os.path.splitext(os.path.basename(name))[0] + "__\n"
                    print("Success")

            if section_body:
                res = "### {}\n".format(self.get_header())
                res += section_body
                beta_res = "### {}\n".format(self.get_header())
                beta_res += beta_section_body

        return res, beta_res
=======

        if missing_rn:
            return None

        return res

    def generate_release_notes(self):
        res = ""

        if len(self.modified_store) + len(self.deleted_store) + len(self.added_store) > 0:
            print "starting %s RN" % (self.get_header(),)

            # Added files
            add_rn = self.release_notes_section(self.added_store, NEW_RN)

            # Modified files
            modified_rn = self.release_notes_section(self.modified_store, MODIFIED_RN)

            if add_rn is None or modified_rn is None:
                return None

            section_body = add_rn + modified_rn

            # Deleted files
            if len(self.deleted_store) > 0:
                section_body += "\n##### Removed " + self.get_header() + "\n"
                for name in self.deleted_store:
                    print " - adding release notes (Removed) for - [%s]" % (name,),
                    section_body += "- __" + name + "__\n"
                    print "Success"

            if len(section_body) > 0:
                res = "### " + self.get_header() + "\n"
                res += section_body

        return res
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class ScriptContent(Content):
    def load_data(self, data):
        return yaml.safe_load(data)

    def get_header(self):
        return "Scripts"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        return release_notes_item(data["name"], data["comment"])

    def modified_release_notes(self, file_path, data):
        release_note = super(ScriptContent, self).modified_release_notes(file_path, data)

        if release_note:
            return release_notes_item(data["name"], release_note)

        # error or ignored release_note
        return release_note
=======
    def added_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) > 0 and rn == "-":
            return ""
        return release_notes_item(cnt["name"], cnt["comment"])

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = release_notes_item(cnt["name"], rn)
        return res


Content.register(ScriptContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class PlaybookContent(Content):
    def load_data(self, data):
        return yaml.safe_load(data)

    def get_header(self):
        return "Playbooks"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        return release_notes_item(data["name"], data['description'])

    def modified_release_notes(self, file_path, data):
        release_note = super(PlaybookContent, self).modified_release_notes(file_path, data)

        if release_note:
            return release_notes_item(data["name"], release_note)

        # error or ignored release_note
        return release_note
=======
    def added_release_notes(self, cnt):
        rn = cnt.get("description")
        if not rn:
            return None
        if rn == "-":
            return ""

        return release_notes_item(cnt["name"], rn)

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = release_notes_item(cnt["name"], rn)
        return res


Content.register(PlaybookContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class ReportContent(Content):
    def load_data(self, data):
        return json.loads(data)

    def get_header(self):
        return "Reports"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        return release_notes_item(data["name"], data["description"])

    def modified_release_notes(self, file_path, data):
        release_note = super(ReportContent, self).modified_release_notes(file_path, data)

        if release_note:
            return release_notes_item(data["name"], release_note)

        # error or ignored release_note
        return release_note
=======
    def added_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) > 0 and rn == "-":
            return ""
        return release_notes_item(cnt["name"], cnt["description"])

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = release_notes_item(cnt["name"], rn)
        return res


Content.register(ReportContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class DashboardContent(Content):
    def load_data(self, data):
        return json.loads(data)

    def get_header(self):
        return "Dashboards"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        return release_notes_item(data["name"], data["description"])

    def modified_release_notes(self, file_path, data):
        release_note = super(DashboardContent, self).modified_release_notes(file_path, data)

        if release_note:
            return release_notes_item(data["name"], release_note)

        # error or ignored release_note
        return release_note
=======
    def added_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) > 0 and rn == "-":
            return ""

        return release_notes_item(cnt["name"], cnt["description"])

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = release_notes_item(cnt["name"], rn)
        return res


Content.register(DashboardContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class WidgetContent(Content):
    def load_data(self, data):
        return json.loads(data)

    def get_header(self):
        return "Widgets"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        return release_notes_item(data["name"], data["description"])

    def modified_release_notes(self, file_path, data):
        release_note = super(WidgetContent, self).modified_release_notes(file_path, data)

        if release_note:
            return release_notes_item(data["name"], release_note)

        # error or ignored release_note
        return release_note


class IncidentFieldContent(Content):
=======
    def added_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) > 0 and rn == "-":
            return ""

        return release_notes_item(cnt["name"], cnt["description"])

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = release_notes_item(cnt["name"], rn)
        return res


Content.register(WidgetContent)


class IncidentFieldContent(Content):

>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
    def __init__(self):
        super(IncidentFieldContent, self).__init__()
        self.show_secondary_header = False

    def load_data(self, data):
        return json.loads(data)

    def get_header(self):
        return "Incident Fields"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        if data.get('description'):
            return release_notes_item(data['name'], data['description'])

        # using the 'modified' function instead of 'added' function to handle ignored RN
        release_note = super(IncidentFieldContent, self).modified_release_notes(file_path, data)

        if release_note:
            return release_notes_item(data['name'], release_note)

        # error or ignored release_note
        return release_note

    def modified_release_notes(self, file_path, data):
        release_note = super(IncidentFieldContent, self).modified_release_notes(file_path, data)

        if release_note:
            return add_dot(release_note) + "\n"

        # error or ignored release_note
        return release_note
=======
    def added_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None

        return add_dot(rn) + "\n"

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = add_dot(rn) + "\n"
        return res


Content.register(IncidentFieldContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class LayoutContent(Content):
    def load_data(self, data):
        return json.loads(data)

    def get_header(self):
<<<<<<< HEAD
        return "Layouts"

    def get_release_notes(self, file_path, data):
        release_note = super(LayoutContent, self).get_release_notes(file_path, data)
        if not release_note:
            return release_note

        layout_kind = LAYOUT_TYPE_TO_NAME.get(data.get("kind", ""))
        if not layout_kind:
            print_error('Invalid layout kind {}'.format(data.get("kind", "")))
            return None

        layout_type = data.get("typeId")
        if not layout_type:
            print_error("Invalid layout kind {}".format(layout_type))
            return None

        return release_notes_item('{} - {}'.format(layout_type, layout_kind), release_note)

    def added_release_notes(self, file_path, data):
        return self.get_release_notes(file_path, data)

    def modified_release_notes(self, file_path, data):
        release_note = super(LayoutContent, self).modified_release_notes(file_path, data)

        if release_note:
            return self.get_release_notes(file_path, data)

        # error or ignored release_note
        return release_note
=======
        return "Incident Layouts"

    @staticmethod
    def get_release_notes(cnt):
        rn = cnt.get("releaseNotes", "")

        layout_kind = LAYOUT_TYPE_TO_NAME.get(cnt.get("kind", ""))
        if not layout_kind:
            print_error("invalid layout kind %s" % (cnt.get("kind", ""),))
            return None

        layout_type = cnt.get("typeId")
        if not layout_type:
            print_error("invalid layout kind %s" % (layout_type,))
            return None

        return release_notes_item(layout_type + " - " + layout_kind, rn)

    def added_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None

        return LayoutContent.get_release_notes(cnt)

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")

        if len(rn) == 0:
            return None

        if rn == "-":
            return ""

        return LayoutContent.get_release_notes(cnt)


Content.register(LayoutContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class ClassifierContent(Content):
    def load_data(self, data):
        return json.loads(data)

    def get_header(self):
        return "Classification & Mapping"

<<<<<<< HEAD
    def get_release_notes(self, file_path, data):
        release_note = super(ClassifierContent, self).get_release_notes(file_path, data)
        brand_name = data.get("brandName")
        if not brand_name:
            print_error('Invalid classifier brand name {}'.format(brand_name))
            return None

        if release_note:
            return release_notes_item(brand_name, release_note)

        return release_note

    def added_release_notes(self, file_path, data):
        release_note = super(ClassifierContent, self).added_release_notes(file_path, data)

        if release_note:
            return self.get_release_notes(file_path, data)

        # error
        return release_note

    def modified_release_notes(self, file_path, data):
        release_note = super(ClassifierContent, self).modified_release_notes(file_path, data)

        if release_note:
            return self.get_release_notes(file_path, data)

        # error or ignored release_note
        return release_note
=======
    @staticmethod
    def get_release_notes(cnt):
        rn = cnt.get("releaseNotes", "")
        brand_name = cnt.get("brandName")
        if not brand_name:
            print_error("invalid classifier brand name %s" % (brand_name,))
            return None

        return release_notes_item(brand_name, rn)

    def added_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None

        return ClassifierContent.get_release_notes(cnt)

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")

        if len(rn) == 0:
            return None

        if rn == "-":
            return ""

        return ClassifierContent.get_release_notes(cnt)


Content.register(ClassifierContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class ReputationContent(Content):
    def __init__(self):
        super(ReputationContent, self).__init__()
        self.show_secondary_header = False

    def load_data(self, data):
        return json.loads(data)

    def get_header(self):
        return "Reputations"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        # This should never happen
        return ""

    def modified_release_notes(self, file_path, data):
        release_note = super(ReputationContent, self).modified_release_notes(file_path, data)

        if release_note:
            return add_dot(release_note) + "\n"

        return release_note
=======
    def added_release_notes(self, cnt):
        # This should never happen
        return ""

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = add_dot(rn) + "\n"
        return res


Content.register(ReputationContent)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


class IntegrationContent(Content):
    def load_data(self, data):
        return yaml.safe_load(data)

    def get_header(self):
        return "Integrations"

<<<<<<< HEAD
    def added_release_notes(self, file_path, data):
        return release_notes_item(data["display"], data["description"])

    def modified_release_notes(self, file_path, data):
        release_note = super(IntegrationContent, self).modified_release_notes(file_path, data)

        if release_note:
            return release_notes_item(data["display"], release_note)

        return release_note


RELEASE_NOTE_GENERATOR = {
=======
    def added_release_notes(self, cnt):
        return release_notes_item(cnt["display"], cnt["description"])

    def modified_release_notes(self, cnt):
        rn = cnt.get("releaseNotes", "")
        if len(rn) == 0:
            return None
        res = ""

        if rn != '-':
            res = release_notes_item(cnt["display"], rn)
        return res


Content.register(IntegrationContent)

release_note_generator = {
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
    INTEGRATIONS_DIR: IntegrationContent(),
    SCRIPTS_DIR: ScriptContent(),
    PLAYBOOKS_DIR: PlaybookContent(),
    REPORTS_DIR: ReportContent(),
    DASHBOARDS_DIR: DashboardContent(),
    WIDGETS_DIR: WidgetContent(),
    INCIDENT_FIELDS_DIR: IncidentFieldContent(),
    LAYOUTS_DIR: LayoutContent(),
    CLASSIFIERS_DIR: ClassifierContent(),
<<<<<<< HEAD
    INDICATOR_TYPES_DIR: ReputationContent()
}


def handle_deleted_file(full_file_name, git_sha1):
    """
    Create release note for deleted file.

    :param full_file_name: path to file in repository
    :param git_sha1: git_sha1 to compare to
    :return: None
    """
    data = get_remote_file(full_file_name, git_sha1)
    # If the data that returns is {} than the file is a md file,
    # for such files we will not have a release note generator and we will skip
    if data:
        name = data.get('name') or full_file_name
        file_type = full_file_name.split("/")[0]
        file_type_mapping = RELEASE_NOTE_GENERATOR.get(file_type)
        if file_type_mapping is not None:
            file_type_mapping.add('D', name)


def create_file_release_notes(change_type, full_file_name):
    """
    Create release note for changed file.

    :param change_type: git change status (A, M, R*)
    :param full_file_name: path to file in repository
    :return: None
    """
    if isinstance(full_file_name, tuple):
        _, full_file_name = full_file_name

    is_pack = is_file_path_in_pack(full_file_name)
    if is_pack:
        file_type = full_file_name.split("/")[2]
    else:
        file_type = full_file_name.split("/")[0]
    base_name = os.path.basename(full_file_name)
    file_suffix = os.path.splitext(base_name)[-1]
    file_type_mapping = RELEASE_NOTE_GENERATOR.get(file_type)

    if file_type_mapping is None or file_suffix not in CONTENT_FILE_SUFFIXES:
        print_warning("Unsupported file type: {}".format(full_file_name))
        return

    if change_type != "R100":  # only file name has changed (no actual data was modified
        if 'R' in change_type:
            # handle the same as modified
            change_type = 'M'

        file_type_mapping.add(change_type, CONTENT_LIB_PATH + full_file_name)


def get_release_notes_draft(github_token, asset_id):
    """
    if possible, download current release draft from content repository in github.

    :param github_token: github token with push permission (in order to get the draft).
    :param asset_id: content build's asset id.
    :return: draft text (or empty string on error).
    """
    if github_token is None:
        print_warning('unable to download draft without github token.')
        return ''

    # Disable insecure warnings
    requests.packages.urllib3.disable_warnings()  # pylint: disable=no-member

    try:
        res = requests.get('https://api.github.com/repos/demisto/content/releases',
                           verify=False,  # guardrails-disable-line
                           headers={'Authorization': 'token {}'.format(github_token)})
    except requests.exceptions.ConnectionError as exc:
        print_warning('unable to get release draft, reason:\n{}'.format(str(exc)))
        return ''

    if res.status_code != 200:
        print_warning('unable to get release draft ({}), reason:\n{}'.format(res.status_code, res.text))
        return ''

    drafts = [release for release in res.json() if release.get('draft', False)]
    if drafts:
        if len(drafts) == 1:
            draft_body = drafts[0]['body']
            raw_asset = re.findall(r'Release Notes for version .* \((\d{5,}|xxxxx)\)', draft_body, re.IGNORECASE)
            if raw_asset:
                draft_body = draft_body.replace(raw_asset[0], asset_id)
            return draft_body

        print_warning('Too many drafts to choose from ({}), skipping update.'.format(len(drafts)))

    return ''


def create_content_descriptor(version, asset_id, res, github_token, beta_rn=None):
    # time format example 2017 - 06 - 11T15:25:57.0 + 00:00
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0+00:00")
    release_notes = '# Cortex XSOAR Content Release Notes for version {} ({})\n'.format(version, asset_id)
    release_notes += '##### Published on {}\n{}'.format(datetime.datetime.now().strftime("%d %B %Y"), res)
=======
    REPUTATIONS_DIR: ReputationContent()
}


def parse_change_list(file_path):
    with open(file_path, 'r') as f:
        data = f.read()
        return data.split("\n")


def get_deleted_content(full_file_name, data):
    start_index = data.find(full_file_name)
    if start_index > 0:
        name_index = data.find("-name:", start_index)
        if name_index > 0:
            return data[name_index:].split("\n")[0][len("-name:"):].strip()
    return full_file_name


def handle_deleted_file(delete_file_path, full_file_name):
    with open(delete_file_path, 'r') as f:
        data = f.read()
        if "/" in full_file_name:
            file_type = full_file_name.split("/")[0]
            file_type_mapping = release_note_generator.get(file_type)
            deleted_content = get_deleted_content(full_file_name, data)
            if file_type_mapping is not None:
                file_type_mapping.add("D", deleted_content)


def create_file_release_notes(file_name, delete_file_path):
    if len(file_name) > 0:
        names = file_name.split("\t")
        change_type = names[0]
        full_file_name = names[1]

        if not "/" in full_file_name:
            return

        file_type = full_file_name.split("/")[0]
        file_type_mapping = release_note_generator.get(file_type)
        if file_type_mapping is None:
            print "Unsupported file type " + file_type
            return

        if change_type == "D":
            handle_deleted_file(delete_file_path, full_file_name)
        elif change_type != "R100" and change_type != "R094":
            if change_type == "R093" or change_type == "R098" or change_type == "R078":
                # handle the same as modified
                full_file_name = names[2]
                change_type = 'M'

            file_type_mapping.add(change_type, contentLibPath + full_file_name)


def create_content_descriptor(version, asset_id, res):
    # time format example 2017 - 06 - 11T15:25:57.0 + 00:00
    date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.0+00:00")
    release_notes = "## Demisto Content Release Notes for version " + version + " (" + asset_id + ")\n"
    release_notes += "##### Published on %s\n%s" % (datetime.datetime.now().strftime("%d %B %Y"), res)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
    content_descriptor = {
        "installDate": "0001-01-01T00:00:00Z",
        "assetId": int(asset_id),
        "releaseNotes": release_notes,
        "modified": date,
        "ignoreGit": False,
        "releaseDate": date,
        "version": -1,
        "release": version,
        "id": ""
    }
<<<<<<< HEAD

    draft = get_release_notes_draft(github_token, asset_id)
    if draft:
        content_descriptor['releaseNotes'] = draft

    with open('content-descriptor.json', 'w') as outfile:
        json.dump(content_descriptor, outfile)

    with open('release-notes.md', 'w') as outfile:
        outfile.write(release_notes)

    print("saving beta release notes")
    with open('beta-release-notes.md', 'w') as outfile:
        beta_release_notes = '## Cortex XSOAR Content Beta Release Notes for version {}\n'.format(NEXT_VERSION)
        beta_release_notes += '##### Published on {}\n{}'.format(datetime.datetime.now().strftime("%d %B %Y"),
                                                                 beta_rn)
        outfile.write(beta_rn)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('version', help='Release version')
    arg_parser.add_argument('git_sha1', help='commit sha1 to compare changes with')
    arg_parser.add_argument('asset_id', help='Asset ID')
    arg_parser.add_argument('server_version', help='Server version')
    arg_parser.add_argument('--github-token', help='Github token')
    args = arg_parser.parse_args()

    tag = get_last_release_version()
    print('Last release version: {}'.format(tag))

    # get changed yaml/json files (filter only relevant changed files)
    validate_manager = ValidateManager()
    try:
        change_log = run_command('git diff --name-status {}'.format(args.git_sha1), exit_on_error=False)
    except RuntimeError:
        print_error('Unable to get the SHA1 of the commit in which the version was released. This can happen if your '
                    'branch is not updated with origin master. Merge from origin master and, try again.\n'
                    'If you\'re not on a fork, run "git merge origin/master".\n'
                    'If you are on a fork, first set https://github.com/demisto/content to be '
                    'your upstream by running "git remote add upstream https://github.com/demisto/content". After '
                    'setting the upstream, run "git fetch upstream", and then run "git merge upstream/master". Doing '
                    'these steps will merge your branch with content master as a base.')
        sys.exit(1)
    else:
        modified_files, added_files, removed_files, _, _ = validate_manager.filter_changed_files(change_log)
        modified_files, added_files, removed_files = filter_packagify_changes(modified_files, added_files,
                                                                              removed_files, tag=tag)

        print('Processing added files')
        for file_path in added_files:
            print(f'Processing {file_path}')
            create_file_release_notes('A', file_path)

        print('Processing modified files')
        for file_path in modified_files:
            print(f'Processing {file_path}')
            create_file_release_notes('M', file_path)

        print('Processing removed files')
        for file_path in removed_files:
            print(f'Processing {file_path}')
            # content entities are only yml/json files. ignore all the rest.
            if file_path.endswith('.yml') or file_path.endswith('.json'):
                handle_deleted_file(file_path, tag)

        # join all release notes
        res = []
        beta_res = []
        missing_release_notes = False
        for key in RELEASE_NOTES_ORDER:
            value = RELEASE_NOTE_GENERATOR[key]
            ans, beta_ans = value.generate_release_notes(args.server_version)
            if ans is None or value.is_missing_release_notes:
                missing_release_notes = True
            if ans:
                res.append(ans)
            if beta_ans:
                beta_res.append(beta_ans)

        release_notes = "\n---\n".join(res)
        beta_release_notes = "\n---\n".join(beta_res)
        create_content_descriptor(args.version, args.asset_id, release_notes, args.github_token,
                                  beta_rn=beta_release_notes)

        if missing_release_notes:
            print_error("Error: some release notes are missing. See previous errors.")
            sys.exit(1)


if __name__ == "__main__":
    main()
=======
    with open('content-descriptor.json', 'w') as outfile:
        json.dump(content_descriptor, outfile)

    with open('release-notes.txt', 'w') as outfile:
        outfile.write(release_notes)


def main(argv):
    if len(argv) < 4:
        print "<Release version>, <File with the full list of changes>, " \
              "<Complete diff file for deleted files>, <assetID>"
        sys.exit(1)
    files = parse_change_list(argv[1])

    for file in files:
        create_file_release_notes(file, argv[2])

    res = []
    missing_release_notes = False
    for key in RELEASE_NOTES_ORDER:
        value = release_note_generator[key]
        ans = value.generate_release_notes()
        if ans is None:
            missing_release_notes = True
        elif len(ans) > 0:
            res.append(ans)

    if missing_release_notes:
        sys.exit(1)

    version = argv[0]
    asset_id = argv[3]

    release_notes = "\n---\n".join(res)
    create_content_descriptor(version, asset_id, release_notes)


if __name__ == "__main__":
    main(sys.argv[1:])
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
