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
            assert list(db.valid_epic_ids(campaigns=[0, ])) == [epicid, ]
