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
#BASEDIR=/volume1/docker
#PUID=1024
#PGID=100
#TZ=America/Chicago
'''

    generator = BaseScriptGenerator(
        template_dir="standard",
        output_suffix="standard",
        docker_env_content=docker_env_content
    )
    generator.generate_scripts()
