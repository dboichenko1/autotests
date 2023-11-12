from pydantic import BaseModel, validator,ValidationError

class GET_LIB_V1(BaseModel):
    id: int
    title: str

    @validator('id') #посмотреть migration guide
    def check_that_id_is_less_than_two(cls,v):
        if v > 2:
            raise ValueError("Id is not less than two")
        else:
            return v