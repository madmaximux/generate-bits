import os
import sys
import logging
from jinja2 import Environment, FileSystemLoader

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import common
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseScriptGenerator:
    def __init__(self, template_dir, output_suffix, docker_env_content):
        self.init_vars = common.get_initial_variables()
        self.project_list = common.get_project_list()
        
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(config.DOCKER_BITS_DIR, template_dir)),
            trim_blocks=True,
            lstrip_blocks=True,
            keep_trailing_newline=True
        )
        self.env.globals.update(get_project_vars=common.get_project_vars)
        
        self.out_basedir_fullpath = os.path.join(config.DOCKER_BITS_OUTPUT, output_suffix)
        self.docker_env_content = docker_env_content
        
        logger.info(f"Initialized {self.__class__.__name__} with template_dir={template_dir}, output_suffix={output_suffix}")

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

    def generate_scripts(self):
        try:
            self.create_output_directories()
            self.write_docker_env_cfg()

            for project in self.project_list:
                print(project["name"])

                project_vars = common.get_project_vars(
                    project["name"], self.init_vars, mode="scripts")
                if project_vars["project_name"] == "name":
                    continue

                out_dir = os.path.join(self.out_basedir_fullpath, project["name"])
                os.makedirs(out_dir, exist_ok=True)

                # Generate docker-run.sh
                template = self.env.get_template("docker-run.j2")
                with open(os.path.join(out_dir, "docker-run.sh"), "w") as out_file:
                    out_file.write(template.render(project_vars=project_vars))

                # Generate docker-compose.yaml
                template = self.env.get_template("docker-compose.j2")
                with open(os.path.join(out_dir, "docker-compose.yaml"), "w") as out_file:
                    out_file.write(template.render(project_vars=project_vars))

                # Generate run-once.sh
                template = self.env.get_template("run-once.j2")
                with open(os.path.join(out_dir, "run-once.sh"), "w") as out_file:
                    out_file.write(template.render(project_vars=project_vars))

        except Exception as e:
            logger.error(f"Error during script generation: {e}")
            raise 