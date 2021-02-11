<<<<<<< HEAD
import argparse
import json
import logging

import demisto_client
from slack import WebClient as SlackClient

from Tests.configure_and_test_integration_instances import update_content_on_demisto_instance
from Tests.scripts.utils.log_util import install_simple_logging
from Tests.test_integration import __create_integration_instance, __delete_integrations_instances
from demisto_sdk.commands.common.tools import str2bool

SERVER_URL = "https://{}"
=======
import re
import sys
import json
import argparse
from subprocess import Popen, PIPE

import demisto
from slackclient import SlackClient

from test_integration import __create_integration_instance, __delete_integrations_instances


class LOG_COLORS:
    NATIVE = '\033[m'
    RED = '\033[01;31m'
    GREEN = '\033[01;32m'


def print_error(error_str):
    print_color(error_str, LOG_COLORS.RED)


# print srt in the given color
def print_color(msg, color):
    print(str(color) + str(msg) + LOG_COLORS.NATIVE)


def run_git_command(command):
    p = Popen(command.split(), stdout=PIPE, stderr=PIPE)
    p.wait()
    if p.returncode != 0:
        print_error("Failed to run git command " + command)
        sys.exit(1)
    return p.stdout.read()


def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


def options_handler():
    parser = argparse.ArgumentParser(description='Parser for slack_notifier args')
<<<<<<< HEAD
    parser.add_argument('-t', '--instance_tests', type=str2bool, help='is instance test build?', required=True)
    parser.add_argument('-s', '--slack', help='The token for slack', required=True)
    parser.add_argument('-e', '--secret', help='Path to secret conf file', required=True)
    parser.add_argument('-u', '--user', help='The username for the login', required=True)
    parser.add_argument('-p', '--password', help='The password for the login', required=True)
    parser.add_argument('-b', '--buildUrl', help='The url for the build', required=True)
    parser.add_argument('-n', '--buildNumber', help='The build number', required=True)
=======
    parser.add_argument('-n', '--nightly', type=str2bool, help='is nightly build?', required=True)
    parser.add_argument('-s', '--slack', help='The token for slack', required=True)
    parser.add_argument('-e', '--secret', help='Path to secret conf file', required=True)
    parser.add_argument('-c', '--server', help='The server URL to connect to', required=True)
    parser.add_argument('-u', '--user', help='The username for the login', required=True)
    parser.add_argument('-p', '--password', help='The password for the login', required=True)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
    options = parser.parse_args()

    return options


<<<<<<< HEAD
def install_new_content(client, server):
    update_content_on_demisto_instance(client, server, 'Server Master')
=======
def get_demisto_instance_and_login(server, username, password):
    c = demisto.DemistoClient(None, server, username, password)
    res = c.Login()
    if res.status_code is not 200:
        print_error("Login has failed with status code " + str(res.status_code))
        sys.exit(1)

    return c
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07


def get_integrations(secret_conf_path):
    with open(secret_conf_path) as data_file:
        secret_conf = json.load(data_file)

    secret_params = secret_conf['integrations'] if secret_conf else []
    return secret_params


def test_instances(secret_conf_path, server, username, password):
<<<<<<< HEAD
    integrations = get_integrations(secret_conf_path)

    instance_ids = []
    failed_integrations = []
    integrations_counter = 0

    content_installation_client = demisto_client.configure(base_url=server, username=username, password=password,
                                                           verify_ssl=False)
    install_new_content(content_installation_client, server)
    for integration in integrations:
        c = demisto_client.configure(base_url=server, username=username, password=password, verify_ssl=False)
        integrations_counter += 1
        integration_name = integration.get('name')
        integration_instance_name = integration.get('instance_name', '')
        integration_params = integration.get('params')
        devops_comments = integration.get('devops_comments')
        product_description = integration.get('product_description', '')
        is_byoi = integration.get('byoi', True)
        has_integration = integration.get('has_integration', True)
        validate_test = integration.get('validate_test', True)

        if has_integration:
            instance_id, failure_message = __create_integration_instance(
                server, username, password, integration_name, integration_instance_name,
                integration_params, is_byoi, validate_test=validate_test)
            if failure_message == 'No configuration':
                logging.warning(
                    f"skipping {integration_name} as it exists in content-test-conf conf.json but not in content repo")
                continue
            if not instance_id:
                logging.error(
                    f'Failed to create instance of {integration_name} with message: {failure_message}')
                failed_integrations.append("{} {} - devops comments: {}".format(
                    integration_name, product_description, devops_comments))
            else:
                instance_ids.append(instance_id)
                logging.success(f'Create integration {integration_name} succeed')
                __delete_integrations_instances(c, instance_ids)

    return failed_integrations, integrations_counter


def create_failed_integrations_file(failed_instances):
    with open("./Tests/failed_instances.txt", "w") as failed_instances_file:
        failed_instances_file.write('\n'.join(failed_instances))


def get_attachments(secret_conf_path, server, user, password, build_url):
    failed_integration, integrations_counter = test_instances(secret_conf_path, server, user, password)
    create_failed_integrations_file(failed_integration)
=======
    c = get_demisto_instance_and_login(server, username, password)
    integrations = get_integrations(secret_conf_path)

    instance_ids = []
    failed_integration = []
    integrations_counter = 0
    for integration in integrations:
        integrations_counter += 1
        integration_name = integration.get('name', None)
        integration_params = integration.get('params', None)
        is_byoi = integration.get('byoi', True)
        has_integration = integration.get('has_integration', True)

        if has_integration:
            instance_id = __create_integration_instance(c, integration_name, integration_params, is_byoi)
            if not instance_id:
                print_error('Failed to create instance of %s' % (integration_name,))
                failed_integration.append(integration_name)
            else:
                instance_ids.append(instance_id)
                print('Create integration %s succeed' % (integration_name,))

    return failed_integration, integrations_counter


def get_attachments(secret_conf_path, server, user, password):
    failed_integration, integrations_counter = test_instances(secret_conf_path, server, user, password)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07

    fields = []
    if failed_integration:
        field_failed_tests = {
<<<<<<< HEAD
            "title": "Found {0} Problematic Instances. See CircleCI for errors.".format(len(failed_integration)),
=======
            "title": "{0} Problematic Instances".format(len(failed_integration)),
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
            "value": '\n'.join(failed_integration),
            "short": False
        }
        fields.append(field_failed_tests)

    color = 'danger' if failed_integration else 'good'
    title = 'There are no problematic instances' if not failed_integration else 'Encountered problems with instances'

    attachment = [{
        'fallback': title,
        'color': color,
        'title': title,
<<<<<<< HEAD
        'fields': fields,
        'title_link': build_url
=======
        'fields': fields
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
    }]

    return attachment, integrations_counter


<<<<<<< HEAD
def slack_notifier(slack_token, secret_conf_path, server, user, password, build_url, build_number):
    logging.info("Starting Slack notifications about instances")
    attachments, integrations_counter = get_attachments(secret_conf_path, server, user, password, build_url)

    sc = SlackClient(slack_token)

    # Failing instances list
    sc.api_call(
        "chat.postMessage",
        json={
            'channel': 'dmst-content-lab',
            'username': 'Instances nightly report',
            'as_user': 'False',
            'attachments': attachments,
            'text': "You have {0} instances configurations".format(integrations_counter)
        }
    )

    # Failing instances file
    sc.api_call(
        "chat.postMessage",
        json={
            'channel': 'dmst-content-lab',
            'username': 'Instances nightly report',
            'as_user': 'False',
            'text': "Detailed list of failing instances could be found in the following link:\n"
                    "https://{}-60525392-gh.circle-artifacts.com/0/artifacts/failed_instances.txt".format(build_number)

        }
    )


if __name__ == "__main__":
    install_simple_logging()
    options = options_handler()
    if options.instance_tests:
        with open('./env_results.json', 'r') as json_file:
            env_results = json.load(json_file)
            server = f'https://localhost:{env_results[0]["TunnelPort"]}'

        slack_notifier(options.slack, options.secret, server, options.user, options.password, options.buildUrl,
                       options.buildNumber)
        # create this file for destroy_instances script
        with open("./Tests/is_build_passed_{}.txt".format(env_results[0]["Role"].replace(' ', '')), 'a'):
            pass
    else:
        logging.error("Not instance tests build, stopping Slack Notifications about instances")
=======
def slack_notifier(slack_token, secret_conf_path, server, user, password):
    branches = run_git_command("git branch")
    branch_name_reg = re.search("\* (.*)", branches)
    branch_name = branch_name_reg.group(1)

    if branch_name == 'master':
        print_color("Starting Slack notifications about instances", LOG_COLORS.GREEN)
        attachments, integrations_counter = get_attachments(secret_conf_path, server, user, password)

        sc = SlackClient(slack_token)
        sc.api_call(
            "chat.postMessage",
            channel="devops-events",
            username="Instances nightly report",
            as_user="False",
            attachments=attachments,
            text="You have {0} instances configurations".format(integrations_counter)
        )


if __name__ == "__main__":
    options = options_handler()
    if options.nightly:
        slack_notifier(options.slack, options.secret, options.server, options.user, options.password)
    else:
        print_color("Not nightly build, stopping Slack Notifications about instances", LOG_COLORS.RED)
>>>>>>> 9796c09436b0e20b9c2496c40e737b4d4922bc07
