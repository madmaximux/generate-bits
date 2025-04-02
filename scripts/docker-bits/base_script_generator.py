#!/usr/bin/env python3
"""
BaseScriptGenerator module.
"""

import json
import os
import sys
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseScriptGenerator:
    def __init__(self, mode, template_type, docker_env_content, init_vars, project_list, project_vars):
        # Accept pre-initialized variables via the constructor
        self.mode = mode
        self.template_type = template_type
        self.docker_env_content = docker_env_content
        self.init_vars = init_vars
        self.project_list = project_list

        self.env = Environment(
            loader=FileSystemLoader(os.path.join(config.DOCKER_BITS_DIR, template_type)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Inject the variables into the Jinja environment
        self.env.globals.update(init_vars=self.init_vars)
        self.env.globals.update(project_vars)  # e.g., {"get_project_vars": common.get_project_vars}

        self.out_basedir_fullpath = os.path.join(config.DOCKER_BITS_OUTPUT, template_type)
        logger.info(f"Initialized {self.__class__.__name__} with template_type='{template_type}'")

    def create_output_directories(self):
        try:
            os.makedirs(self.out_basedir_fullpath, exist_ok=True)
            logger.info(f"Created output directory: {self.out_basedir_fullpath}")
        except OSError as e:
            logger.error(f"Failed to create output directory: {e}")
            raise

    def write_docker_env_cfg(self):
        try:
            with open(os.path.join(self.out_basedir_fullpath, "docker-env.cfg"), "w") as out_file:
                out_file.write(self.docker_env_content.lstrip('\n'))
            logger.info("Created docker-env.cfg file")
        except OSError as e:
            logger.error(f"Failed to write docker-env.cfg: {e}")
            raise

    def safe_get_template(self, template_name):
        """
        Retrieve a template with error handling for missing templates.
        """
        try:
            return self.env.get_template(template_name)
        except TemplateNotFound as e:
            logger.error(f"Template not found: {template_name} - {e}")
            raise

    def generate_scripts(self):
        try:
            self.create_output_directories()
            self.write_docker_env_cfg()

            for project in self.project_list:
                logger.info(f"Processing project: {project.get('name', 'Unknown')}")
                # print(project["name"])

                # Retrieve the get_project_vars function and compute project-specific variables.
                get_project_vars = self.env.globals.get("get_project_vars")
                local_project_vars = get_project_vars(project["name"], self.init_vars, self.mode, self.template_type)
                
                # Skip projects with the default project name.
                if local_project_vars.get("project_name") == "name":
                    continue

                out_dir = os.path.join(self.out_basedir_fullpath, project["name"])
                os.makedirs(out_dir, exist_ok=True)

                # Generate docker-run.sh
                template_run = self.safe_get_template("docker-run.sh.j2")
                with open(os.path.join(out_dir, "docker-run.sh"), "w") as out_file:
                    out_file.write(template_run.render(project_vars=local_project_vars))

                # Generate docker-compose.yaml
                template_compose = self.safe_get_template("docker-compose.yaml.j2")
                with open(os.path.join(out_dir, "docker-compose.yaml"), "w") as out_file:
                    out_file.write(template_compose.render(project_vars=local_project_vars))

                # Generate run-once.sh
                template_run_once = self.safe_get_template("run-once.sh.j2")
                with open(os.path.join(out_dir, "run-once.sh"), "w") as out_file:
                    out_file.write(template_run_once.render(project_vars=local_project_vars))

                # Generate install.sh (custom)
                if self.template_type == "custom":
                    template_install = self.safe_get_template("install.sh.j2")
                    with open(os.path.join(out_dir, "install.sh"), "w") as out_file:
                        out_file.write(template_install.render(project_vars=local_project_vars))

        except Exception as e:
            logger.error(f"Error during script generation: {e}")
            raise 