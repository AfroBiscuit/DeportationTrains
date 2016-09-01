import export


def test_offset_date():
    assert export.offset_date('05', '01', '1991', 5) == '1996-01-05'


def test_date_certainty():
    assert export.date_certainty('05', '01', '1991') == 'Exact'


def test_generate_deportee_feature_collection():
    pass  # Todo


def test_valid_lat_long():
    good_input = {
        'gsx$long': {
            '$t': '150.44'
        },
        'gsx$lat': {
            '$t': '42.524'
        }
    }
    assert export.valid_lat_long(good_input)


def test_generate_deportee_features():
    pass  # Todo


def test_generate_feature():
    pass  # Todo


def test_generate_deportee_properties():
    pass  # Todo


def test_export_output():
    pass  # Todo


def test_generate_filters():
    pass  # Todo
