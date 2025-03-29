#!/usr/bin/env python3
#
# Portainer App Templates for LinuxServer.io Docker containers
# Copyright (C) 2021  Technorabilia
# Written by Simon de Kraa <simon@technorabilia.com>
#
# Modified by Madmaximux <madmaximux@GitHub>
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

"""
Master script to generate both custom and standard Portainer templates.
This script performs initialization tasks once (fetching variables, project list, 
and get_project_vars) and then passes these values to the template generators.
"""

import sys
import os
import logging

from base_template_generator import BaseTemplateGenerator

# Add one level above to the Python path to locate the common module.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import common

def generate_templates_for(mode, template_type, init_vars, project_list, project_vars):
    """
    Generates templates for a given template type.
    
    Arguments:
        template_type (str): The type of templates to generate (e.g., 'standard' or 'custom').
        init_vars (dict): The initialization variables.
        project_list (list): The list of projects.
        project_vars (dict): Project variables to pass into the Jinja environment.
    """
    logging.info("Generating %s templates", template_type)
    generator = BaseTemplateGenerator(
        mode=mode,
        template_type=template_type,
        init_vars=init_vars,
        project_list=project_list,
        project_vars=project_vars
    )
    generator.generate_templates()
    logging.info("%s templates generated successfully", template_type.capitalize())

def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    try:
        # Perform initialization tasks once.
        logging.info("Initializing variables and project list")
        init_vars = common.get_initial_variables()
        project_list = common.get_project_list()
        logging.info("Initialization complete")
        
        # Retrieve get_project_vars only once for the entire project.
        project_vars = {"get_project_vars": common.get_project_vars}

        # Define the order of template generation.
        mode = "templates"
        template_types = ["standard", "custom"]
        for template_type in template_types:
            generate_templates_for(mode, template_type, init_vars, project_list, project_vars)

    except Exception as e:
        logging.error("Template generation failed: %s", e)
        raise

if __name__ == "__main__":
    main()
