from unittest import mock

from k2var import data_store


@mock.patch('k2var.data_store.path')
def test_valid_epic_ids(path):
    path.isfile.return_value = True

    epicid = 1
    with mock.patch.object(data_store.Database, '__iter__') as mock_iter:
        mock_iter.return_value = iter([epicid, ])
        db = data_store.Database()
        assert list(db.valid_epic_ids()) == [epicid, ]
