import json
import os
import sys
import logging
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import common
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class BaseTemplateGenerator:
    def __init__(self, template_dir, output_suffix):
        self.init_vars = common.get_initial_variables()
        self.project_list = common.get_project_list()
        
        self.env = Environment(
            loader=FileSystemLoader(os.path.join(config.PORTAINER_TEMPLATES_DIR, template_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        self.env.globals.update(init_vars=self.init_vars)
        self.env.globals.update(get_project_vars=common.get_project_vars)
        
        self.out_basedir_fullpath = os.path.join(config.PORTAINER_TEMPLATES_OUTPUT, output_suffix)
        
        logger.info(f"Initialized {self.__class__.__name__} with template_dir={template_dir}, output_suffix={output_suffix}")

    def create_output_directories(self):
        try:
            os.makedirs(self.out_basedir_fullpath, exist_ok=True)
            logger.info(f"Created output directory: {self.out_basedir_fullpath}")
        except OSError as e:
            logger.error(f"Failed to create output directory: {e}")
            raise

    def generate_templates(self):
        try:
            self.create_output_directories()
            
            template = self.env.get_template("templates.j2")
            projects = {"projects": self.project_list}
            
            out_filename = os.path.join(self.out_basedir_fullpath, "templates.json")
            with open(out_filename, "w") as out_file:
                out_file.write(template.render(projects))
            logger.info(f"Generated templates file: {out_filename}")

            # Validate the generated JSON
            with open(out_filename) as in_file:
                templates = json.load(in_file)
            logger.info("Successfully validated JSON")

            # Check minimum file size
            file_size = os.path.getsize(out_filename)
            if file_size < config.MIN_TEMPLATE_FILE_SIZE:
                error_msg = f"Generated templates file is too small: {file_size} bytes"
                logger.error(error_msg)
                raise Exception(error_msg)
            logger.info(f"File size check passed: {file_size} bytes")

        except TemplateNotFound as e:
            logger.error(f"Template not found: {e}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON generated: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during template generation: {e}")
            raise 