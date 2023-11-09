import requests
from configuration import get_lib_export_data_v1, get_lib_export_data_v2
from basic_classes.response import Response
from schemas.get_lib_export_data import GET_LIB_V1_CSHEMA, GET_LIB_V2_CSHEMA
def test_one():
    v1 = requests.get(get_lib_export_data_v1)
    v2 = requests.get(get_lib_export_data_v2)
    Response(v1).assert_status_code(200).validate(GET_LIB_V1_CSHEMA)
    Response(v2).assert_status_code(200).validate(GET_LIB_V2_CSHEMA)

