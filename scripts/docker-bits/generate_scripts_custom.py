# Docker scripts for LinuxServer.io Docker containers
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

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import common

from jinja2 import Environment, FileSystemLoader

init_vars = common.get_initial_variables()
project_list = common.get_project_list()

env = Environment(loader=FileSystemLoader(
    "./templates/docker-bits/custom"), trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
env.globals.update(get_project_vars=common.get_project_vars)

out_basedir = "./output/docker-bits/lsio"
out_basedir_fullpath = "{}/custom".format(out_basedir)
out_basedirs_list = [out_basedir_fullpath]
for directory in out_basedirs_list:
    os.makedirs(directory, exist_ok=True)

with open("{}/docker-env.cfg".format(out_basedir_fullpath), "w") as out_file:
    out_file.write('''
## Global Settings
DOCKERBASEDIR=/volume1/docker
DOCKERCOMPOSEDIRSUFFIX="-compose"
DOCKERCOMPOSEDIR=${DOCKERBASEDIR}/projects
DOCKERCONFIGDIR=${DOCKERBASEDIR}/appdata
DOCKERSTORAGEDIR=/volume1/data
PUID=1028
PGID=65537
UMASK=002
TZ=America/Chicago
''')

for project in project_list:
    print(project["name"])

    project_vars = common.get_project_vars(
        project["name"], init_vars, mode="scripts")
    if project_vars["project_name"] == "name":
        continue

    out_dir = "{}/{}".format(out_basedir_fullpath, project["name"])
    os.makedirs(out_dir, exist_ok=True)

    template = env.get_template("docker-run.j2")
    with open("{}/docker-run.sh".format(out_dir), "w") as out_file:
        out_file.write(template.render(project_vars=project_vars))

    template = env.get_template("docker-compose.j2")
    with open("{}/docker-compose.yaml".format(out_dir), "w") as out_file:
        out_file.write(template.render(project_vars=project_vars))

    template = env.get_template("run-once.j2")
    with open("{}/run-once.sh".format(out_dir), "w") as out_file:
        out_file.write(template.render(project_vars=project_vars))
