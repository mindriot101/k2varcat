try:
    from unittest import mock
except ImportError:
    import mock

from k2var import data_store


@mock.patch('k2var.data_store.path')
def test_valid_epic_ids(path):
    path.lexists.return_value = True

    epicid = 1
    with mock.patch.object(data_store.Database, '__iter__') as mock_iter:
        with mock.patch.object(data_store.Database, 'load_data'):
            mock_iter.return_value = iter([epicid, ])
            db = data_store.Database(None)
            assert [items[0] for items in
                    list(db.valid_epic_ids(campaigns=[0, ]))] == [epicid, ]


@mock.patch('k2var.data_store.Database.load_data')
def test_valid_epic_ids_with_fixtures(load_data,
                                      epicid_campaign_0,
                                      epicid_campaign_1,
                                      filename_campaign_0,
                                      filename_campaign_1):
    load_data.return_value = {
        epicid_campaign_0: None,
        epicid_campaign_1: None
    }
    db = data_store.Database(None)
    valid_ids = list(db.valid_epic_ids(campaigns=[0, 1]))
    assert sorted(valid_ids) == sorted([(epicid_campaign_0, 0),
                                        (epicid_campaign_1, 1)])


@mock.patch('k2var.data_store.Database.load_data')
def test_valid_epic_ids_with_fixture_0(load_data,
                                       epicid_campaign_0,
                                       filename_campaign_0):
    load_data.return_value = {
        epicid_campaign_0: None,
    }
    db = data_store.Database(None)
    valid_ids = list(db.valid_epic_ids(campaigns=[0, ]))
    assert sorted(valid_ids) == sorted([(epicid_campaign_0, 0), ])


@mock.patch('k2var.data_store.Database.load_data')
def test_valid_epic_ids_with_fixture_1(load_data,
                                       epicid_campaign_1,
                                       filename_campaign_1):
    load_data.return_value = {
        epicid_campaign_1: None,
    }
    db = data_store.Database(None)
    valid_ids = list(db.valid_epic_ids(campaigns=[1, ]))
    assert sorted(valid_ids) == sorted([(epicid_campaign_1, 1), ])
