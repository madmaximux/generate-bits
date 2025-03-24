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

from jinja2 import Environment, FileSystemLoader

import common

init_vars = common.get_initial_variables()
project_list = common.get_project_list()

env_standard = Environment(loader=FileSystemLoader(
    "templates/docker-bits/standard"), trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
env_standard.globals.update(get_project_vars=common.get_project_vars)

out_basedir = "./output/docker-bits/lsio"
out_basedir_standard = "{}/standard".format(out_basedir)
out_basedirs_list = [out_basedir_standard]
for directory in out_basedirs_list:
    os.makedirs(directory, exist_ok=True)

with open("{}/docker-env.cfg".format(out_basedir_standard), "w") as out_file:
    out_file.write('''#BASEDIR=/volume1/docker
#PUID=1024
#PGID=100
#TZ=Europe/Amsterdam
''')

for project in project_list:
    print(project["name"])

    project_vars = common.get_project_vars(
        project["name"], init_vars, mode="scripts")
    if project_vars["project_name"] == "name":
        continue

    out_dir = "{}/{}".format(out_basedir_standard, project["name"])
    os.makedirs(out_dir, exist_ok=True)

    template = env_standard.get_template("docker-run.j2")
    with open("{}/docker-run.sh".format(out_dir), "w") as out_file:
        out_file.write(template.render(project_vars=project_vars))

    template = env_standard.get_template("docker-compose.j2")
    with open("{}/docker-compose.yaml".format(out_dir), "w") as out_file:
        out_file.write(template.render(project_vars=project_vars))

    template = env_standard.get_template("run-once.j2")
    with open("{}/run-once.sh".format(out_dir), "w") as out_file:
        out_file.write(template.render(project_vars=project_vars))
