import pytest
from k2var import epic as e
from k2var.data_store import Database
from k2var.tasks import render_only_png
import os
import webbrowser


@pytest.fixture
def epic():
    return e.Epic(epicid=201644120, campaign=1)


def test_campaign_top_level(epic):
    assert epic.campaign_dir == 'c1'


def test_epic_top_level(epic):
    assert epic.top_level == '201600000'


@pytest.mark.parametrize('input,expected', [((201644120, 1), '44000'),
                                            ((201645050, 1), '45000'),
                                            ((201199515, 1), '99000'),
                                            ])
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


def test_render_task(tmpdir, epicid_campaign_1, csvfile):
    db = Database(csvfile)
    output_dir = str(tmpdir)
    epic_id, campaign = epicid_campaign_1, 1
    render_only_png(output_dir, epic_id, campaign, db.get(str(epic_id)))

    for p, _, files in os.walk(os.path.dirname(output_dir)):
        for f in files:
            print(os.path.join(p, f))
    for key in ['orig', 'detrend', 'phase']:
        path = ('{0}/c1/201100000/22000/'
            'hlsp_k2varcat_k2_lightcurve_201122454-c01_kepler_v2_llc-{key}.png'.format(
                output_dir, key=key))
        assert os.path.isfile(path)
