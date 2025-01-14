import numpy as np

from hyspecppt.hppt.experiment_settings import DEFAULT_EXPERIMENT, DEFAULT_LATTICE, PLOT_TYPES
from hyspecppt.hppt.hppt_model import HyspecPPTModel  # noqa: F401


def test_setdefaultvalues():
    """Test setting single crystal data function"""
    model = HyspecPPTModel()
    assert model.Ei == DEFAULT_EXPERIMENT["Ei"]
    assert model.S2 == DEFAULT_EXPERIMENT["S2"]
    assert model.alpha_p == DEFAULT_EXPERIMENT["alpha_p"]
    assert model.plot_type == DEFAULT_EXPERIMENT["plot_type"]


def test_set_and_get_singlecrystaldata():
    """Test setting and getting single crystal data function"""
    model = HyspecPPTModel()
    params = DEFAULT_LATTICE
    model.set_single_crystal_data(params)
    assert model.get_single_crystal_data()["a"] == params["a"]
    assert model.get_single_crystal_data()["b"] == params["b"]
    assert model.get_single_crystal_data()["c"] == params["c"]

    assert model.get_single_crystal_data()["alpha"] == params["alpha"]
    assert model.get_single_crystal_data()["beta"] == params["beta"]
    assert model.get_single_crystal_data()["gamma"] == params["gamma"]

    assert model.get_single_crystal_data()["h"] == params["h"]
    assert model.get_single_crystal_data()["k"] == params["k"]
    assert model.get_single_crystal_data()["l"] == params["l"]


def test_set_and_get_crosshairdata():
    """Test setting and getting crosshair data function"""
    model = HyspecPPTModel()
    current_experiment_type = "powder"
    model.set_crosshair_data(current_experiment_type=current_experiment_type, DeltaE=20.0, modQ=1.0)
    assert model.get_crosshair_data()["DeltaE"] == 20.0
    assert model.get_crosshair_data()["modQ"] == 1.0

    current_experiment_type = "single_crystal"
    model.set_single_crystal_data(DEFAULT_LATTICE)
    model.set_crosshair_data(current_experiment_type=current_experiment_type, DeltaE=30.0, modQ=1.0)
    assert model.get_crosshair_data()["DeltaE"] == 30.0
    assert model.get_crosshair_data()["modQ"] == 0.0
    model.cp.sc_parameters.h = 10
    model.cp.sc_parameters.l = 10
    model.cp.sc_parameters.k = 10
    assert np.isclose(model.get_crosshair_data()["modQ"], 108.827)  # modQ greater than maxQ
    assert model.cp.modQ == 0.0  # stored modQ is still 0.0


def test_set_and_get_experimentdata():
    """Test setting and getting experiment data function"""
    model = HyspecPPTModel()
    model.set_experiment_data(Ei=10.0, S2=35.0, alpha_p=45.0, plot_type=PLOT_TYPES[0])
    assert model.get_experiment_data()["Ei"] == 10.0
    assert model.get_experiment_data()["S2"] == 35.0
    assert model.get_experiment_data()["alpha_p"] == 45.0
    assert model.get_experiment_data()["plot_type"] == PLOT_TYPES[0]


def test_calculate_graph_data_alpha():
    """Test calculating different graph data"""
    model = HyspecPPTModel()
    model.set_experiment_data(Ei=20.0, S2=60.0, alpha_p=30.0, plot_type=PLOT_TYPES[0])
    assert np.isclose(min(model.calculate_graph_data()["Q_low"]), 1.55338)
    assert np.isclose(max(model.calculate_graph_data()["Q_low"]), 2.30880)

    assert np.isclose(min(model.calculate_graph_data()["Q_hi"]), 3.25839)
    assert np.isclose(max(model.calculate_graph_data()["Q_hi"]), 5.3811)
    assert model.calculate_graph_data()["E"].all() == np.linspace(-20, 18, 200).all()

    assert model.calculate_graph_data()["Q2d"][0][0] == 0.0
    assert model.calculate_graph_data()["Q2d"][0][1] == 0.0

    assert np.isclose(model.calculate_graph_data()["Q2d"][199][0], 5.38106)
    assert np.isclose(model.calculate_graph_data()["Q2d"][199][1], 5.38106)

    assert np.isclose(model.calculate_graph_data()["E2d"][0][0], -20)
    assert np.isclose(model.calculate_graph_data()["E2d"][0][199], 18.0)

    assert np.isnan(model.calculate_graph_data()["ang_PQ"][0][0])  # not allowed (Q, E) positions
    assert np.isnan(model.calculate_graph_data()["ang_PQ"][84][4])  # not allowed (Q, E) positions

    assert np.isclose(model.calculate_graph_data()["ang_PQ"][84][5], 166.59943)
    assert np.isclose(model.calculate_graph_data()["ang_PQ"][199][0], 114.73561)
    assert np.isnan(model.calculate_graph_data()["ang_PQ"][199][1])  # not allowed (Q, E) positions


def test_calculate_graph_data_cos2_alpha():
    """Test calculating different graph data"""
    model = HyspecPPTModel()
    model.set_experiment_data(Ei=20.0, S2=60.0, alpha_p=30.0, plot_type=PLOT_TYPES[1])
    assert np.isclose(min(model.calculate_graph_data()["Q_low"]), 1.55338)
    assert np.isclose(max(model.calculate_graph_data()["Q_low"]), 2.30880)

    assert np.isclose(min(model.calculate_graph_data()["Q_hi"]), 3.25839)
    assert np.isclose(max(model.calculate_graph_data()["Q_hi"]), 5.3811)
    assert model.calculate_graph_data()["E"].all() == np.linspace(-20, 18, 200).all()

    assert model.calculate_graph_data()["Q2d"][0][0] == 0.0
    assert model.calculate_graph_data()["Q2d"][0][1] == 0.0

    assert np.isclose(model.calculate_graph_data()["Q2d"][199][0], 5.38106)
    assert np.isclose(model.calculate_graph_data()["Q2d"][199][1], 5.38106)

    assert np.isclose(model.calculate_graph_data()["E2d"][0][0], -20)
    assert np.isclose(model.calculate_graph_data()["E2d"][0][199], 18.0)

    assert np.isnan(model.calculate_graph_data()["cos2_ang_PQ"][0][0])  # not allowed (Q, E) positions
    assert np.isnan(model.calculate_graph_data()["cos2_ang_PQ"][84][4])  # not allowed (Q, E) positions

    assert np.isclose(model.calculate_graph_data()["cos2_ang_PQ"][84][5], np.cos(np.radians(166.59943)) ** 2)
    assert np.isclose(model.calculate_graph_data()["cos2_ang_PQ"][199][0], np.cos(np.radians(114.73561)) ** 2)
    assert np.isnan(model.calculate_graph_data()["cos2_ang_PQ"][199][1])  # not allowed (Q, E) positions


def test_calculate_graph_data_cos2_ang_PQ_plus_1_div_2():
    """Test calculating different graph data"""
    model = HyspecPPTModel()
    model.set_experiment_data(Ei=20.0, S2=60.0, alpha_p=30.0, plot_type=PLOT_TYPES[2])
    assert np.isclose(min(model.calculate_graph_data()["Q_low"]), 1.55338)
    assert np.isclose(max(model.calculate_graph_data()["Q_low"]), 2.30880)

    assert np.isclose(min(model.calculate_graph_data()["Q_hi"]), 3.25839)
    assert np.isclose(max(model.calculate_graph_data()["Q_hi"]), 5.3811)
    assert model.calculate_graph_data()["E"].all() == np.linspace(-20, 18, 200).all()

    assert model.calculate_graph_data()["Q2d"][0][0] == 0.0
    assert model.calculate_graph_data()["Q2d"][0][1] == 0.0

    assert np.isclose(model.calculate_graph_data()["Q2d"][199][0], 5.38106)
    assert np.isclose(model.calculate_graph_data()["Q2d"][199][1], 5.38106)

    assert np.isclose(model.calculate_graph_data()["E2d"][0][0], -20)
    assert np.isclose(model.calculate_graph_data()["E2d"][0][199], 18.0)

    assert np.isnan(model.calculate_graph_data()["cos2_ang_PQ_plus_1_div_2"][0][0])  # not allowed (Q, E) positions
    assert np.isnan(model.calculate_graph_data()["cos2_ang_PQ_plus_1_div_2"][84][4])  # not allowed (Q, E) positions

    assert np.isclose(
        model.calculate_graph_data()["cos2_ang_PQ_plus_1_div_2"][84][5], (np.cos(np.radians(166.59943)) ** 2 + 1) / 2
    )
    assert np.isclose(
        model.calculate_graph_data()["cos2_ang_PQ_plus_1_div_2"][199][0], (np.cos(np.radians(114.73561)) ** 2 + 1) / 2
    )
    assert np.isnan(model.calculate_graph_data()["cos2_ang_PQ_plus_1_div_2"][199][1])  # not allowed (Q, E) positions
