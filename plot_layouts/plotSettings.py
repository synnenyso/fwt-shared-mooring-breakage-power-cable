import matplotlib.pyplot as plt
import numpy as np
import re
import matplotlib.pyplot as plt

# -----------------------------------------------------------------
# Get coordinates of the mooring system
# plat : platform / FWT position
# anch : anchor
# buoy : buoy (if exists)
# -----------------------------------------------------------------
def read_coordinates(filename):

    plat = []       # platform coordinates
    anch = []           # anchor coordinates
    buoy = []       # buoy coordinates

    with open(filename, "r") as f:

        next(f)  # skip header

        for line in f:

            parts = line.split()

            name = parts[0]
            x = float(parts[1])
            y = float(parts[2])
            z = float(parts[3])

            if "P" in name:
                plat.append([x, y, z])

            elif "A" in name:
                anch.append([x, y, z])

            elif "B" in name:
                buoy.append([x, y, z])

    return (
        np.array(plat),
        np.array(anch),
        np.array(buoy),
    )


# -----------------------------------------------------------------
# Find SC topologies
# -----------------------------------------------------------------
def read_sc_topologies(filename):
    """
    Read SC topologies from SC_HM.txt or SC_Cyber.txt.

    Returns
    -------
    topologies : list[np.ndarray]

    Example:
    topologies[0] =
    array([
        [1, 2],
        [2, 3],
        [1, 4],
        ...
    ])
    """

    topologies = []

    with open(filename, "r") as f:

        for line in f:

            line = line.strip()

            # Skip header and empty lines
            if not line or not line.startswith("["):
                continue

            pairs = re.findall(r"(\d+)\s+(\d+)", line)

            layout = np.array(
                [[int(a), int(b)] for a, b in pairs],
                dtype=int
            )

            topologies.append(layout)

    return topologies

# -----------------------------------------------------------------
# Read file with linenames
# -----------------------------------------------------------------
def read_line_names(filename):

    with open(filename) as f:

        return [line.strip() for line in f if line.strip()]

# -----------------------------------------------------------------
# Plot layout
# -----------------------------------------------------------------
def plot_base_system(ax, system_type, plat, anch, buoy, line_names):

    lw = 3

    if system_type == "A":

        # -----------------------------------
        # Anchor lines: al_P1F2_A1
        # -----------------------------------
        for name in line_names:

            if not name.startswith("al_"):
                continue

            p = int(re.search(r'P(\d+)', name).group(1))
            a = int(re.search(r'A(\d+)', name).group(1))

            ax.plot(
                [anch[a-1, 0], plat[p-1, 0]],
                [anch[a-1, 1], plat[p-1, 1]],
                color="k",
                linewidth=lw
            )

        # -----------------------------------
        # Shared lines: sl_P1F4_P2F1
        # -----------------------------------
        for name in line_names:

            if not name.startswith("sl_"):
                continue

            p1, p2 = map(int, re.findall(r'P(\d+)', name))

            ax.plot(
                [plat[p1-1, 0], plat[p2-1, 0]],
                [plat[p1-1, 1], plat[p2-1, 1]],
                color="k",
                linewidth=lw
            )

    else:  # System B

        # -----------------------------------
        # Anchor -> Buoy lines
        # -----------------------------------
        for aa, bb in zip(anch, buoy):

            ax.plot(
                [aa[0], bb[0]],
                [aa[1], bb[1]],
                color="k",
                linewidth=lw
            )

        # -----------------------------------
        # Buoy -> Platform lines
        # sl_P1F1_B1
        # -----------------------------------
        for name in line_names:

            if not name.startswith("sl_"):
                continue

            p = int(re.search(r'P(\d+)', name).group(1))
            b = int(re.search(r'B(\d+)', name).group(1))

            ax.plot(
                [buoy[b-1, 0], plat[p-1, 0]],
                [buoy[b-1, 1], plat[p-1, 1]],
                color="k",
                linewidth=lw
            )

    # -----------------------------------
    # Plot nodes
    # -----------------------------------

    ax.plot(
        anch[:, 0],
        anch[:, 1],
        "x",
        color="k",
        markersize=10,
        markeredgewidth=2,
        label="Anchor"
    )

    if len(buoy):
        ax.plot(
            buoy[:, 0],
            buoy[:, 1],
            "o",
            color="k",
            markerfacecolor="k",
            markersize=8,
            label="Buoy"
        )

    ax.plot(
        plat[:, 0],
        plat[:, 1],
        "<",
        color="k",
        markerfacecolor="k",
        markersize=10,
        label="FWT"
    )

    ax.set_aspect("equal")

# -----------------------------------------------------------------
# Plot layout
# -----------------------------------------------------------------
def plot_sc_scc_layout(
    plat,
    anch,
    buoy,
    layout,
    sc_topology,
    scc_FWT,
    scc_or,
    system_type,
    line_names,
):
    """
    Plot one layout: SC topology and one SCC connection and orientation.
    """

    fig, ax = plt.subplots(figsize=(10, 8))

    # Base mooring system
    plot_base_system(ax, system_type, plat, anch, buoy, line_names)

    # Suspended cables (SC)
    for k, (u1, u2) in enumerate(layout):
        x = [plat[u1 - 1, 0], plat[u2 - 1, 0]]
        y = [plat[u1 - 1, 1], plat[u2 - 1, 1]]

        ax.plot(
            x,
            y,
            "r-",
            lw=5,
            label="SC" if k == 0 else None,
        )

    # SCC
    rad = 1440 / 2

    e1 = plat[scc_FWT - 1, :2]

    direction = scc_or - 180

    e2 = [
        e1[0] + rad * np.cos(np.deg2rad(direction)),
        e1[1] + rad * np.sin(np.deg2rad(direction)),
    ]

    ax.plot(
        [e1[0], e2[0]],
        [e1[1], e2[1]],
        "b-",
        lw=7,
        label="SCC",
    )

    # FWT markers
    ax.plot(
        plat[:, 0],
        plat[:, 1],
        "<k",
        ms=12,
    )

    ax.set_title(f"SC {sc_topology} | SCC {scc_FWT}")
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper right", bbox_to_anchor=(1.2,1.2))

    plt.show()