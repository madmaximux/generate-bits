import os

# Base directories
TEMPLATES_DIR = "./templates"
OUTPUT_DIR = "./output"

# Docker bits configuration
DOCKER_BITS_DIR = os.path.join(TEMPLATES_DIR, "docker-bits")
DOCKER_BITS_OUTPUT = os.path.join(OUTPUT_DIR, "docker-bits/lsio")

# Portainer templates configuration
PORTAINER_TEMPLATES_DIR = os.path.join(TEMPLATES_DIR, "portainer-templates")
PORTAINER_TEMPLATES_OUTPUT = os.path.join(OUTPUT_DIR, "portainer-templates/lsio")

# Validation settings
MIN_TEMPLATE_FILE_SIZE = 200000  # bytes