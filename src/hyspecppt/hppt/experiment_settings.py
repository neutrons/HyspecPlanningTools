"""Definition of constants and default parameters"""

# unicode
alpha = "\u03b1"
beta = "\u03b2"
gamma = "\u03b3"
square = "\u00b2"
subscript_s = "\u209b"

# defined plot types
PLOT_TYPES = [
    alpha + subscript_s,
    "cos" + square + alpha + subscript_s,
    "(1+cos" + square + alpha + subscript_s + ")/2",
    "cos" + square + alpha + subscript_s + "-sin" + square + alpha + subscript_s,
]

# default parameters
DEFAULT_LATTICE = dict(a=1, b=1, c=1, alpha=90, beta=90, gamma=90, h=0, k=0, l=0)
DEFAULT_EXPERIMENT = dict(Ei=20, S2=30, alpha_p=0, plot_type=PLOT_TYPES[1])
DEFAULT_CROSSHAIR = dict(DeltaE=0, modQ=0)
DEFAULT_MODE = dict(current_experiment_type="single_crystal")
# maximum momentum transfer
MAX_MODQ = 15
# number of points in the plot
N_POINTS = 200
# tank half-width
TANK_HALF_WIDTH = 30.0


# invalid style
INVALID_QLINEEDIT = """
QLineEdit {
border-color: red;
border-style: outset;
border-width: 2px;
border-radius: 4px;
padding-left: -1px;
padding-right: -1px;
padding-top: 1px;
padding-bottom: 1px;
}"""
