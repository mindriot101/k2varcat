from unittest import mock

from k2var.data_store import Database

@mock.patch('k2var.data_store.path')
def test_valid_epic_ids(path):
    path.isfile.return_value = True

    epicid = 1
    with mock.patch.object(Database, '__iter__') as mock_iter:
        mock_iter.return_value = iter([epicid, ])
        db = Database()
        assert list(db.valid_epic_ids()) == [epicid, ]
