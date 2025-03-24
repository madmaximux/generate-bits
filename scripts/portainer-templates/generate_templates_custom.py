# Portainer App Templates for LinuxServer.io Docker containers
# Copyright (C) 2021  Technorabilia
# Written by Simon de Kraa <simon@technorabilia.com>
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

import json
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import common_standard as common

from jinja2 import Environment, FileSystemLoader

init_vars = common.get_initial_variables()
project_list = common.get_project_list()

env_standard = Environment(loader=FileSystemLoader(
    "./templates/portainer-templates/standard"), trim_blocks=True, lstrip_blocks=True)
env_standard.globals.update(init_vars=init_vars)
env_standard.globals.update(get_project_vars=common.get_project_vars)
template = env_standard.get_template("templates.j2")

out_basedir = "./output/portainer-templates"
out_basedir_standard = "{}/standard".format(out_basedir)
out_basedirs_list = [out_basedir_standard]

for directory in out_basedirs_list:
    os.makedirs(directory, exist_ok=True)

projects = {
    "projects": project_list
}

out_filename = "{}/templates.json".format(out_basedir_standard)
with open(out_filename, "w") as out_file:
    out_file.write(template.render(projects))

# check valid json
with open(out_filename) as in_file:
    templates = json.load(in_file)

# check filesize
if os.path.getsize(out_filename) < 200000:
    raise Exception
