# Copyright (C) 2021  Technorabilia
# Written by Simon de Kraa <simon@technorabilia.com>
# Modified (C) 2025  Madmaximux <madmaximux@GitHub>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import textwrap

import requests
import yaml
import project_vars_processor


def get_project_vars(project_name, init_vars, mode, template_type):
    project_vars = init_vars.copy()

    vars_url = "https://raw.githubusercontent.com/linuxserver/docker-{}/master/readme-vars.yml".format(
        project_name)
    response = requests.get(vars_url)
    project_vars.update(yaml.load(response.text, Loader=yaml.FullLoader))

    # Process project_vars using the processor (which now handles overrides)
    project_vars = project_vars_processor.process_project_vars(project_vars, project_name, mode, template_type)
    return project_vars


def get_initial_variables():
    vars_url = "https://raw.githubusercontent.com/linuxserver/docker-jenkins-builder/master/ansible/vars/common.yml"
    resp = requests.get(vars_url)
    init_vars = yaml.load(resp.text, Loader=yaml.FullLoader)

    vars_url = "https://raw.githubusercontent.com/linuxserver/docker-jenkins-builder/master/ansible/vars/_container-vars-blank"
    resp = requests.get(vars_url)
    init_vars.update(yaml.load(resp.text, Loader=yaml.FullLoader))

    # blank out certain vars
    init_vars["param_net"] = ""
    return init_vars


def get_project_list():
    image_url = "https://fleet.linuxserver.io/api/v1/images"
    response = requests.get(image_url)
    response_json = response.json()
    project_list = response_json["data"]["repositories"]["linuxserver"]

    project_list = list(
        filter(lambda project: not project["deprecated"], project_list))
    
    excluded_names = {"ci", "d2-builder", "jenkins-builder", "lsio-api", "python", "readme-sync"}
    project_list = list(
        filter(lambda project: project['name'] not in excluded_names, project_list))

    # # testing
    # project_list = list(
    #     filter(lambda project: project["name"] in ["plex", "sonarr", "tautulli", "nzbget", "emby", "jellyfin"], project_list))

    return project_list
