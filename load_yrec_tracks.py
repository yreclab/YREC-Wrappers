"""
load_yrec_tracks.py

Function to load YREC stellar evolution tracks from one or more directories,
with options to create subgiant bundles, EEP tracks grouped by Mass, and isochrones grouped by Age.

Author: Vincent A. Smedile
Institution: The Ohio State University
Date: 2025-08-11

Usage:
    from load_yrec_tracks import load_yrec_tracks
    results = load_yrec_tracks('/path/to/yrec/tracks', recursive=True, iso_round=2)
"""

import os
from glob import glob

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
        Must be a positive integer.

    Returns
    -------
    dict
        Dictionary containing keys for requested outputs. Keys may include:
        'star_lists', 'subgiant_star_lists', 'eep_lists', 'isochrone_lists'.
    """

    # 1. Normalize input so that track_dirs is always a list
    if isinstance(track_dirs, str):
        track_dirs = [track_dirs]

    # 2. Initialize container for all loaded tracks, if requested
    star_lists = {} if load_all_tracks else None

    # 3. Load all .track files from each directory
    if load_all_tracks:
        for track_dir in track_dirs:

            # 3a. Build glob pattern depending on recursive flag
            if recursive:
                pattern = os.path.join(track_dir, '**', '*.track')
                track_files = glob(pattern, recursive=True)
            else:
                pattern = os.path.join(track_dir, '*.track')
                track_files = glob(pattern, recursive=False)

            # 3b. Iterate over each found track file
            for filepath in track_files:

                # Extract directory and filename info for grouping and messages
                dir_path = os.path.dirname(filepath)
                foldername = os.path.basename(dir_path)
                filename = os.path.basename(filepath)

                # Create group name by stripping extension and appending suffix
                list_name = os.path.splitext(foldername)[0] + '_yrectracks'

                # 3c. Load track data using external 'tracker' function
                try:
                    table = tracker(filepath)  # Replace with your actual track loading function
                except Exception as e:
                    print(f"Failed to read {filename} with tracker: {e}")
                    continue  # Skip problematic files

                # 3d. Append loaded track data to the appropriate group list
                if list_name not in star_lists:
                    star_lists[list_name] = []
                star_lists[list_name].append((table, filename))

    # 4. Initialize output dictionary for requested processed results
    output = {}

    # 5. Create subgiant-only track bundles (X_cen <= 1e-4) if requested
    if load_subgiants:
        if not load_all_tracks:
            raise ValueError("load_subgiants=True requires load_all_tracks=True")

        subgiant_star_lists = {}

        # 5a. Iterate over each track group loaded
        for list_name, track_list in star_lists.items():
            subgiant_list = []

            # 5b. For each track DataFrame, filter subgiant phase
            for df, fname in track_list:
                sg_df = df[df['X_cen'] <= 1e-4].copy()
                if sg_df.empty:
                    print(f"⚠️ Warning: Subgiant selection empty for file '{fname}' in list '{list_name}'.")
                else:
                    subgiant_list.append(sg_df)

            # 5c. Store subgiant data under a new key with '_sgb' suffix
            key = list_name + '_sgb'
            if key not in subgiant_star_lists:
                subgiant_star_lists[key] = []
            subgiant_star_lists[key].extend(subgiant_list)

        output['subgiant_star_lists'] = subgiant_star_lists

    # 6. Create isochrone lists grouped by rounded Age(Gyr) if requested
    if load_isochrones:
        if not load_all_tracks:
            raise ValueError("load_isochrones=True requires load_all_tracks=True")

        isochrone_lists = {}

        for track_list in star_lists.values():
            for table, filename in track_list:

                # 6a. Skip if Age(Gyr) column missing
                if 'Age(Gyr)' not in table.columns:
                    continue

                # 6b. Defensive copy to avoid modifying original
                table = table.copy()

                # 6c. Validate rounding parameter
                if iso_round < 1:
                    print('Invalid iso_round value; defaulting to 2.')
                    iso_round = 2

                # 6d. Round Age(Gyr) to specified decimal places for grouping
                table['AgeRounded'] = table['Age(Gyr)'].round(iso_round)

                # 6e. Group by rounded age and collect isochrone data
                for age, age_group in table.groupby('AgeRounded'):
                    iso_name = f"{age:.{iso_round}f}Gyr_iso"
                    if iso_name not in isochrone_lists:
                        isochrone_lists[iso_name] = []
                    # Drop helper column before appending
                    isochrone_lists[iso_name].append(age_group.drop(columns=['AgeRounded']).copy())

        output['isochrone_lists'] = isochrone_lists

    # 7. Create EEP (Equivalent Evolutionary Phase) tracks grouped by Mass if requested
    if load_eeps:
        if not load_all_tracks:
            raise ValueError("load_eeps=True requires load_all_tracks=True")

        eep_lists = {}

        for track_list in star_lists.values():
            for table, filename in track_list:

                # 7a. Skip if Mass column missing
                if 'Mass' not in table.columns:
                    continue

                # 7b. Group by Mass and collect EEP tracks
                for mass, mass_group in table.groupby('Mass'):
                    eep_name = f"{mass:.2f}Msun_eep"
                    if eep_name not in eep_lists:
                        eep_lists[eep_name] = []
                    eep_lists[eep_name].append(mass_group.copy())

        output['eep_lists'] = eep_lists

    # 8. Include all loaded raw tracks in output if requested
    if load_all_tracks:
        output['star_lists'] = star_lists

    # 9. Return the assembled output dictionary
    return output
