"""
load_yrec_tracks.py

Function to load YREC stellar evolution tracks from one or more directories,
with options to create subgiant bundles, EEP tracks grouped by Mass, and isochrones grouped by Age.

If the tracker() function is not already loaded, this script will automatically fetch
the latest version from the YREC-Wrappers GitHub repository and import it dynamically.

Author: Vincent A. Smedile
Institution: The Ohio State University
Date: 2025-08-11
"""

import os
from glob import glob
import importlib.util
import urllib.request
import tempfile

# ============================================================
# AUTOLOAD tracker() FROM GITHUB IF NOT ALREADY AVAILABLE
# ============================================================
try:
    tracker  # test if tracker() is defined in the current scope
except NameError:
    print("tracker() not found — fetching from GitHub...")
    
    # URL of the raw Tracker.py file in the YREC-Wrappers repo
    RAW_TRACKER_URL = (
        "https://raw.githubusercontent.com/yreclab/YREC-Wrappers/main/newheader_yrec/Tracker.py"
    )

    try:
        # Step 1: Download Tracker.py into a temporary file
        with tempfile.NamedTemporaryFile(suffix=".py", delete=False) as tmp_file:
            urllib.request.urlretrieve(RAW_TRACKER_URL, tmp_file.name)
            tmp_path = tmp_file.name

        # Step 2: Dynamically import the downloaded Tracker.py
        spec = importlib.util.spec_from_file_location("tracker_module", tmp_path)
        tracker_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tracker_module)

        # Step 3: Assign tracker() to the global scope
        tracker = tracker_module.tracker
        print("✅ tracker() loaded successfully from GitHub.")

    except Exception as e:
        raise ImportError(
            f"❌ Failed to load tracker() from GitHub. "
            f"Check your internet connection or the repo URL.\nError: {e}"
        )

# ============================================================
# load_yrec_tracks begins here!!
# ============================================================

def load_yrec_tracks(
    track_dirs,
    recursive=True,
    load_subgiants=True,
    load_all_tracks=True,
    load_eeps=True,
    load_isochrones=True,
    iso_round=2
):
    """
    Load YREC tracks and optionally create subgiant bundles, EEP tracks, and isochrones.

    Parameters
    ----------
    track_dirs : str or list of str
        Directory or list of directories to search for .track files.
    recursive : bool
        Whether to search subdirectories recursively.
    load_subgiants : bool
        If True, create and return subgiant-only tracks (X_cen <= 1e-4).
    load_all_tracks : bool
        If True, load and return all tracks.
    load_eeps : bool
        If True, group and return EEP tracks by Mass.
    load_isochrones : bool
        If True, group and return isochrones by Age(Gyr).
    iso_round : int, default 2
        Number of decimal places to round Age(Gyr) values for isochrone grouping.

    Returns
    -------
    dict
        Dictionary containing keys for requested outputs.
    """

    # 1. Normalize input to list
    if isinstance(track_dirs, str):
        track_dirs = [track_dirs]

    # 2. Prepare container for loaded tracks
    star_lists = {} if load_all_tracks else None

    # 3. Load .track files
    if load_all_tracks:
        for track_dir in track_dirs:
            # Build search pattern
            pattern = os.path.join(track_dir, '**', '*.track') if recursive else os.path.join(track_dir, '*.track')
            track_files = glob(pattern, recursive=recursive)

            for filepath in track_files:
                dir_path = os.path.dirname(filepath)
                foldername = os.path.basename(dir_path)
                filename = os.path.basename(filepath)
                list_name = os.path.splitext(foldername)[0] + '_yrectracks'

                try:
                    table = tracker(filepath)  # call the dynamically loaded tracker()
                except Exception as e:
                    print(f"Failed to read {filename} with tracker: {e}")
                    continue

                if list_name not in star_lists:
                    star_lists[list_name] = []
                star_lists[list_name].append((table, filename))

    output = {}

    # 4. Subgiant-only lists
    if load_subgiants:
        if not load_all_tracks:
            raise ValueError("load_subgiants=True requires load_all_tracks=True")

        subgiant_star_lists = {}
        for list_name, track_list in star_lists.items():
            subgiant_list = []
            for df, fname in track_list:
                sg_df = df[df['X_cen'] <= 1e-4].copy()
                if not sg_df.empty:
                    subgiant_list.append(sg_df)
                else:
                    print(f"⚠️ No subgiant phase for '{fname}' in '{list_name}'.")
            subgiant_star_lists[list_name + '_sgb'] = subgiant_list

        output['subgiant_star_lists'] = subgiant_star_lists

    # 5. Isochrones
    if load_isochrones:
        if not load_all_tracks:
            raise ValueError("load_isochrones=True requires load_all_tracks=True")

        isochrone_lists = {}
        for track_list in star_lists.values():
            for table, filename in track_list:
                if 'Age(Gyr)' not in table.columns:
                    continue
                table = table.copy()
                if iso_round < 1:
                    print("Invalid iso_round; defaulting to 2.")
                    iso_round = 2
                table['AgeRounded'] = table['Age(Gyr)'].round(iso_round)
                for age, age_group in table.groupby('AgeRounded'):
                    iso_name = f"{age:.{iso_round}f}Gyr_iso"
                    isochrone_lists.setdefault(iso_name, []).append(
                        age_group.drop(columns=['AgeRounded']).copy()
                    )
        output['isochrone_lists'] = isochrone_lists

    # 6. EEP tracks
    if load_eeps:
        if not load_all_tracks:
            raise ValueError("load_eeps=True requires load_all_tracks=True")

        eep_lists = {}
        for track_list in star_lists.values():
            for table, filename in track_list:
                if 'Mass' not in table.columns:
                    continue
                for mass, mass_group in table.groupby('Mass'):
                    eep_name = f"{mass:.2f}Msun_eep"
                    eep_lists.setdefault(eep_name, []).append(mass_group.copy())
        output['eep_lists'] = eep_lists

    # 7. Add raw tracks if requested
    if load_all_tracks:
        output['star_lists'] = star_lists

    return output
