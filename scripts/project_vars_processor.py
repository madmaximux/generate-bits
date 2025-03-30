import textwrap

def process_project_vars(project_vars, project_name, mode, template_type):
    """
    Process and override the project_vars dictionary based on mode and template_type.
    
    Args:
        project_vars (dict): The original project variables.
        project_name (str, optional): The project name; if None, uses project_vars["project_name"].
        mode (str): Processing mode ("scripts" or "templates").
        template_type (str): The type of template ("standard" or "custom").
        
    Returns:
        dict: The processed project_vars dictionary.
    """

    if project_name is None:
        project_name = project_vars.get("project_name", "")

    # --- Common overrides for all modes ---
    if "project_blurb" in project_vars:
        blurb = project_vars["project_blurb"]
        blurb = blurb.replace("{{ project_name|capitalize }}", project_name.capitalize())
        blurb = blurb.replace("{{ project_name }}", project_name.capitalize())
        blurb = blurb.replace("{{ project_url }}", project_vars.get("project_url", ""))
        blurb = blurb.replace("\n", " ").replace('"', "'")
        blurb = ' '.join(blurb.split())
        project_vars["project_blurb"] = blurb

    # Remove rows in param_env_vars where env_var is "TZ"
    if "param_env_vars" in project_vars:
        project_vars["param_env_vars"] = [row for row in project_vars["param_env_vars"] if row.get("env_var") != "TZ"]
        if not project_vars["param_env_vars"]:
            project_vars["param_usage_include_env"] = False

    if project_vars.get("project_logo") == "http://www.logo.com/logo.png":
        project_vars["project_logo"] = ""

    if project_vars.get("full_custom_readme", ""):
        project_vars["project_blurb"] = "# This container needs special attention. Please check https://hub.docker.com/r/linuxserver/{} for details.".format(project_vars.get("project_name", ""))

    # --- Process based on template_type ---

    # --- Process standard  ---
    if template_type == "standard":

        # --- Process standard scripts ---
        if mode == "scripts":

            # Replace container name placeholder if provided
            if "param_container_name" in project_vars and project_name:
                project_vars["param_container_name"] = project_vars["param_container_name"].replace(
                    "{{ project_name }}", project_name)
                
            # Wrap project_blurb text into commented lines
            if "project_blurb" in project_vars:
                lines = textwrap.wrap(project_vars["project_blurb"], 78, break_long_words=False)
                new_blurb = ""
                for line in lines:
                    new_blurb += "# {}\n".format(line)
                project_vars["project_blurb"] = new_blurb

            # Process environment variable parameters for scripts
            if "common_param_env_vars" in project_vars:
                for row in project_vars["common_param_env_vars"]:
                    if row.get("env_var") == "PGID":
                        row["env_value"] = "${PGID:-100}"
                        row["desc"] = "for GroupID"
                    if row.get("env_var") == "PUID":
                        row["env_value"] = "${PUID:-1024}"
                        row["desc"] = "for UserID"
                    if row.get("env_var") == "TZ":
                        row["env_value"] = "${TZ:-Europe/Amsterdam}"

        # --- Process standard templates ---
        elif mode == "templates":

            # Process environment variable parameters for templates
            if "common_param_env_vars" in project_vars:
                for row in project_vars["common_param_env_vars"]:
                    if row.get("env_var") == "PGID":
                        row["env_value"] = 100
                        row["desc"] = "for GroupID"
                    if row.get("env_var") == "PUID":
                        row["env_value"] = 1024
                        row["desc"] = "for UserID"
                    if row.get("env_var") == "TZ":
                        row["env_value"] = "Europe/Amsterdam"

    # --- Process custom  ---
    elif template_type == "custom":

        # --- Common for all modes --- #

        # --- Volumes --- #

        # --- param_volumes --- #
        if project_vars["param_usage_include_vols"] and "param_volumes" in project_vars:

            media_keywords = ["movies", "tv", "music", "playlists", "podcasts", "media"]
            download_keywords = ["downloads"]

            # Extract param_volumes from project_vars
            param_volumes = project_vars["param_volumes"]

            # Process each row in param_volumes
            for row in param_volumes:

                vol_path = row.get('vol_path', '')
                # Modify rows based on conditions
                if any(keyword in vol_path for keyword in media_keywords + download_keywords):
                    row['vol_path'] = '/data'
                    row['vol_host_path'] = '/volume1/data'
                    row['desc'] = 'Location of data on disk'
                if any(keyword in vol_path for keyword in media_keywords) and not any(keyword in vol_path for keyword in download_keywords):                    
                    row['vol_path'] = '/data/media'
                    row['vol_host_path'] = '/volume1/data/media'
                    row['desc'] = 'Location of media on disk'
                elif any(keyword in vol_path for keyword in download_keywords) and not any(keyword in vol_path for keyword in media_keywords):
                    row['vol_path'] = '/data/downloads'
                    row['vol_host_path'] = '/volume1/data/downloads'
                    row['desc'] = 'Location of downloads on disk'

            # Remove duplicates based on 'vol_path'
            project_vars["param_volumes"] = list({row['vol_path']: row for row in param_volumes}.values())


        # --- opt_param_volumes --- #
        if project_vars["opt_param_usage_include_vols"] and "opt_param_volumes" in project_vars:

            media_keywords = ["movies", "tv", "music", "playlists", "podcasts", "media"]
            download_keywords = ["downloads"]

            # Extract opt_param_volumes from project_vars
            opt_param_volumes = project_vars["opt_param_volumes"]

            # Process each row in opt_param_volumes
            for row in opt_param_volumes:

                vol_path = row.get('vol_path', '')
                # Modify rows based on conditions
                if any(keyword in vol_path for keyword in media_keywords + download_keywords):
                    row['vol_path'] = '/data'
                    row['vol_host_path'] = '/volume1/data'
                    row['desc'] = 'Location of data on disk'
                if any(keyword in vol_path for keyword in media_keywords) and not any(keyword in vol_path for keyword in download_keywords):                    
                    row['vol_path'] = '/data/media'
                    row['vol_host_path'] = '/volume1/data/media'
                    row['desc'] = 'Location of media on disk'
                elif any(keyword in vol_path for keyword in download_keywords) and not any(keyword in vol_path for keyword in media_keywords):
                    row['vol_path'] = '/data/downloads'
                    row['vol_host_path'] = '/volume1/data/downloads'
                    row['desc'] = 'Location of downloads on disk'

            # Remove duplicates based on 'vol_path'
            project_vars["opt_param_volumes"] = list({row['vol_path']: row for row in opt_param_volumes}.values())

            # Removing duplicates across all volumes
            if project_vars["param_usage_include_vols"] and project_vars["opt_param_usage_include_vols"]:
                # Create a set of 'vol_path' values from param_volumes
                param_vol_paths = {row['vol_path'] for row in project_vars["param_volumes"]}
                # Remove duplicates from opt_param_volumes that are already in param_volumes
                project_vars["opt_param_volumes"] = [row for row in opt_param_volumes if row['vol_path'] not in param_vol_paths]
                if len(project_vars["opt_param_volumes"]) == 0:
                    project_vars["opt_param_usage_include_vols"] = False

        # --- Plex --- #
        if project_name.lower() == "plex":

            # --- Plex ports --- #
            project_vars["param_ports"] = [row for row in project_vars["param_ports"] if row.get("external_port") != "80"]

            project_vars["param_usage_include_ports"] = True
            project_vars["param_ports"] = [
                {"external_port": "32400", "internal_port": "32400/tcp", "port_desc": "Plex Media Server"}
                ]

            project_vars["opt_param_usage_include_ports"] = True
            project_vars["opt_param_ports"] = [
                {"external_port": "32412", "internal_port": "32412/udp", "port_desc": "GDM network discovery (local)"},
                {"external_port": "32410", "internal_port": "32410/udp", "port_desc": "GDM network discovery (local)"},
                {"external_port": "32413", "internal_port": "32413/udp", "port_desc": "GDM network discovery (local)"},
                {"external_port": "32414", "internal_port": "32414/udp", "port_desc": "GDM network discovery (local)"}
            ]

        # --- Process custom scripts ---
        if mode == "scripts":

            # Replace container name placeholder if provided
            if "param_container_name" in project_vars and project_name:
                project_vars["param_container_name"] = project_vars["param_container_name"].replace(
                    "{{ project_name }}", project_name)
                
            # Wrap project_blurb text into commented lines
            if "project_blurb" in project_vars:
                lines = textwrap.wrap(project_vars["project_blurb"], 78, break_long_words=False)
                new_blurb = ""
                for line in lines:
                    new_blurb += "# {}\n".format(line)
                project_vars["project_blurb"] = new_blurb

            # Process environment variable parameters for custom scripts
            if "common_param_env_vars" in project_vars:
                for row in project_vars["common_param_env_vars"]:
                    if row.get("env_var") == "PGID":
                        row["env_value"] = "${PGID:-100}"
                        row["desc"] = "for GroupID"
                    if row.get("env_var") == "PUID":
                        row["env_value"] = "${PUID:-1024}"
                        row["desc"] = "for UserID"
                    if row.get("env_var") == "TZ":
                        row["env_value"] = "${TZ:-America/Chicago}"

                # Insert UMASK if it does not exist
                if not any(r.get("env_var") == "UMASK" for r in project_vars.get("common_param_env_vars", [])):
                    umask_env_var = {
                        "env_var": "UMASK",
                        "env_value": "${UMASK:-002}",
                        "desc": "for UMASK"
                    }
                    tz_index = next((i for i, r in enumerate(project_vars["common_param_env_vars"]) if r.get("env_var") == "TZ"), -1)
                    if tz_index >= 0:
                        project_vars["common_param_env_vars"].insert(tz_index, umask_env_var)
                    else:
                        project_vars.setdefault("common_param_env_vars", []).append(umask_env_var)

            # --- tautulli --- #
            if project_name.lower() == "tautulli":
                project_vars["custom_opt_param_usage_include_vols"] = True
                project_vars["custom_opt_param_volumes"] = [
                    {"vol_path": "/plex_logs", "vol_host_path": "${DOCKERCONFIGPATH:-/volume1/docker/appdata}/plex/Library/Application Support/Plex Media Server/Logs", "desc": "Plex logs"}
                ]
                
        # --- Process custom templates ---
        elif mode == "templates":

            # Process environment variable parameters for custom templates
            if "common_param_env_vars" in project_vars:
                for row in project_vars["common_param_env_vars"]:
                    if row.get("env_var") == "PGID":
                        row["env_value"] = 100
                        row["desc"] = "for GroupID"
                    if row.get("env_var") == "PUID":
                        row["env_value"] = 1024
                        row["desc"] = "for UserID"
                    if row.get("env_var") == "TZ":
                        row["env_value"] = "America/Chicago"

                # Insert UMASK if it does not exist
                if not any(r.get("env_var") == "UMASK" for r in project_vars.get("common_param_env_vars", [])):
                    umask_env_var = {
                        "env_var": "UMASK",
                        "env_value": "002",
                        "desc": "for UMASK"
                    }
                    tz_index = next((i for i, r in enumerate(project_vars["common_param_env_vars"]) if r.get("env_var") == "TZ"), -1)
                    if tz_index >= 0:
                        project_vars["common_param_env_vars"].insert(tz_index, umask_env_var)
                    else:
                        project_vars.setdefault("common_param_env_vars", []).append(umask_env_var)

            # --- tautulli --- #
            if project_name.lower() == "tautulli":
                project_vars["custom_opt_param_usage_include_vols"] = True
                project_vars["custom_opt_param_volumes"] = [
                    {"vol_path": "/plex_logs", "vol_host_path": "/volume1/docker/appdata/plex/Library/Application Support/Plex Media Server/Logs", "desc": "Plex logs"}
                ]

    return project_vars
