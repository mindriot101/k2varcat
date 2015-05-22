import pytest
from k2var import epic as e


@pytest.fixture
def epic():
    return e.Epic(epicid=201644120, campaign=1)


def test_campaign_top_level(epic):
    assert epic.campaign_dir == 'c1'


def test_epic_top_level(epic):
    assert epic.top_level == '201600000'


@pytest.mark.parametrize('input,expected', [((201644120, 1), '44000'),
                                            ((201645050, 1), '45000'),])
def test_epic_bottom_level(input, expected):
    assert e.Epic(*input).bottom_level == expected


def test_output_dir(epic):
    assert epic.output_dir('/') == '/c1/201600000/44000'


def test_png_filename(epic):
    result = epic.png_filename_stub('orig')
    expected = 'hlsp_k2varcat_k2_lightcurve_201644120-c01_kepler_v2_llc-orig.png'
    assert result == expected


def test_png_filename_bad_type(epic):
    with pytest.raises(ValueError) as err:
        epic.png_filename_stub('invalid_type')

    assert 'Image type must be one of' in str(err)

def test_png_filename_full_path(epic):
    result = epic.png_filename('/', 'orig')
    expected = '/c1/201600000/44000/hlsp_k2varcat_k2_lightcurve_201644120-c01_kepler_v2_llc-orig.png'
    assert result == expected
