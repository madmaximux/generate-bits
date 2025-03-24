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

from base_script_generator import BaseScriptGenerator

if __name__ == "__main__":
    docker_env_content = '''
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
'''

    generator = BaseScriptGenerator(
        template_dir="custom",
        output_suffix="custom",
        docker_env_content=docker_env_content
    )
    generator.generate_scripts()
